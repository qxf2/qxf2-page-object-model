"""This module contains changed pytest for report-portal."""

# This program is free software: you can redistribute it
# and/or modify it under the terms of the GPL licence

import logging
from os import getenv
import dill as pickle
import pkg_resources
import pytest
import requests
import time

from pytest_reportportal import LAUNCH_WAIT_TIMEOUT
from reportportal_client.errors import ResponseError
from reportportal_client.helpers import gen_attributes

from .service import PyTestServiceClass
from .listener import RPReportListener

try:
    # This try/except can go away once we support pytest >= 3.3
    pkg_resources.get_distribution('pytest >= 3.3.0')
    PYTEST_HAS_LOGGING_PLUGIN = True
    try:
        # This try/except can go away once we support pytest >= 5.4.0
        from _pytest.logging import get_actual_log_level
    except ImportError:
        from _pytest.logging import get_log_level_for_setting as \
            get_actual_log_level
except pkg_resources.VersionConflict:
    PYTEST_HAS_LOGGING_PLUGIN = False

log = logging.getLogger(__name__)


def is_master(config):
    """
    Validate workerinput attribute.

    True if the code running the given pytest.config object
    is running in a xdist master node or not running xdist at all.
    """
    return not hasattr(config, 'workerinput')


@pytest.mark.optionalhook
def pytest_configure_node(node):
    """
    Configure node of tests.

    :param node: _pytest.nodes.Node
    :return: pickle of RPService
    """
    if node.config._reportportal_configured is False:
        # Stop now if the plugin is not properly configured
        return
    node.workerinput['py_test_service'] = pickle.dumps(
            node.config.py_test_service)


def pytest_sessionstart(session):
    """
    Start test session.

    :param session: Session
    :return: None
    """
    if session.config._reportportal_configured is False:
        # Stop now if the plugin is not properly configured
        return
    if is_master(session.config):
        try:
            session.config.py_test_service.init_service(
                project=session.config.getini('rp_project'),
                endpoint=session.config.getini('rp_endpoint'),
                uuid=getenv('RP_UUID') or session.config.getini('rp_uuid'),
                log_batch_size=int(session.config.getini('rp_log_batch_size')),
                ignore_errors=bool(session.config.getini('rp_ignore_errors')),
                custom_launch=session.config.option.rp_launch_id or None,
                ignored_attributes=session.config.getini(
                    'rp_ignore_attributes'),
                verify_ssl=session.config.getini('rp_verify_ssl'),
                retries=int(session.config.getini('retries')),
                parent_item_id=session.config.option.rp_parent_item_id or None,
            )
        except ResponseError as response_error:
            log.warning('Failed to initialize reportportal-client service. '
                        'Reporting is disabled.')
            log.debug(str(response_error))
            session.config.py_test_service.rp = None
            return

        attributes = gen_attributes(
            session.config.getini('rp_launch_attributes'))
        if not session.config.option.rp_launch_id:
            session.config.py_test_service.start_launch(
                session.config.option.rp_launch,
                attributes=attributes,
                description=session.config.option.rp_launch_description,
                rerun=session.config.option.rp_rerun,
                rerun_of=session.config.option.rp_rerun_of
            )
            if session.config.pluginmanager.hasplugin('xdist'):
                wait_launch(session.config.py_test_service.rp)


def pytest_collection_finish(session):
    """
    Collect tests if session is configured.

    :param session: pytest.Session
    :return: None
    """
    if session.config._reportportal_configured is False:
        # Stop now if the plugin is not properly configured
        return

    session.config.py_test_service.collect_tests(session)


def wait_launch(rp_client):
    """
    Wait for initialize RP_Service.

    :param rp_client: RP_Service
    :return: None
    """
    timeout = time.time() + LAUNCH_WAIT_TIMEOUT
    while not rp_client.launch_id:
        if time.time() > timeout:
            raise Exception("Launch not found")
        time.sleep(1)


