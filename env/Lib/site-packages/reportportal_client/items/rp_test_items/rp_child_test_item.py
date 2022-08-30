"""
This module contains functional for Child RP test items management.

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

from weakref import proxy

from reportportal_client.core.rp_requests import ItemStartRequest
from reportportal_client.items.rp_test_items.rp_base_test_item import \
    RPBaseTestItem


class RPChildTestItem(RPBaseTestItem):
    """This model stores attributes for RP child test items."""

    def __init__(self, rp_url, session, api_version, project_name, parent_item,
                 item_name, item_type, launch_uuid, generated_id,
                 **kwargs):
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
        :param kwargs:        Dict of additional named parameters
        """
        super(RPChildTestItem, self).__init__(rp_url, session, api_version,
                                              project_name, item_name,
                                              item_type, launch_uuid,
                                              generated_id, **kwargs)
        self.parent_item = proxy(parent_item)
        self.parent_item.add_child_item(self)
        self.weight = self.parent_item.weight + 1

    def start(self, start_time):
        """Create request object to start child test item.

        :param start_time:    Test item start time
        """
        endpoint = "{url}/{api_version}/{project_name}/item/" \
                   "{parentItemUuid}". \
            format(url=self.rp_url, api_version=self.api_version,
                   project_name=self.project_name,
                   parentItemUuid=self.parent_item.uuid)

        self.add_request(endpoint, self.session.post, ItemStartRequest,
                         self.item_name, start_time,
                         self.item_type, self.launch_uuid,
                         attributes=self.attributes, code_ref=self.code_ref,
                         description=self.description,
                         has_stats=self.has_stats,
                         parameters=self.parameters,
                         retry=self.retry, uuid=self.uuid,
                         unique_id=self.unique_id)
