"""This module includes classes representing RP API requests.

Detailed information about requests wrapped up in that module
can be found by the following link:
https://github.com/reportportal/documentation/blob/master/src/md/src/DevGuides/reporting.md

Copyright (c) 2018 http://reportportal.io .

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import json
import uuid

from reportportal_client.core.rp_file import RPFile
from reportportal_client.core.rp_issues import Issue
from reportportal_client.static.abstract import (
    AbstractBaseClass,
    abstractmethod
)
from reportportal_client.static.defines import DEFAULT_PRIORITY, RP_LOG_LEVELS

from .rp_responses import RPResponse


class HttpRequest:
    """This model stores attributes related to RP HTTP requests."""

    def __init__(self, session_method, url, data=None, json=None):
        """Initialize instance attributes.

        :param session_method: Method of the requests.Session instance
        :param url:            Request URL
        :param data:           Dictionary, list of tuples, bytes, or file-like
                               object to send in the body of the request
        :param json:           JSON to be send in the body of the request
        """
        self.data = data
        self.json = json
        self.session_method = session_method
        self.url = url

    def make(self):
        """Make HTTP request to the Report Portal API."""
        return RPResponse(self.session_method(
            self.url, data=self.data, json=self.json))


class RPRequestBase(object):
    """Base class for the rest of the RP request models."""

    __metaclass__ = AbstractBaseClass

    def __init__(self):
        """Initialize instance attributes."""
        self._http_request = None
        self._priority = DEFAULT_PRIORITY
        self._response = None

    def __lt__(self, other):
        """Priority protocol for the PriorityQueue."""
        return self.priority < other.priority

    @property
    def http_request(self):
        """Get the HttpRequest object of the request."""
        return self._http_request

    @http_request.setter
    def http_request(self, value):
        """Set the HttpRequest object of the request."""
        self._http_request = value

    @property
    def priority(self):
        """Get the priority of the request."""
        return self._priority

    @priority.setter
    def priority(self, value):
        """Set the priority of the request."""
        self._priority = value

    @property
    def response(self):
        """Get the response object for the request."""
        return self._response

    @response.setter
    def response(self, value):
        """Set the response object for the request."""
        self._response = value

    @abstractmethod
    def payload(self):
        """Abstract interface for getting HTTP request payload."""
        raise NotImplementedError('Payload interface is not implemented!')


class LaunchStartRequest(RPRequestBase):
    """RP start launch request model.

    https://github.com/reportportal/documentation/blob/master/src/md/src/DevGuides/reporting.md#start-launch
    """

    def __init__(self,
                 name,
                 start_time,
                 attributes=None,
                 description=None,
                 mode='default',
                 rerun=False,
                 rerun_of=None,
                 uuid=None):
        """Initialize instance attributes.

        :param name:        Name of the launch
        :param start_time:	Launch start time
        :param attributes:  Launch attributes
        :param description: Description of the launch
        :param mode:        Launch mode. Allowable values 'default' or 'debug'
        :param rerun:       Rerun mode. Allowable values 'True' of 'False'
        :param rerun_of:    Rerun mode. Specifies launch to be re-runned. Uses
                            with the 'rerun' attribute.
        :param uuid:        Launch uuid (string identifier)
        """
        super(LaunchStartRequest, self).__init__()
        self.attributes = attributes
        self.description = description
        self.mode = mode
        self.name = name
        self.rerun = rerun
        self.rerun_of = rerun_of
        self.start_time = start_time
        self.uuid = uuid

    @property
    def payload(self):
        """Get HTTP payload for the request."""
        return {
            'attributes': self.attributes,
            'description': self.description,
            'mode': self.mode,
            'name': self.name,
            'rerun': self.rerun,
            'rerunOf': self.rerun_of,
            'startTime': self.start_time,
            'uuid': self.uuid
        }


class LaunchFinishRequest(RPRequestBase):
    """RP finish launch request model.

    https://github.com/reportportal/documentation/blob/master/src/md/src/DevGuides/reporting.md#finish-launch
    """

    def __init__(self,
                 end_time,
                 status=None,
                 attributes=None,
                 description=None):
        """Initialize instance attributes.

        :param end_time:    Launch end time
        :param status:      Launch status. Allowable values: "passed",
                            "failed", "stopped", "skipped", "interrupted",
                            "cancelled"
        :param attributes:  Launch attributes(tags). Pairs of key and value.
                            Overrides attributes on start
        :param description: Launch description. Overrides description on start
        """
        super(LaunchFinishRequest, self).__init__()
        self.attributes = attributes
        self.description = description
        self.end_time = end_time
        self.status = status

    @property
    def payload(self):
        """Get HTTP payload for the request."""
        return {
            'attributes': self.attributes,
            'description': self.description,
            'endTime': self.end_time,
            'status': self.status
        }


class ItemStartRequest(RPRequestBase):
    """RP start test item request model.

    https://github.com/reportportal/documentation/blob/master/src/md/src/DevGuides/reporting.md#start-rootsuite-item
    """

    def __init__(self,
                 name,
                 start_time,
                 type_,
                 launch_uuid,
                 attributes=None,
                 code_ref=None,
                 description=None,
                 has_stats=True,
                 parameters=None,
                 retry=False,
                 uuid=None,
                 unique_id=None):
        """Initialize instance attributes.

        :param name:        Name of the test item
        :param start_time:  Test item start time
        :param type_:       Type of the test item. Allowable values: "suite",
                            "story", "test", "scenario", "step",
                            "before_class", "before_groups", "before_method",
                            "before_suite", "before_test", "after_class",
                            "after_groups", "after_method", "after_suite",
                            "after_test"
        :param launch_uuid: Parent launch UUID
        :param attributes:  Test item attributes
        :param code_ref:    Physical location of the test item
        :param description: Test item description
        :param has_stats:   Set to False if test item is nested step
        :param parameters:  Set of parameters (for parametrized test items)
        :param retry:       Used to report retry of the test. Allowable values:
                            "True" or "False"
        :param uuid:        Test item UUID (auto generated)
        :param unique_id:   Test item ID (auto generated)
        """
        super(ItemStartRequest, self).__init__()
        self.attributes = attributes
        self.code_ref = code_ref
        self.description = description
        self.has_stats = has_stats
        self.launch_uuid = launch_uuid
        self.name = name
        self.parameters = parameters
        self.retry = retry
        self.start_time = start_time
        self.type_ = type_
        self.uuid = uuid
        self.unique_id = unique_id

    @property
    def payload(self):
        """Get HTTP payload for the request."""
        return {
            'attributes': self.attributes,
            'codeRef': self.code_ref,
            'description': self.description,
            'hasStats': self.has_stats,
            'launchUuid': self.launch_uuid,
            'name': self.name,
            'parameters': self.parameters,
            'retry': self.retry,
            'startTime': self.start_time,
            'type': self.type_,
        }


class ItemFinishRequest(RPRequestBase):
    """RP finish test item request model.

    https://github.com/reportportal/documentation/blob/master/src/md/src/DevGuides/reporting.md#finish-child-item
    """

    def __init__(self,
                 end_time,
                 launch_uuid,
                 status,
                 attributes=None,
                 description=None,
                 issue=None,
                 retry=False):
        """Initialize instance attributes.

        :param end_time:    Test item end time
        :param launch_uuid: Parent launch UUID
        :param status:      Test status. Allowable values: "passed",
                            "failed", "stopped", "skipped", "interrupted",
                            "cancelled"
        :param attributes:  Test item attributes(tags). Pairs of key and value.
                            Overrides attributes on start
        :param description: Test item description. Overrides description
                            from start request.
        :param issue:       Issue of the current test item
        :param retry:       Used to report retry of the test. Allowable values:
                           "True" or "False"
        """
        super(ItemFinishRequest, self).__init__()
        self.attributes = attributes
        self.description = description
        self.end_time = end_time
        self.issue = issue  # type: Issue
        self.launch_uuid = launch_uuid
        self.status = status
        self.retry = retry

    @property
    def payload(self):
        """Get HTTP payload for the request."""
        return {
            'attributes': self.attributes,
            'description': self.description,
            'endTime': self.end_time,
            'issue': self.issue.payload,
            'launch_uuid': self.launch_uuid,
            'status': self.status,
            'retry': self.retry
        }


class RPRequestLog(RPRequestBase):
    """RP log save request model.

    https://github.com/reportportal/documentation/blob/master/src/md/src/DevGuides/reporting.md#save-single-log-without-attachment
    """

    def __init__(self,
                 launch_uuid,
                 time,
                 file=None,
                 item_uuid=None,
                 level=RP_LOG_LEVELS[40000],
                 message=None):
        """Initialize instance attributes.

        :param launch_uuid: Launch UUID
        :param time:        Log time
        :param file:        Object of the RPFile
        :param item_uuid:   Test item UUID
        :param level:       Log level. Allowable values: error(40000),
                            warn(30000), info(20000), debug(10000),
                            trace(5000), fatal(50000), unknown(60000)
        :param message:     Log message
        """
        super(RPRequestLog, self).__init__()
        self.file = file  # type: RPFile
        self.launch_uuid = launch_uuid
        self.level = level
        self.message = message
        self.time = time
        self.item_uuid = item_uuid

    def __file(self):
        """Form file payload part of the payload."""
        if not self.file:
            return {}
        return {'file': {'name': self.file.name}}

    @property
    def payload(self):
        """Get HTTP payload for the request."""
        payload = {
            'launchUuid': self.launch_uuid,
            'level': self.level,
            'message': self.message,
            'time': self.time,
            'itemUuid': self.item_uuid
        }
        return payload.update(self.__file())


class RPLogBatch(RPRequestBase):
    """RP log save batches with attachments request model.

    https://github.com/reportportal/documentation/blob/master/src/md/src/DevGuides/reporting.md#batch-save-logs
    """

    def __init__(self, log_reqs):
        """Initialize instance attributes.

        :param log_reqs:
        """
        super(RPLogBatch, self).__init__()
        self.default_content = 'application/octet-stream'
        self.log_reqs = log_reqs

    def __get_file(self, rp_file):
        """Form a tuple for the single file."""
        return ('file', (rp_file.name or uuid.uuid4(),
                         rp_file.content,
                         rp_file.content_type or self.default_content))

    def __get_files(self):
        """Get list of files for the JSON body."""
        files = []
        for req in self.log_reqs:
            if req.file:
                files.append(self.__get_file(req.file))
        return files

    def __get_request_part(self):
        r"""Form JSON body for the request.

        Example:
        [('json_request_part',
          (None,
           '[{"launchUuid": "bf6edb74-b092-4b32-993a-29967904a5b4",
              "time": "1588936537081",
              "message": "Html report",
              "level": "INFO",
              "itemUuid": "d9dc2514-2c78-4c4f-9369-ee4bca4c78f8",
              "file": {"name": "Detailed report"}}]',
           'application/json')),
         ('file',
          ('Detailed report',
           '<html lang="utf-8">\n<body><p>Paragraph</p></body></html>',
           'text/html'))]
        """
        return [(
            'json_request_part', (
                None,
                json.dumps([log.payload for log in self.log_reqs]),
                'application/json'
            )
        )].extend(self.__get_files())

    @property
    def payload(self):
        """Get HTTP payload for the request."""
        return self.__get_request_part()
