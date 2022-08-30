"""This module includes Service functions for work with pytest agent."""

import logging
from os import getenv
import sys
import traceback
from time import time

import pkg_resources
import pytest
from _pytest.doctest import DoctestItem
from _pytest.main import Session

try:
    pkg_resources.get_distribution('pytest >= 3.4.0')
    from _pytest.nodes import File, Item
except pkg_resources.VersionConflict:
    from _pytest.main import File, Item

try:
    pkg_resources.get_distribution('pytest >= 3.8.0')
    from _pytest.warning_types import PytestWarning
except pkg_resources.VersionConflict:
    from pytest_reportportal.errors import PytestWarning


from _pytest.python import Class, Function, Instance, Module
from _pytest.unittest import TestCaseFunction, UnitTestCase

from reportportal_client import ReportPortalService
from reportportal_client.external.google_analytics import send_event
from reportportal_client.helpers import (
    gen_attributes,
    get_launch_sys_attrs,
    get_package_version
)
from reportportal_client.service import _dict_to_payload
from six import with_metaclass
from six.moves import queue


log = logging.getLogger(__name__)


def timestamp():
    """Time for difference between start and finish tests."""
    return str(int(time() * 1000))


def trim_docstring(docstring):
    """
    Convert docstring.

    :param docstring: input docstring
    :return: docstring
    """
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxsize
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxsize:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)


