"""This module contains functional for test items management.

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
from reportportal_client.helpers import generate_uuid, dict_to_payload
from reportportal_client.items.rp_log_items.rp_log_item import RPLogItem
from reportportal_client.items.rp_test_items.rp_child_test_item import \
    RPChildTestItem
from reportportal_client.items.rp_test_items.rp_root_test_item import \
    RPRootTestItem


class TestManager(object):
    """Manage test items during single launch.

    Test item types (item_type) can be:
        (SUITE, STORY, TEST, SCENARIO, STEP, BEFORE_CLASS,
        BEFORE_GROUPS, BEFORE_METHOD, BEFORE_SUITE, BEFORE_TEST, AFTER_CLASS,
        AFTER_GROUPS, AFTER_METHOD, AFTER_SUITE, AFTER_TEST).

    'attributes' and 'parameters' should be a dictionary
        with the following format:
            {
                "<key1>": "<value1>",
                "<key2>": "<value2>",
                ...
            }
    """

    def __init__(self, rp_url, session, api_version, launch_id, project_name):
        """Initialize instance attributes.

        :param rp_url:          report portal url
        :param session:         Session object
        :param api_version:     RP API version
        :param launch_id:       Parent launch UUID
        :param project_name:    RP project name
        """
        self.rp_url = rp_url
        self.session = session
        self.api_version = api_version
        self.launch_id = launch_id
        self.project_name = project_name
        self.__storage = []

    def start_test_item(self,
                        name,
                        start_time,
                        item_type,
                        description=None,
                        attributes=None,
                        parameters=None,
                        parent_item_id=None,
                        has_stats=True,
                        **kwargs):
        """Start new test item.

        :param name:            test item name
        :param start_time:      test item execution start time
        :param item_type:       test item type (see class doc string)
        :param description:     test item description
        :param attributes:      test item attributes(tags)
                                Pairs of key and value (see class doc string)
        :param parameters:      test item set of parameters
                                (for parametrized tests) (see class doc string)
        :param parent_item_id:  UUID of parent test item
        :param has_stats:       True - regular test item, False - test item
                                without statistics (nested step)
        :param kwargs:          other parameters
        :return:                test item UUID
        """
        if attributes and isinstance(attributes, dict):
            attributes = dict_to_payload(attributes)
        if parameters:
            parameters = dict_to_payload(parameters)

        item_data = {
            "description": description,
            "attributes": attributes,
            "parameters": parameters,
            "has_stats": has_stats
        }
        kwargs and item_data.update(kwargs)
        uuid = generate_uuid()
        if not parent_item_id:
            test_item = RPRootTestItem(self.rp_url,
                                       self.session,
                                       self.api_version,
                                       self.project_name,
                                       name,
                                       item_type,
                                       self.launch_id,
                                       uuid,
                                       **item_data)
            self.__storage.append(test_item)
        else:
            parent_item = self.get_test_item(parent_item_id)
            test_item = RPChildTestItem(self.rp_url,
                                        self.session,
                                        self.api_version,
                                        self.project_name,
                                        parent_item,
                                        name,
                                        item_type,
                                        self.launch_id,
                                        uuid,
                                        **item_data)
        test_item.start(start_time)
        return uuid

    def update_test_item(self, item_uuid, attributes=None, description=None,
                         **kwargs):
        """Update existing test item at the Report Portal.

        :param str item_uuid:   test item UUID returned on the item start
        :param str description: test item description
        :param dict attributes: test item attributes(tags)
                                Pairs of key and value (see class doc string)
        """
        self.get_test_item(item_uuid)
        raise NotImplementedError()

    def finish_test_item(self,
                         item_uuid,
                         end_time,
                         status,
                         issue=None,
                         attributes=None,
                         **kwargs):
        """Finish test item.

        :param item_uuid:  id of the test item
        :param end_time:   time in UTC format
        :param status:     status of the test
        :param issue:      description of an issue
        :param attributes: dict with attributes
        :param kwargs:     other parameters
        """
        # check if the test is skipped, if not - do not mark as TO INVESTIGATE
        if issue is None and status == "SKIPPED":
            issue = {"issue_type": "NOT_ISSUE"}
        if attributes and isinstance(attributes, dict):
            attributes = dict_to_payload(attributes)
        self.get_test_item(item_uuid).finish(end_time, status, issue=issue,
                                             attributes=attributes, **kwargs)

    def remove_test_item(self, item_uuid):
        """Remove test item by uuid.

        :param item_uuid: test item uuid
        """
        self.get_test_item(item_uuid)
        raise NotImplementedError()

    def log(self, time, message=None, level=None, attachment=None,
            item_id=None):
        """Log message. Can be added to test item in any state.

        :param time:        log time
        :param message:     log message
        :param level:       log level
        :param attachment:  attachments to log (images,files,etc.)
        :param item_id:     parent item UUID
        :return:            log item UUID
        """
        uuid = generate_uuid()
        # Todo: Do we store log items?
        log_item = RPLogItem(self.rp_url,
                             self.session,
                             self.api_version,
                             self.project_name,
                             self.launch_id,
                             uuid)
        log_item.create(time, attachment, item_id, level, message)
        return uuid

    def get_test_item(self, item_uuid):
        """Get test item by its uuid in the storage.

        :param item_uuid:   test item uuid
        :return:            test item object if found else None
        """
        # Todo: add 'force' parameter to get item from report portal server
        #  instead of cache and update cache data according to this request
        return self._find_item(item_uuid, self.__storage)

    def _find_item(self, item_uuid, storage):
        """Find test item by its uuid in given storage.

        :param item_uuid:   test item uuid
        :param storage:     list with test item objects
        :return:            test item object if found else None
        """
        for test_item in reversed(storage):
            if item_uuid == test_item.generated_id:
                return test_item
            else:
                if hasattr(test_item, "child_items") and test_item.child_items:
                    found_item = self._find_item(item_uuid,
                                                 test_item.child_items)
                    if found_item:
                        return found_item

    def get_storage(self):
        """Get storage.

        :return: storage with test items
        """
        return self.__storage
