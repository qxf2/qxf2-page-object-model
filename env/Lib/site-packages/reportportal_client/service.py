"""
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
from time import sleep

import requests
import uuid
import logging

import six
from six.moves.collections_abc import Mapping
from requests.adapters import HTTPAdapter

from .errors import ResponseError, EntryCreatedError, OperationCompletionError
from .helpers import verify_value_length

POST_LOGBATCH_RETRY_COUNT = 10
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def _convert_string(value):
    """Support and convert strings in py2 and py3.

    :param value: input string
    :return value: convert string
    """
    if isinstance(value, six.text_type):
        # Don't try to encode 'unicode' in Python 2.
        return value
    return str(value)


def _dict_to_payload(dictionary):
    """Convert dict to list of dicts.

    :param dictionary: initial dict
    :return list: list of dicts
    """
    system = dictionary.pop("system", False)
    return [
        {"key": key, "value": _convert_string(value), "system": system}
        for key, value in sorted(dictionary.items())
    ]


def _get_id(response):
    """Get id from Response.

    :param response: Response object
    :return id: int value of id
    """
    try:
        return _get_data(response)["id"]
    except KeyError:
        raise EntryCreatedError(
            "No 'id' in response: {0}".format(response.text))


def _get_msg(response):
    """
    Get message from Response.

    :param response: Response object
    :return: data: json data
    """
    try:
        return _get_data(response)
    except KeyError:
        raise OperationCompletionError(
            "No 'message' in response: {0}".format(response.text))


def _get_data(response):
    """
    Get data from Response.

    :param response: Response object
    :return: json data
    """
    data = _get_json(response)
    error_messages = _get_messages(data)
    error_count = len(error_messages)

    if error_count == 1:
        raise ResponseError(error_messages[0])
    elif error_count > 1:
        raise ResponseError(
            "\n  - ".join(["Multiple errors:"] + error_messages))
    elif not response.ok:
        response.raise_for_status()
    elif not data:
        raise ResponseError("Empty response")
    else:
        return data


def _get_json(response):
    """
    Get json from Response.

    :param response: Response object
    :return: data: json object
    """
    try:
        if response.text:
            return response.json()
        else:
            return {}
    except ValueError as value_error:
        raise ResponseError(
            "Invalid response: {0}: {1}".format(value_error, response.text))


def _get_messages(data):
    """
    Get messages (ErrorCode) from Response.

    :param data: dict of datas
    :return list: Empty list or list of errors
    """
    error_messages = []
    for ret in data.get("responses", [data]):
        if "errorCode" in ret:
            error_messages.append(
                "{0}: {1}".format(ret["errorCode"], ret.get("message"))
            )

    return error_messages


def uri_join(*uri_parts):
    """Join uri parts.

    Avoiding usage of urlparse.urljoin and os.path.join
    as it does not clearly join parts.

    Args:
        *uri_parts: tuple of values for join, can contain back and forward
                    slashes (will be stripped up).

    Returns:
        An uri string.

    """
    return '/'.join(str(s).strip('/').strip('\\') for s in uri_parts)


class ReportPortalService(object):
    """Service class with report portal event callbacks."""

    def __init__(self,
                 endpoint,
                 project,
                 token,
                 log_batch_size=20,
                 is_skipped_an_issue=True,
                 verify_ssl=True,
                 retries=None,
                 max_pool_size=50,
                 **kwargs):
        """Init the service class.

        Args:
            endpoint: endpoint of report portal service.
            project: project name to use for launch names.
            token: authorization token.
            log_batch_size: option to set the maximum number of logs
                            that can be processed in one batch
            is_skipped_an_issue: option to mark skipped tests as not
                'To Investigate' items on Server side.
            verify_ssl: option to not verify ssl certificates
            max_pool_size: option to set the maximum number of
                           connections to save in the pool.

        """
        self._batch_logs = []
        self.endpoint = endpoint
        self.log_batch_size = log_batch_size
        self.project = project
        self.token = token
        self.is_skipped_an_issue = is_skipped_an_issue
        self.base_url_v1 = uri_join(self.endpoint, "api/v1", self.project)
        self.base_url_v2 = uri_join(self.endpoint, "api/v2", self.project)

        self.session = requests.Session()
        if retries:
            self.session.mount('https://', HTTPAdapter(
                max_retries=retries, pool_maxsize=max_pool_size))
            self.session.mount('http://', HTTPAdapter(
                max_retries=retries, pool_maxsize=max_pool_size))
        self.session.headers["Authorization"] = "bearer {0}".format(self.token)
        self.launch_id = kwargs.get('launch_id')
        self.verify_ssl = verify_ssl

    def terminate(self, *args, **kwargs):
        """Call this to terminate the service."""
        pass

    def start_launch(self,
                     name,
                     start_time,
                     description=None,
                     attributes=None,
                     mode=None,
                     rerun=False,
                     rerunOf=None,
                     **kwargs):
        """Start a new launch with the given parameters."""
        if attributes and isinstance(attributes, dict):
            attributes = _dict_to_payload(attributes)
        data = {
            "name": name,
            "description": description,
            "attributes": verify_value_length(attributes),
            "startTime": start_time,
            "mode": mode,
            "rerun": rerun,
            "rerunOf": rerunOf
        }
        url = uri_join(self.base_url_v2, "launch")
        r = self.session.post(url=url, json=data, verify=self.verify_ssl)
        self.launch_id = _get_id(r)
        logger.debug("start_launch - ID: %s", self.launch_id)
        return self.launch_id

    def finish_launch(self, end_time, status=None, attributes=None, **kwargs):
        """Finish a launch with the given parameters.

        Status can be one of the followings:
        (PASSED, FAILED, STOPPED, SKIPPED, RESETED, CANCELLED)
        """
        # process log batches firstly:
        if self._batch_logs:
            self._log_batch(None, force=True)
        if attributes and isinstance(attributes, dict):
            attributes = _dict_to_payload(attributes)
        data = {
            "endTime": end_time,
            "status": status,
            "attributes": verify_value_length(attributes)
        }
        url = uri_join(self.base_url_v2, "launch", self.launch_id, "finish")
        r = self.session.put(url=url, json=data, verify=self.verify_ssl)
        logger.debug("finish_launch - ID: %s", self.launch_id)
        return _get_msg(r)

    def get_launch_info(self, max_retries=5):
        """Get the current launch information.

        Perform "max_retries" attempts to get current launch information
        with 0.5 second sleep between them.

        :param int max_retries: Number of retries to get launch information.
        :return dict: launch information
        """
        if self.launch_id is None:
            return {}

        url = uri_join(self.base_url_v1, "launch/uuid", self.launch_id)

        for _ in range(max_retries):
            logger.debug("get_launch_info - ID: %s", self.launch_id)
            resp = self.session.get(url=url, verify=self.verify_ssl)

            if resp.status_code == 200:
                launch_info = _get_json(resp)
                logger.debug("get_launch_info - Launch info: %s", launch_info)
                break

            logger.debug("get_launch_info - Launch info: Response code %s\n%s",
                         resp.status_code, resp.text)
            sleep(0.5)
        else:
            logger.warning("get_launch_info - Launch info: "
                           "Failed to fetch launch ID from the API.")
            launch_info = {}

        return launch_info

    def get_launch_ui_id(self, max_retries=5):
        """Get UI ID of the current launch.

        :return str: UI ID of the given launch.
                     None if UI ID has not been found.
        """
        return self.get_launch_info(max_retries=max_retries).get("id")

    def get_launch_ui_url(self, max_retries=5):
        """Get UI URL of the current launch.

        If UI ID can`t be found after max_retries, return URL of all launches.

        :return str: launch URL or all launches URL.
        """
        ui_id = self.get_launch_ui_id(max_retries=max_retries) or ""
        path = "ui/#{0}/launches/all/{1}".format(self.project, ui_id)
        url = uri_join(self.endpoint, path)
        logger.debug("get_launch_ui_url - ID: %s", self.launch_id)
        return url

    def start_test_item(self,
                        name,
                        start_time,
                        item_type,
                        description=None,
                        attributes=None,
                        parameters=None,
                        parent_item_id=None,
                        has_stats=True,
                        code_ref=None,
                        test_case_id=None,
                        **kwargs):
        """
        Item_type can be.

        (SUITE, STORY, TEST, SCENARIO, STEP, BEFORE_CLASS,
        BEFORE_GROUPS, BEFORE_METHOD, BEFORE_SUITE, BEFORE_TEST, AFTER_CLASS,
        AFTER_GROUPS, AFTER_METHOD, AFTER_SUITE, AFTER_TEST).

        attributes and parameters should be a dictionary
        with the following format:
            {
                "<key1>": "<value1>",
                "<key2>": "<value2>",
                ...
            }
        """
        if attributes and isinstance(attributes, dict):
            attributes = _dict_to_payload(attributes)
        if parameters:
            parameters = _dict_to_payload(parameters)

        data = {
            "name": name,
            "description": description,
            "attributes": verify_value_length(attributes),
            "startTime": start_time,
            "launchUuid": self.launch_id,
            "type": item_type,
            "parameters": parameters,
            "hasStats": has_stats,
            "codeRef": code_ref,
            "testCaseId": test_case_id,
        }
        if parent_item_id:
            url = uri_join(self.base_url_v2, "item", parent_item_id)
        else:
            url = uri_join(self.base_url_v2, "item")
        r = self.session.post(url=url, json=data, verify=self.verify_ssl)

        item_id = _get_id(r)
        logger.debug("start_test_item - ID: %s", item_id)
        return item_id

    def update_test_item(self, item_uuid, attributes=None, description=None):
        """Update existing test item at the Report Portal.

        :param str item_uuid:   Test item UUID returned on the item start
        :param str description: Test item description
        :param list attributes: Test item attributes
                                [{'key': 'k_name', 'value': 'k_value'}, ...]
        """
        data = {
            "description": description,
            "attributes": verify_value_length(attributes),
        }
        item_id = self.get_item_id_by_uuid(item_uuid)
        url = uri_join(self.base_url_v1, "item", item_id, "update")
        r = self.session.put(url=url, json=data, verify=self.verify_ssl)
        logger.debug("update_test_item - Item: %s", item_id)
        return _get_msg(r)

    def finish_test_item(self,
                         item_id,
                         end_time,
                         status,
                         issue=None,
                         attributes=None,
                         **kwargs):
        """Finish the test item and return HTTP response.

        :param item_id:    id of the test item
        :param end_time:   time in UTC format
        :param status:     status of the test
        :param issue:      description of an issue
        :param attributes: list of attributes
        :param kwargs:     other parameters
        :return:           json message

        """
        # check if skipped test should not be marked as "TO INVESTIGATE"
        if issue is None and status == "SKIPPED" \
                and not self.is_skipped_an_issue:
            issue = {"issue_type": "NOT_ISSUE"}

        if attributes and isinstance(attributes, dict):
            attributes = _dict_to_payload(attributes)

        data = {
            "endTime": end_time,
            "status": status,
            "issue": issue,
            "launchUuid": self.launch_id,
            "attributes": verify_value_length(attributes)
        }
        url = uri_join(self.base_url_v2, "item", item_id)
        r = self.session.put(url=url, json=data, verify=self.verify_ssl)
        logger.debug("finish_test_item - ID: %s", item_id)
        return _get_msg(r)

    def get_item_id_by_uuid(self, uuid):
        """Get test item ID by the given UUID.

        :param str uuid: UUID returned on the item start
        :return str:     Test item id
        """
        url = uri_join(self.base_url_v1, "item", "uuid", uuid)
        return _get_json(self.session.get(
            url=url, verify=self.verify_ssl))["id"]

    def get_project_settings(self):
        """
        Get settings from project.

        :return: json body
        """
        url = uri_join(self.base_url_v1, "settings")
        r = self.session.get(url=url, json={}, verify=self.verify_ssl)
        logger.debug("settings")
        return _get_json(r)

    def log(self, time, message, level=None, attachment=None, item_id=None):
        """
        Create log for test.

        :param time: time in UTC
        :param message: description
        :param level:
        :param attachment: files
        :param item_id:  id of item
        :return: id of item from response
        """
        data = {
            "launchUuid": self.launch_id,
            "time": time,
            "message": message,
            "level": level,
        }
        if item_id:
            data["itemUuid"] = item_id
        if attachment:
            data["attachment"] = attachment
        return self._log_batch(data)

    def _log_batch(self, log_data, force=False):
        """
        Log batch of messages with attachment.

        Args:
        log_data: log record that needs to be processed.
            log record is a dict of;
                time, message, level, attachment
                attachment is a dict of:
                    name: name of attachment
                    data: fileobj or content
                    mime: content type for attachment
        item_id: UUID of the test item that owns log_data
        force:   Flag that forces client to process all the logs
                 stored in self._batch_logs immediately
        """
        if log_data:
            self._batch_logs.append(log_data)

        if len(self._batch_logs) < self.log_batch_size and not force:
            return

        url = uri_join(self.base_url_v2, "log")
        attachments = []
        for log_item in self._batch_logs:
            log_item["launchUuid"] = self.launch_id
            attachment = log_item.pop("attachment", None)
            if attachment:
                if not isinstance(attachment, Mapping):
                    attachment = {"data": attachment}

                name = attachment.get("name", str(uuid.uuid4()))
                log_item["file"] = {"name": name}
                attachments.append(("file", (
                    name,
                    attachment["data"],
                    attachment.get("mime", "application/octet-stream")
                )))

        files = [(
            "json_request_part", (
                None,
                json.dumps(self._batch_logs),
                "application/json"
            )
        )]
        files.extend(attachments)
        for i in range(POST_LOGBATCH_RETRY_COUNT):
            try:
                r = self.session.post(
                    url=url,
                    files=files,
                    verify=self.verify_ssl
                )
                logger.debug("log_batch response: %s", r.text)
                self._batch_logs = []
                return _get_data(r)
            except KeyError:
                if i + 1 == POST_LOGBATCH_RETRY_COUNT:
                    raise
