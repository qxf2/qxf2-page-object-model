"""
This module contains functional for RP log items management.

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

from reportportal_client.core.rp_requests import RPRequestLog
from reportportal_client.items.item_weight import ItemWeight
from reportportal_client.items.rp_base_item import BaseRPItem
from reportportal_client.static.defines import RP_LOG_LEVELS


class RPLogItem(BaseRPItem):
    """This model stores attributes for RP log items."""

    def __init__(self, rp_url, session, api_version, project_name,
                 launch_uuid, generated_id):
        """Initialize instance attributes.

        :param rp_url:          report portal URL
        :param session:         Session object
        :param api_version:     RP API version
        :param project_name:    RP project name
        :param launch_uuid:     Parent launch UUID
        :param generated_id:    Id generated to speed up client
        """
        super(RPLogItem, self).__init__(rp_url, session, api_version,
                                        project_name, launch_uuid,
                                        generated_id)
        self.weight = ItemWeight.LOG_ITEM_WEIGHT

    @property
    def response(self):
        """Get the response object for RP log item."""
        return self.responses[0]

    @response.setter
    def response(self, value):
        """Set the response object for RP log item."""
        raise NotImplementedError

    def create(self, time, file_obj=None, item_uuid=None,
               level=RP_LOG_LEVELS[40000], message=None):
        """Add request for log item creation.

        :param time:        Log item time
        :param file_obj:    Object of the RPFile
        :param item_uuid:   Parent test item UUID
        :param level:       Log level. Allowable values: error(40000),
                            warn(30000), info(20000), debug(10000),
                            trace(5000), fatal(50000), unknown(60000)
        :param message:     Log message
        """
        endpoint = "/api/{version}/{projectName}/log".format(
            version=self.api_version, projectName=self.project_name)
        self.add_request(endpoint, self.session.post, RPRequestLog,
                         self.launch_uuid, time, file=file_obj,
                         item_uuid=item_uuid, level=level, message=message)
