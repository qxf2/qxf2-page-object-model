"""
This module contains functional for Base RP items management.

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

from reportportal_client.core.rp_requests import HttpRequest
from reportportal_client.core.rp_responses import RPResponse
from reportportal_client.static.defines import NOT_FOUND


class BaseRPItem(object):
    """This model stores attributes related to RP item."""

    def __init__(self, rp_url, session, api_version, project_name,
                 launch_uuid, generated_id):
        """Initialize instance attributes.

        :param rp_url:         report portal url
        :param session:        Session object
        :param api_version:    RP API version
        :param project_name:   RP project name
        :param launch_uuid:    Parent launch UUID
        :param generated_id:   Id generated to speed up client
        """
        self.uuid = None
        self.weight = None
        self.generated_id = generated_id
        self.http_requests = []
        self.responses = []
        self.rp_url = rp_url
        self.session = session
        self.api_version = api_version
        self.project_name = project_name
        self.launch_uuid = launch_uuid

    @property
    def http_request(self):
        """Get last http request.

        :return: request object
        """
        return self.http_requests[-1] if self.http_requests else None

    @property
    def response(self):
        """Get last http response.

        :return: Response data object
        """
        return self.responses[-1] if self.responses else None

    @response.setter
    def response(self, data):
        """Set the response object for the test item.

        :param data: Response data object
        """
        response = RPResponse(data)
        self.responses.append(response)
        self.uuid = response.id if (response.id is
                                    not NOT_FOUND) else self.uuid

    @property
    def unhandled_requests(self):
        """Get list of requests that were not handled.

        :return: list of HttpRequest objects
        """
        return [request for request in self.http_requests
                if not request.response]

    def add_request(self, endpoint, method, request_class, *args, **kwargs):
        """Add new request object.

        :param endpoint:       request endpoint
        :param method:         Session object method. Allowable values: get,
                               post, put, delete
        :param request_class:  request class object
        :param args:           request object attributes
        :param kwargs:         request object named attributes
        :return: None
        """
        rp_request = request_class(*args, **kwargs)
        rp_request.http_request = HttpRequest(method, endpoint)
        rp_request.priority = self.weight
        self.http_requests.append(rp_request)
