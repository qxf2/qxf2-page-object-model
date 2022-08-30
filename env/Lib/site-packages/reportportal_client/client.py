"""This module contains Report Portal Client class.

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


class RPClient(object):
    """Report portal client."""

    def __init__(self, base_url, username, password, project_name, api_version,
                 **kwargs):
        """Initialize required attributes.

        :param base_url:        Base url of Report Portal
        :param username:        Username
        :param password:        Password
        :param project_name:    Name of project
        :param api_version:     Version of API
        """
        self._launch_uuid = None
        self._token = None
        self.api_version = api_version
        self.base_url = base_url
        self.password = password
        self.port = kwargs.get('port', None)
        self.project_name = project_name
        self.username = username

    @property
    def launch_uuid(self):
        """Get launch uuid."""
        return self._launch_uuid

    @property
    def token(self):
        """Get the token."""
        return self._token

    def _request(self, uri, token, **kwargs):
        """Make Rest calls with necessary params.

        :param uri:   Request URI
        :param token: Access token
        :return:      :class:`Response <Response>` object
        """

    def start_launch(self, name, start_time, **kwargs):
        """Start launch.

        :param name:        Name of launch
        :param start_time:  Launch start time
        """
        # uri = f'/api/{self.api_version}/{self.project_name}/launch'

    def start_item(self, name, start_time, item_type, parent_uuid=None,
                   **kwargs):
        """Start case/step/nested step item.

        :param name:        Name of test item
        :param start_time:  Test item start time
        :param item_type:   Type of test item
        :param parent_uuid: Parent test item UUID
        """
        # uri = f'/api/{self.api_version}/{self.project_name}/item/
        # {parent_uuid}'

    def finish_item(self, item_uuid, end_time, **kwargs):
        """Finish suite/case/step/nested step item.

        :param end_time:    Item end time
        :param item_uuid:   Item UUID
        """
        # uri = f'/api/{self.api_version}/{self.project_name}/item/{item_uuid}'

    def finish_launch(self, end_time, **kwargs):
        """Finish launch.

        :param end_time:    Launch end time
        """
        # uri = f'/api/{self.api_version}/{self.project_name}/launch' \
        #       f'/{self.launch_uuid}/finish'

    def save_log(self, log_time, **kwargs):
        """Save logs for test items.

        :param log_time:    Log time
        """
        # uri = f'/api/{self.api_version}/{self.project_name}/log'
