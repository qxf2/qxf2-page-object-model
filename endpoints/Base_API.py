"""
A wrapper around Requests to make Restful API calls
"""

import asyncio
from urllib.error import HTTPError
from urllib.error import URLError

class Base_API:
    "Main base class for Requests based scripts"

    def get(self, url, headers=None):
        "Get request"
        json_response = None
        error = {}
        headers = headers if headers else {}
        try:
            response = self.request_obj.get(url=url,headers=headers)
            try:
                json_response = response.json()
            except:
                json_response = None
        except (HTTPError,URLError) as e:
            error = e
            if isinstance(e,HTTPError):
                error_message = e.read()
                print("\n******\nGET Error: %s %s" %
                    (url, error_message))
            elif (e.reason.args[0] == 10061):
                print("\033[1;31m\nURL open error: Please check if the API server is up or there is any other issue accessing the URL\033[1;m")
                raise e
            else:
                print(e.reason.args)
                # bubble error back up after printing relevant details
                raise e # We raise error only when unknown errors occurs (other than HTTP error and url open error 10061)
        except Exception as e:
            print("Python says:%s" % str(e))
            json_response = None

        return {'response': response.status_code,'text':response.text,'json_response':json_response, 'error': error}

    def post(self, url,params=None, data=None,json=None,headers=None):
        "Post request"
        error = {}
        json_response = None
        headers = headers if headers else {}
        try:
            response = self.request_obj.post(url,params=params,json=json,headers=headers)
            try:
                json_response = response.json()
            except:
                json_response = None
        except (HTTPError,URLError) as e:
            error = e
            if isinstance(e,HTTPError,URLError):
                error_message = e.read()
                print("\n******\nPOST Error: %s %s %s" %
                    (url, error_message, str(json)))
            elif (e.reason.args[0] == 10061):
                print("\033[1;31m\nURL open error: Please check if the API server is up or there is any other issue accessing the URL\033[1;m")
            else:
                print(e.reason.args)
                # bubble error back up after printing relevant details
            raise e
        except Exception as e:
            print("Python says:%s" % str(e))
            json_response = None

        return {'response': response.status_code,'text':response.text,'json_response':json_response, 'error': error}


    def delete(self, url,headers=None):
        "Delete request"
        response = False
        error = {}
        headers = headers if headers else {}
        try:
            response = self.request_obj.delete(url,headers = headers)
            try:
                json_response = response.json()
            except:
                json_response = None

        except (HTTPError,URLError) as e:
            error = e
            if isinstance(e,HTTPError):
                error_message = e.read()
                print("\n******\nPUT Error: %s %s %s" %
                      (url, error_message, str(data)))
            elif (e.reason.args[0] == 10061):
                print("\033[1;31m\nURL open error: Please check if the API server is up or there is any other issue accessing the URL\033[1;m")
            else:
                print(str(e.reason.args))
            # bubble error back up after printing relevant details
            raise e
        except Exception as e:
            print("Python says:%s" % str(e))
            json_response = None

        return {'response': response.status_code,'text':response.text,'json_response':json_response, 'error': error}


    def put(self,url,json=None, headers=None):
        "Put request"
        error = {}
        response = False
        headers = headers if headers else {}
        try:
            response = self.request_obj.put(url,json=json,headers=headers)
            try:
                json_response = response.json()
            except:
                json_response = None


        except (HTTPError,URLError) as e:
            error = e
            if isinstance(e,HTTPError):
                error_message = e.read()
                print("\n******\nPUT Error: %s %s %s" %
                      (url, error_message, str(data)))
            elif (e.reason.args[0] == 10061):
                print("\033[1;31m\nURL open error: Please check if the API server is up or there is any other issue accessing the URL\033[1;m")
            else:
                print(str(e.reason.args))
            # bubble error back up after printing relevant details
            raise e
        except Exception as e:
            print("Python says:%s" % str(e))
            json_response = None

        return {'response': response.status_code,'text':response.text,'json_response':json_response, 'error': error}

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