def pytest_sessionfinish(session):
    """
    Finish session if has attr  'workerinput'.

    :param session: pytest.Session
    :return: None
    """
    if session.config._reportportal_configured is False:
        # Stop now if the plugin is not properly configured
        return

    if is_master(session.config):
        if not session.config.option.rp_launch_id:
            session.config.py_test_service.finish_launch()


def pytest_configure(config):
    """
    Configure RPReportListener for send logs.

    :param config: Config file
    :return:  None
    """
    if config.getoption('--collect-only', default=False) or \
            config.getoption('--setup-plan', default=False) or \
            not config.option.rp_enabled:
        config._reportportal_configured = False
        return

    project = config.getini('rp_project')
    endpoint = config.getini('rp_endpoint')
    uuid = getenv('RP_UUID') or config.getini('rp_uuid')
    ignore_errors = config.getini('rp_ignore_errors')
    config._reportportal_configured = all([project, endpoint, uuid])

    if config._reportportal_configured and ignore_errors:
        try:
            verify_ssl = config.getini('rp_verify_ssl')
            r = requests.get(
                '{0}/api/v1/project/{1}'.format(endpoint, project),
                headers={
                    'Authorization': 'bearer {0}'.format(uuid)
                },
                verify=verify_ssl
            )
            r.raise_for_status()
        except requests.exceptions.RequestException as exc:
            log.exception(exc)
            config._reportportal_configured = False

    if config._reportportal_configured is False:
        return

    if not config.option.rp_launch:
        config.option.rp_launch = config.getini('rp_launch')

    if not config.option.rp_launch_description:
        config.option.rp_launch_description = config.\
            getini('rp_launch_description')
    if not config.option.rp_launch_id:
        config.option.rp_launch_id = config.getini('rp_launch_id')

    if not config.option.rp_rerun_of:
        config.option.rp_rerun_of = config.getini('rp_rerun_of')
    if config.option.rp_rerun_of:
        config.option.rp_rerun = True
    else:
        if not config.option.rp_rerun:
            config.option.rp_rerun = config.getini('rp_rerun')

    if not config.option.rp_parent_item_id:
        config.option.rp_parent_item_id = config.getini('rp_parent_item_id')
    if not config.option.rp_launch_id:
        config.option.rp_launch_id = config.getini('rp_launch_id')

    if is_master(config):
        config.py_test_service = PyTestServiceClass()
    else:
        config.py_test_service = pickle.loads(config.
                                              workerinput['py_test_service'])

    # set Pytest_Reporter and configure it
    if PYTEST_HAS_LOGGING_PLUGIN:
        # This check can go away once we support pytest >= 3.3
        log_level = get_actual_log_level(config, 'rp_log_level')
        if log_level is None:
            log_level = logging.NOTSET
    else:
        log_level = logging.NOTSET

    config._reporter = RPReportListener(config.py_test_service,
                                        log_level=log_level,
                                        endpoint=endpoint)

    if hasattr(config, '_reporter'):
        config.pluginmanager.register(config._reporter)


def pytest_unconfigure(config):
    """
    Clear config from reporter.

    :param config: Config file
    :return: None
    """
    if config._reportportal_configured is False:
        # Stop now if the plugin is not properly configured
        return

    if hasattr(config, '_reporter'):
        reporter = config._reporter
        del config._reporter
        config.pluginmanager.unregister(reporter)
        log.debug('RP is unconfigured')


