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


class Error(Exception):
    """General exception for package."""


class ResponseError(Error):
    """Error in response returned by RP."""


class EntryCreatedError(ResponseError):
    """Represents error in case no entry is created.

    No 'id' in the json response.
    """


class OperationCompletionError(ResponseError):
    """Represents error in case of operation failure.

    No 'message' in the json response.
    """
