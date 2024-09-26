"""
A wrapper around Requests to make Restful API calls
"""

import asyncio
from urllib.error import HTTPError
from urllib.error import URLError
from requests.exceptions import HTTPError, RequestException, ConnectionError

class Base_API:
    "Main base class for Requests based scripts"

    def get(self, url, headers=None):
        "Get request"
        headers = headers if headers else {}
        try:
            response = self.request_obj.get(url=url, headers=headers)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f"GET request failed: {http_err}")
        except ConnectionError:
            print(f"\033[1;31mFailed to connect to {url}. Check if the API server is up.\033[1;m")
        except RequestException as err:
            print(f"\033[1;31mAn error occurred: {err}\033[1;m")
        return response  

    def post(self, url,params=None, data=None,json=None,headers=None):
        "Post request"
        headers = headers if headers else {}
        try:
            response = self.request_obj.post(url, params=params, data=data, json=json, headers=headers)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f"POST request failed: {http_err}")
        except ConnectionError:
            print(f"\033[1;31mFailed to connect to {url}. Check if the API server is up.\033[1;m")
        except RequestException as err:
            print(f"\033[1;31mAn error occurred: {err}\033[1;m")
        return response


    def delete(self, url,headers=None):
        "Delete request"
        headers = headers if headers else {}
        try:
            response = self.request_obj.delete(url, headers=headers)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f"DELETE request failed: {http_err}")
        except ConnectionError:
            print(f"\033[1;31mFailed to connect to {url}. Check if the API server is up.\033[1;m")
        except RequestException as err:
            print(f"\033[1;31mAn error occurred: {err}\033[1;m")
        return response

    def put(self,url,json=None, headers=None):
        "Put request"
        headers = headers if headers else {}
        try:
            response = self.request_obj.put(url, json=json, headers=headers)
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
