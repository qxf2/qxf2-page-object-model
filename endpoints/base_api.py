"""
A wrapper around Requests to make Restful API calls
"""

import asyncio
import requests
from requests.exceptions import HTTPError, RequestException

class BaseAPI:
    "Main base class for Requests based scripts"
    session_object = requests.Session()
    base_url = None

    def get(self, url, headers=None, raise_for_status=True):
        "Get request"
        headers = headers if headers else {}
        try:
            response = self.session_object.get(url=url, headers=headers)
            if raise_for_status:
                response.raise_for_status()
        except HTTPError as http_err:
            print(f"GET request failed: {http_err}")
        except ConnectionError:
            print(f"\033[1;31mFailed to connect to {url}. Check if the API server is up.\033[1;m")
        except RequestException as err:
            print(f"\033[1;31mAn error occurred: {err}\033[1;m")
        return response

    # pylint: disable=too-many-arguments
    def post(self, url,params=None, data=None, json=None, headers=None, raise_for_status=True):
        "Post request"
        headers = headers if headers else {}
        try:
            response = self.session_object.post(url,
                                                params=params,
                                                data=data,
                                                json=json,
                                                headers=headers)
            if raise_for_status:
                response.raise_for_status()
        except HTTPError as http_err:
            print(f"POST request failed: {http_err}")
        except ConnectionError:
            print(f"\033[1;31mFailed to connect to {url}. Check if the API server is up.\033[1;m")
        except RequestException as err:
            print(f"\033[1;31mAn error occurred: {err}\033[1;m")
        return response


    def delete(self, url,headers=None, raise_for_status=True):
        "Delete request"
        headers = headers if headers else {}
        try:
            response = self.session_object.delete(url, headers=headers)
            if raise_for_status:
                response.raise_for_status()
        except HTTPError as http_err:
            print(f"DELETE request failed: {http_err}")
        except ConnectionError:
            print(f"\033[1;31mFailed to connect to {url}. Check if the API server is up.\033[1;m")
        except RequestException as err:
            print(f"\033[1;31mAn error occurred: {err}\033[1;m")
        return response

    def put(self,url,json=None, headers=None, raise_for_status=True):
        "Put request"
        headers = headers if headers else {}
        try:
            response = self.session_object.put(url, json=json, headers=headers)
            if raise_for_status:
                response.raise_for_status()
        except HTTPError as http_err:
            print(f"PUT request failed: {http_err}")
        except ConnectionError:
            print(f"\033[1;31mFailed to connect to {url}. Check if the API server is up.\033[1;m")
        except RequestException as err:
            print(f"\033[1;31mAn error occurred: {err}\033[1;m")
        return response

    async def async_get(self, url, headers=None):
        "Run the blocking GET method in a thread"
        headers = headers if headers else {}
        response = await asyncio.to_thread(self.get, url, headers)
        return response

    # pylint: disable=too-many-arguments
    async def async_post(self,
                         url,
                         params=None,
                         data=None,
                         json=None,
                         headers=None):
        "Run the blocking POST method in a thread"
        headers = headers if headers else {}
        response = await asyncio.to_thread(self.post,
                                           url,
                                           params,
                                           data,
                                           json,
                                           headers)
        return response

    async def async_delete(self, url, headers=None):
        "Run the blocking DELETE method in a thread"
        headers = headers if headers else {}
        response = await asyncio.to_thread(self.delete, url, headers)
        return response

    async def async_put(self, url, json=None, headers=None):
        "Run the blocking PUT method in a thread"
        headers = headers if headers else {}
        response = await asyncio.to_thread(self.put, url, json, headers)
        return response
