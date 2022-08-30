"""This module contains models for the RP response objects.

Detailed information about responses wrapped up in that module
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

from reportportal_client.static.defines import NOT_FOUND
from reportportal_client.static.errors import ResponseError


class RPMessage(object):
    """Model for the message returned by RP API."""

    __slots__ = ['message', 'error_code']

    def __init__(self, data):
        """Initialize instance attributes.

        :param data: Dictionary representation of the API response
        """
        self.error_code = data.get('error_code', NOT_FOUND)
        self.message = data.get('message', NOT_FOUND)

    def __str__(self):
        """Change string representation of the class."""
        if self.error_code is NOT_FOUND:
            return self.message
        return '{error_code}: {message}'.format(error_code=self.error_code,
                                                message=self.message)

    @property
    def is_empty(self):
        """Check if returned message is empty."""
        return self.message is NOT_FOUND


class RPResponse(object):
    """Class representing RP API response."""

    __slots__ = ['_data', '_resp']

    def __init__(self, data):
        """Initialize instance attributes.

        :param data: requests.Response object
        """
        self._data = self._get_json(data)
        self._resp = data

    @staticmethod
    def _get_json(data):
        """Get response in dictionary.

        :param data: requests.Response object
        :return:     dict
        """
        if not data.text:
            return {}
        try:
            return data.json()
        except ValueError as error:
            raise ResponseError('Invalid response: {0}: {1}'
                                .format(error, data.text))

    @property
    def id(self):
        """Get value of the 'id' key."""
        return self.json.get('id', NOT_FOUND)

    @property
    def is_success(self):
        """Check if response to API has been successful."""
        return self._resp.ok

    def _iter_messages(self):
        """Generate RPMessage for each response."""
        data = self.json.get('responses', [self.json])
        for chunk in data:
            message = RPMessage(chunk)
            if not message.is_empty:
                yield message

    @property
    def json(self):
        """Get the response in dictionary."""
        return self._data

    @property
    def message(self):
        """Get value of the 'msg' key."""
        return self.json.get('msg', NOT_FOUND)

    @property
    def messages(self):
        """Get list of messages received."""
        return tuple(self._iter_messages())