def pytest_addoption(parser):
    """
    Add parameter in config of reporter.

    :param parser: Config
    :return:  None
    """
    group = parser.getgroup('reporting')
    group.addoption(
        '--rp-launch',
        action='store',
        dest='rp_launch',
        help='Launch name (overrides rp_launch config option)')
    group.addoption(
        '--rp-launch-id',
        action='store',
        dest='rp_launch_id',
        help='Use already existing launch-id. The plugin won\'t control the '
             'Launch status (overrides rp_launch_id config option)')
    group.addoption(
        '--rp-launch-description',
        action='store',
        dest='rp_launch_description',
        help='Launch description (overrides '
             'rp_launch_description config option)')
    group.addoption(
        '--rp-rerun',
        action='store_true',
        dest='rp_rerun',
        help='Marks the launch as the rerun')
    group.addoption(
        '--rp-rerun-of',
        action='store',
        dest='rp_rerun_of',
        help='ID of the launch to be marked as a rerun '
             '(use only with rp_rerun=True)')
    group.addoption(
        '--rp-parent-item-id',
        action='store',
        dest='rp_parent_item_id',
        help="Create all test item as child items of the given "
             "(already existing) item.")

    group.addoption(
        '--reportportal',
        action='store_true',
        dest='rp_enabled',
        default=False,
        help='Enable ReportPortal plugin'
    )

    if PYTEST_HAS_LOGGING_PLUGIN:
        group.addoption(
            '--rp-log-level',
            dest='rp_log_level',
            default=None,
            help='Logging level for automated log records reporting'
        )
        parser.addini(
            'rp_log_level',
            default=None,
            help='Logging level for automated log records reporting'
        )

    parser.addini(
        'rp_uuid',
        help='UUID')

    parser.addini(
        'rp_endpoint',
        help='Server endpoint')

    parser.addini(
        'rp_project',
        help='Project name')

    parser.addini(
        'rp_launch',
        default='Pytest Launch',
        help='Launch name')

    parser.addini(
        'rp_launch_id',
        default=None,
        help='Use already existing launch-id. The plugin won\'t control '
             'the Launch status')

    parser.addini(
        'rp_launch_attributes',
        type='args',
        help='Launch attributes, i.e Performance Regression')

    parser.addini(
        'rp_tests_attributes',
        type='args',
        help='Attributes for all tests items, e.g. Smoke')

    parser.addini(
        'rp_launch_description',
        default='',
        help='Launch description')

    parser.addini(
        'rp_log_batch_size',
        default='20',
        help='Size of batch log requests in async mode')

    parser.addini(
        'rp_ignore_errors',
        default=False,
        type='bool',
        help='Ignore Report Portal errors (exit otherwise)')

    parser.addini(
        'rp_ignore_attributes',
        type='args',
        help='Ignore specified pytest markers, i.e parametrize')

    parser.addini(
        'rp_hierarchy_dirs_level',
        default=0,
        help='Directory starting hierarchy level')

    parser.addini(
        'rp_hierarchy_dirs',
        default=False,
        type='bool',
        help='Enables hierarchy for directories')

    parser.addini(
        'rp_hierarchy_module',
        default=True,
        type='bool',
        help='Enables hierarchy for module')

    parser.addini(
        'rp_hierarchy_class',
        default=True,
        type='bool',
        help='Enables hierarchy for class')

    parser.addini(
        'rp_hierarchy_parametrize',
        default=False,
        type='bool',
        help='Enables hierarchy for parametrized tests')

    parser.addini(
        'rp_issue_marks',
        type='args',
        default='',
        help='Pytest marks to get issue information')

    parser.addini(
        'rp_issue_system_url',
        default='',
        help='URL to get issue description. Issue id '
             'from pytest mark will be added to this URL')

    parser.addini(
        'rp_verify_ssl',
        default=True,
        type='bool',
        help='Verify HTTPS calls')

    parser.addini(
        'rp_display_suite_test_file',
        default=True,
        type='bool',
        help="In case of True, include the suite's relative"
             " file path in the launch name as a convention of "
             "'<RELATIVE_FILE_PATH>::<SUITE_NAME>'. "
             "In case of False, set the launch name to be the suite name "
             "only - this flag is relevant only when"
             " 'rp_hierarchy_module' flag is set to False")

    parser.addini(
        'rp_issue_id_marks',
        type='bool',
        default=True,
        help='Adding tag with issue id to the test')

    parser.addini(
        'rp_parent_item_id',
        default=None,
        help="Create all test item as child items of the given "
             "(already existing) item.")

    parser.addini(
        'retries',
        default='0',
        help='Amount of retries for performing REST calls to RP server')

    parser.addini(
        'rp_rerun',
        default=False,
        help='Marks the launch as the rerun')

    parser.addini(
        'rp_rerun_of',
        default='',
        help='ID of the launch to be marked as a rerun '
             '(use only with rp_rerun=True)')