class Singleton(type):
    """Class Singleton pattern."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Redefine call method.

        :param args:   list of additional params
        :param kwargs: dict of additional params
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(
                *args, **kwargs)
        return cls._instances[cls]


class PyTestServiceClass(with_metaclass(Singleton, object)):
    """Pytest service class for reporting test results to the Report Portal."""

    def __init__(self):
        """Initialize instance attributes."""
        self._errors = queue.Queue()
        self._hier_parts = {}
        self._issue_types = {}
        self._item_parts = {}
        self._loglevels = ('TRACE', 'DEBUG', 'INFO', 'WARN', 'ERROR')
        self._skip_analytics = getenv('ALLURE_NO_ANALYTICS')
        self.agent_name = 'pytest-reportportal'
        self.agent_version = get_package_version(self.agent_name)
        self.ignore_errors = True
        self.ignored_attributes = []
        self.log_batch_size = 20
        self.log_item_id = None
        self.parent_item_id = None
        self.rp = None
        self.rp_supports_parameters = True
        try:
            pkg_resources.get_distribution('reportportal_client >= 3.2.0')
        except pkg_resources.VersionConflict:
            self.rp_supports_parameters = False

    @property
    def issue_types(self):
        """Issue types for the Report Portal project."""
        if not self._issue_types:
            if not self.project_settings:
                return self._issue_types
            for item_type in ("AUTOMATION_BUG", "PRODUCT_BUG", "SYSTEM_ISSUE",
                              "NO_DEFECT", "TO_INVESTIGATE"):
                for item in self.project_settings["subTypes"][item_type]:
                    self._issue_types[item["shortName"]] = item["locator"]
        return self._issue_types

    def init_service(self,
                     endpoint,
                     project,
                     uuid,
                     log_batch_size,
                     ignore_errors,
                     ignored_attributes,
                     verify_ssl=True,
                     custom_launch=None,
                     parent_item_id=None,
                     retries=0):
        """Update self.rp with the instance of the ReportPortalService."""
        self._errors = queue.Queue()
        if self.rp is None:
            self.ignore_errors = ignore_errors
            self.ignored_attributes = ignored_attributes
            self.parent_item_id = parent_item_id
            if self.rp_supports_parameters:
                self.ignored_attributes = list(
                    set(ignored_attributes).union({'parametrize'}))
            self.log_batch_size = log_batch_size
            log.debug('ReportPortal - Init service: endpoint=%s, '
                      'project=%s, uuid=%s', endpoint, project, uuid)
            self.rp = ReportPortalService(
                endpoint=endpoint,
                project=project,
                token=uuid,
                log_batch_size=log_batch_size,
                retries=retries,
                verify_ssl=verify_ssl,
                launch_id=custom_launch,
            )
            self.project_settings = None
            if self.rp and hasattr(self.rp, "get_project_settings"):
                self.project_settings = self.rp.get_project_settings()
        else:
            log.debug('The pytest is already initialized')
        return self.rp

    def start_launch(self,
                     launch_name,
                     mode=None,
                     description=None,
                     attributes=None,
                     rerun=False,
                     rerun_of=None,
                     **kwargs):
        """
        Launch test items.

        :param launch_name: name of the launch
        :param mode:        mode
        :param description: description of launch test
        :param kwargs:      additional params
        :return: item ID
        """
        self._stop_if_necessary()
        if self.rp is None:
            return

        sl_pt = {
            'attributes': self._get_launch_attributes(attributes),
            'name': launch_name,
            'start_time': timestamp(),
            'description': description,
            'mode': mode,
            'rerun': rerun,
            'rerunOf': rerun_of
        }
        log.debug('ReportPortal - Start launch: request_body=%s', sl_pt)
        item_id = self.rp.start_launch(**sl_pt)
        log.debug('ReportPortal - Launch started: id=%s', item_id)
        if not self._skip_analytics:
            send_event(self.agent_name, self.agent_version)
        return item_id

    def collect_tests(self, session):
        """
        Collect all tests.

        :param session: pytest.Session
        :return: None
        """
        self._stop_if_necessary()
        if self.rp is None:
            return

        hier_dirs = False
        hier_module = False
        hier_class = False
        hier_param = False
        display_suite_file_name = True

        if not hasattr(session.config, 'workerinput'):
            hier_dirs = session.config.getini('rp_hierarchy_dirs')
            hier_module = session.config.getini('rp_hierarchy_module')
            hier_class = session.config.getini('rp_hierarchy_class')
            hier_param = session.config.getini('rp_hierarchy_parametrize')
            display_suite_file_name = session.config.getini(
                'rp_display_suite_test_file')

        try:
            hier_dirs_level = int(
                session.config.getini('rp_hierarchy_dirs_level'))
        except ValueError:
            hier_dirs_level = 0

        dirs_parts = {}
        tests_parts = {}

        for item in session.items:
            # Start collecting test item parts
            parts = []

            # Hierarchy for directories
            rp_name = self._add_item_hier_parts_dirs(item, hier_dirs,
                                                     hier_dirs_level, parts,
                                                     dirs_parts)

            # Hierarchy for Module and Class/UnitTestCase
            item_parts = self._get_item_parts(item)
            rp_name = self._add_item_hier_parts_other(item_parts, item, Module,
                                                      hier_module, parts,
                                                      rp_name)
            rp_name = self._add_item_hier_parts_other(item_parts, item, Class,
                                                      hier_class, parts,
                                                      rp_name)
            rp_name = self._add_item_hier_parts_other(item_parts, item,
                                                      UnitTestCase, hier_class,
                                                      parts, rp_name)

            # Hierarchy for parametrized tests
            if hier_param:
                rp_name = self._add_item_hier_parts_parametrize(item, parts,
                                                                tests_parts,
                                                                rp_name)

            # Hierarchy for test itself (Function/TestCaseFunction)
            item._rp_name = rp_name + ("::" if rp_name else "") + item.name

            # Result initialization
            for part in parts:
                part._rp_result = "PASSED"

            self._item_parts[item] = parts
            for part in parts:
                if '_pytest.python.Class' in str(type(
                        part)) and not display_suite_file_name and not \
                        hier_module:
                    part._rp_name = part._rp_name.split("::")[-1]
                if part not in self._hier_parts:
                    self._hier_parts[part] = {"finish_counter": 1,
                                              "start_flag": False}
                else:
                    self._hier_parts[part]["finish_counter"] += 1

    def start_pytest_item(self, test_item=None):
        """
        Start pytest_item.

        :param test_item: pytest.Item
        :return: item ID
        """
        self._stop_if_necessary()
        if self.rp is None:
            return

        for part in self._item_parts[test_item]:
            if self._hier_parts[part]["start_flag"]:
                self.parent_item_id = self._hier_parts[part]["item_id"]
                continue
            self._hier_parts[part]["start_flag"] = True
            payload = {
                'name': self._get_item_name(part),
                'description': self._get_item_description(part),
                'start_time': timestamp(),
                'item_type': 'SUITE',
                'parent_item_id': self.parent_item_id,
                'code_ref': str(test_item.fspath)
            }
            log.debug('ReportPortal - Start Suite: request_body=%s', payload)
            item_id = self.rp.start_test_item(**payload)
            self.log_item_id = item_id
            self.parent_item_id = item_id
            self._hier_parts[part]["item_id"] = item_id

        # Item type should be sent as "STEP" until we upgrade to RPv6.
        # Details at:
        # https://github.com/reportportal/agent-Python-RobotFramework/issues/56
        start_rq = {
            'attributes': self._get_item_markers(test_item),
            'name': self._get_item_name(test_item),
            'description': self._get_item_description(test_item),
            'start_time': timestamp(),
            'item_type': 'STEP',
            'parent_item_id': self.parent_item_id,
            'code_ref': '{0}:{1}'.format(test_item.fspath, test_item.name)
        }
        if self.rp_supports_parameters:
            start_rq['parameters'] = self._get_parameters(test_item)

        log.debug('ReportPortal - Start TestItem: request_body=%s', start_rq)
        item_id = self.rp.start_test_item(**start_rq)
        self.log_item_id = item_id
        return item_id

    def finish_pytest_item(self, test_item, item_id, status, issue=None):
        """
        Finish pytest_item.

        :param test_item: test_item
        :param item_id:   Pytest.Item
        :param status:    an item finish status (PASSED, FAILED, STOPPED,
        SKIPPED, RESETED, CANCELLED, INFO, WARN)
        :param issue:     an external system issue reference
        :return: None
        """
        self._stop_if_necessary()
        if self.rp is None:
            return

        fta_rq = {
            'end_time': timestamp(),
            'status': status,
            'issue': issue,
            'item_id': item_id
        }

        log.debug('ReportPortal - Finish TestItem: request_body=%s', fta_rq)

        parts = self._item_parts[test_item]
        self.rp.finish_test_item(**fta_rq)
        while len(parts) > 0:
            part = parts.pop()
            if status == "FAILED":
                part._rp_result = status
            self._hier_parts[part]["finish_counter"] -= 1
            if self._hier_parts[part]["finish_counter"] > 0:
                continue
            payload = {
                'end_time': timestamp(),
                'issue': issue,
                'item_id': self._hier_parts[part]["item_id"],
                'status': part._rp_result
            }
            log.debug('ReportPortal - End TestSuite: request_body=%s', payload)
            self.rp.finish_test_item(**payload)

    def finish_launch(self, status=None, **kwargs):
        """
        Finish tests launch.

        :param status: an launch status (PASSED, FAILED, STOPPED, SKIPPED,
        INTERRUPTED, CANCELLED, INFO, WARN)
        :param kwargs: additional params
        :return: None
        """
        self._stop_if_necessary()
        if self.rp is None:
            return

        # To finish launch session str parameter is needed
        fl_rq = {
            'end_time': timestamp(),
            'status': status
        }
        log.debug('ReportPortal - Finish launch: request_body=%s', fl_rq)
        self.rp.finish_launch(**fl_rq)

    def post_log(self, message, loglevel='INFO', attachment=None):
        """
        Send a log message to the Report Portal.

        :param message:    message in log body
        :param loglevel:   a level of a log entry (ERROR, WARN, INFO, DEBUG,
        TRACE, FATAL, UNKNOWN)
        :param attachment: attachment file
        :return: None
        """
        self._stop_if_necessary()
        if self.rp is None:
            return

        if loglevel not in self._loglevels:
            log.warning('Incorrect loglevel = %s. Force set to INFO. '
                        'Available levels: %s.', loglevel, self._loglevels)
            loglevel = 'INFO'

        sl_rq = {
            'item_id': self.log_item_id,
            'time': timestamp(),
            'message': message,
            'level': loglevel,
            'attachment': attachment
        }
        self.rp.log(**sl_rq)

    def _stop_if_necessary(self):
        """
        Stop tests if any error occurs.

        :return: None
        """
        try:
            exc, msg, tb = self._errors.get(False)
            traceback.print_exception(exc, msg, tb)
            sys.stderr.flush()
            if not self.ignore_errors:
                pytest.exit(msg)
        except queue.Empty:
            pass

    @staticmethod
    def _add_item_hier_parts_dirs(item, hier_flag, dirs_level, report_parts,
                                  dirs_parts, rp_name=""):
        """
        Add item to hierarchy of parents located in directory.

        :param item:         Pytest.Item
        :param hier_flag:    flag
        :param dirs_level:   int value of level
        :param report_parts: ''
        :param dirs_parts:   ''
        :param rp_name:      report name
        :return: str rp_name
        """
        parts_dirs = PyTestServiceClass._get_item_dirs(item)
        dir_path = item.fspath.new(dirname="", basename="", drive="")
        rp_name_path = ""

        for dir_name in parts_dirs[dirs_level:]:
            dir_path = dir_path.join(dir_name)
            path = str(dir_path)

            if hier_flag:
                if path in dirs_parts:
                    item_dir = dirs_parts[path]
                    rp_name = ""
                else:
                    if hasattr(Item, "from_parent"):
                        item_dir = File.from_parent(parent=item,
                                                    fspath=dir_path,
                                                    nodeid=dir_name)
                    else:
                        item_dir = File(dir_path, nodeid=dir_name,
                                        session=item.session,
                                        config=item.session.config)
                    rp_name += dir_name
                    item_dir._rp_name = rp_name
                    dirs_parts[path] = item_dir
                    rp_name = ""

                report_parts.append(item_dir)
            else:
                rp_name_path = path[1:]

        if not hier_flag:
            rp_name += rp_name_path

        return rp_name

    @staticmethod
    def _add_item_hier_parts_parametrize(item, report_parts, tests_parts,
                                         rp_name=""):
        """
        Add item to hierarchy of parents with params.

        :param item:         pytest.Item
        :param report_parts: Parent reports
        :param tests_parts:  test item parts
        :param rp_name:      name of report
        :return: str rp_name
        """
        for mark in item.own_markers:
            if mark.name == 'parametrize':
                ch_index = item.nodeid.find("[")
                test_fullname = item.nodeid[
                                :ch_index if ch_index > 0 else len(
                                    item.nodeid)]
                test_name = item.originalname

                rp_name += ("::" if rp_name else "") + test_name

                if test_fullname in tests_parts:
                    item_test = tests_parts[test_fullname]
                else:
                    if hasattr(Item, "from_parent"):
                        item_test = Item.from_parent(parent=item,
                                                     name=test_fullname,
                                                     nodeid=test_fullname)
                    else:
                        item_test = Item(test_fullname, nodeid=test_fullname,
                                         session=item.session,
                                         config=item.session.config)
                    item_test._rp_name = rp_name
                    item_test.obj = item.obj
                    item_test.keywords = item.keywords
                    item_test.own_markers = item.own_markers
                    item_test.parent = item.parent

                    tests_parts[test_fullname] = item_test

                rp_name = ""
                report_parts.append(item_test)
                break

        return rp_name

    @staticmethod
    def _add_item_hier_parts_other(item_parts, item, item_type, hier_flag,
                                   report_parts, rp_name=""):
        """
        Add item to hierarchy of parents.

        :param item_parts:  Parent_items
        :param item:        pytest.Item
        :param item_type:   (SUITE, STORY, TEST, SCENARIO, STEP, BEFORE_CLASS,
         BEFORE_GROUPS, BEFORE_METHOD, BEFORE_SUITE, BEFORE_TEST, AFTER_CLASS,
        AFTER_GROUPS, AFTER_METHOD, AFTER_SUITE, AFTER_TEST)
        :param hier_flag:    bool state
        :param report_parts: list of parent reports
        :param rp_name:      report name
        :return: str rp_name
        """
        for part in item_parts:

            if type(part) is item_type:

                if item_type is Module:
                    module_path = str(
                        item.fspath.new(dirname=rp_name,
                                        basename=part.fspath.basename,
                                        drive=""))
                    rp_name = module_path if rp_name else module_path[1:]
                elif item_type in (Class, Function, UnitTestCase,
                                   TestCaseFunction):
                    rp_name += ("::" if rp_name else "") + part.name

                if hier_flag:
                    part._rp_name = rp_name
                    rp_name = ""
                    report_parts.append(part)

        return rp_name

    @staticmethod
    def _get_item_parts(item):
        """
        Get item of parents.

        :param item: pytest.Item
        :return list of parents
        """
        parts = []
        parent = item.parent
        if not isinstance(parent, Instance):
            parts.append(parent)
        while True:
            parent = parent.parent
            if parent is None:
                break
            if isinstance(parent, Instance):
                continue
            if isinstance(parent, Session):
                break
            parts.append(parent)

        parts.reverse()
        return parts

    @staticmethod
    def _get_item_dirs(item):
        """
        Get directory of item.

        :param item: pytest.Item
        :return: list of dirs
        """
        root_path = item.session.config.rootdir.strpath
        dir_path = item.fspath.new(basename="")
        rel_dir = dir_path.new(dirname=dir_path.relto(root_path), basename="",
                               drive="")

        dir_list = []
        for directory in rel_dir.parts(reverse=False):
            dir_name = directory.basename
            if dir_name:
                dir_list.append(dir_name)

        return dir_list

    def _get_launch_attributes(self, ini_attrs):
        """Generate launch attributes in the format supported by the client.

        :param list ini_attrs: List for attributes from the pytest.ini file
        """
        attributes = ini_attrs or []
        system_attributes = get_launch_sys_attrs()
        system_attributes['agent'] = (
            '{}-{}'.format(self.agent_name, self.agent_version))
        return attributes + _dict_to_payload(system_attributes)

    def _get_item_markers(self, item):
        """
        Get attributes of item.

        :param item: pytest.Item
        :return: list of tags
        """
        # Try to extract names of @pytest.mark.* decorators used for test item
        # and exclude those which present in rp_ignore_attributes parameter
        def get_marker_value(item, keyword):
            try:
                marker = item.get_closest_marker(keyword)
            except AttributeError:
                # pytest < 3.6
                marker = item.keywords.get(keyword)

            marker_values = []
            if marker and marker.args:
                for arg in marker.args:
                    marker_values.append("{}:{}".format(keyword, arg))
            else:
                marker_values.append(keyword)
            # returns a list of strings to accommodate multiple values
            return marker_values

        try:
            get_marker = getattr(item, "get_closest_marker")
        except AttributeError:
            get_marker = getattr(item, "get_marker")

        raw_attrs = []
        for k in item.keywords:
            if get_marker(k) is not None and k not in self.ignored_attributes:
                raw_attrs.extend(get_marker_value(item, k))
        raw_attrs.extend(item.session.config.getini('rp_tests_attributes'))
        return gen_attributes(raw_attrs)

    def _get_parameters(self, item):
        """
        Get params of item.

        :param item: Pytest.Item
        :return: dict of params
        """
        return item.callspec.params if hasattr(item, 'callspec') else None

    @staticmethod
    def _get_item_name(test_item):
        """
        Get name of item.

        :param test_item: pytest.Item
        :return: name
        """
        name = test_item._rp_name
        if len(name) > 256:
            name = name[:256]
            test_item.warn(
                PytestWarning(
                    'Test node ID was truncated to "{}" because of name size '
                    'constrains on reportportal'.format(name)
                )
            )
        return name

    @staticmethod
    def _get_item_description(test_item):
        """
        Get description of item.

        :param test_item: pytest.Item
        :return string description
        """
        if isinstance(test_item, (Class, Function, Module, Item)):
            doc = test_item.obj.__doc__
            if doc is not None:
                return trim_docstring(doc)
        if isinstance(test_item, DoctestItem):
            return test_item.reportinfo()[2]
