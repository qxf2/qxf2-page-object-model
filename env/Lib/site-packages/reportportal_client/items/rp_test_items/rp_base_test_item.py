"""
This module contains functional for Base RP test items management.

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

from reportportal_client.items.rp_base_item import BaseRPItem
from reportportal_client.core.rp_requests import ItemFinishRequest


class RPBaseTestItem(BaseRPItem):
    """This model stores common attributes for RP test items."""

    def __init__(self, rp_url, session, api_version, project_name, item_name,
                 item_type, launch_uuid, generated_id, **kwargs):
        """Initialize instance attributes.

        :param rp_url:        report portal url
        :param session:       Session object
        :param api_version:   RP API version
        :param project_name:  RP project name
        :param item_name:     RP item name
        :param item_type:     Type of the test item. Allowable values: "suite",
                              "story", "test", "scenario", "step",
                              "before_class", "before_groups", "before_method",
                              "before_suite", "before_test", "after_class",
                              "after_groups", "after_method", "after_suite",
                              "after_test"
        :param launch_uuid:   Parent launch UUID
        :param generated_id:  Id generated to speed up client
        :param has_stats:     If item has stats
        :param kwargs:        Dict of additional named parameters
        """
        super(RPBaseTestItem, self).__init__(rp_url, session, api_version,
                                             project_name, launch_uuid,
                                             generated_id)
        self.item_name = item_name
        self.item_type = item_type
        self.description = kwargs.get("description")
        self.attributes = kwargs.get("attributes")
        self.uuid = kwargs.get("uuid")
        self.code_ref = kwargs.get("code_ref")
        self.parameters = kwargs.get("parameters")
        self.unique_id = kwargs.get("unique_id")
        self.retry = kwargs.get("retry", False)
        self.has_stats = kwargs.get("has_stats", True)
        self.child_items = []

    def add_child_item(self, item):
        """Add new child item to the list.

        :param item:        test item object
        :return:            None
        """
        self.child_items.append(item)

    def finish(self, end_time, status=None, description=None,
               attributes=None, issue=None):
        """Form finish request for RP test item.

        :param end_time:    Test item end time
        :param status:      Test status. Allowable values: "passed",
                            "failed", "stopped", "skipped", "interrupted",
                            "cancelled"
        :param description: Test item description.
        :param attributes:  List with attributes
        :param issue:       Issue of the current test item
        """
        attributes = attributes or self.attributes
        endpoint = "{url}/api/{version}/{projectName}/item/{itemUuid}". \
            format(url=self.rp_url, version=self.api_version,
                   projectName=self.project_name, itemUuid=self.uuid)

        self.add_request(endpoint, self.session.post, ItemFinishRequest,
                         end_time, self.launch_uuid, status,
                         attributes=attributes, description=description,
                         issue=issue, retry=self.retry)
