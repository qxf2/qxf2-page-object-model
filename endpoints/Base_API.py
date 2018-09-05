"""
A wrapper around Mechanize to make Restful API calls
"""

import json
import requests
from requests.auth import HTTPBasicAuth
from urllib.error import HTTPError
from urllib.error import URLError
from conf import api_example_conf as conf

class Base_API:
    "Main base class for Mechanize based scripts"

    def __init__(self, url=None):
        pass


    #def get_browser(self):
        "Create and return a browser object"
        #browser = mechanize.Browser()
        #browser.set_handle_robots(False)

        #return browser


    def get(self, url, headers={}):
        "Mechanize Get request"
        #browser = self.get_browser()
        request_headers = []
        response = {}
        error = {}
        #user = user_name
        #passwd = password
        for key, value in headers.items():
            request_headers.append((key, value))
            #browser.addheaders = request_headers
        try:
            #response = browser.open(mechanize.Request(url))
            #response = requests.get(url,auth=('eric','testqxf2'))
            response = requests.get(url,auth=(conf.user_name,conf.password))
            json_response = response.json() 
            print (json_response['successful'])
            print (response.json())
            response = json.loads(response.text)
            print ("??????%s"%response)
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
                raise e  # We raise error only when unknown errors occurs (other than HTTP error and url open error 10061) 

        return {'response': response, 'error': error}
    

    def post(self, url, data=None, headers={}):
        "Mechanize Post request"
        #browser = self.get_browser()
        response = {}
        error = {}
        try:
            #response = browser.open(mechanize.Request(
                #url=url, data=data, headers=headers))
            response = requests.post('http://127.0.0.1:5000/cars/add',json ={'name':'figo','brand':'Ford','price_range':'2-3lacs','car_type':'hatchback'}, auth=('eric','testqxf2'))
        except (HTTPError,URLError) as e:
            error = e
            if isinstance(e,HTTPError,URLError):
                error_message = e.read()
                print("Iam here")
                print("\n******\nPOST Error: %s %s %s" %
                      (url, error_message, str(data)))
            elif (e.reason.args[0] == 10061):
                print("\033[1;31m\nURL open error: Please check if the API server is up or there is any other issue accessing the URL\033[1;m")
            else:
                print(e.reason.args)
            # bubble error back up after printing relevant details
            raise e

        return {'response': response, 'error': error}

    
    def delete(self, url, headers={}):
        "Mechanize Delete request"
        #browser = self.get_browser()
        response = False
        error = {}
        try:
            #browser.open(Mechanize_Delete_Request_class(url, headers=headers))
            #response = True
            response = requests.delete('http://127.0.0.1:5000/cars/remove/figo', json = {'name':'figo','brand':'Ford','price_range':'2-3lacs','car_type':'hatchback'},auth=('eric','testqxf2'))
        except Exception as e:
            if (e.reason.args[0] == 10061):
                print("\033[1;31m\nURL open error: Please check if the API server is up or there is any other issue accessing the URL\033[1;m")
            print("Exception in Mechanize_Delete_request: %s" % str(e))
            raise e

        return {'response': response, 'error': error}
    

    def put(self, url, data=None, headers={}):
        "Mechanize Put request"
        #browser = self.get_browser()
        response = {}
        error = {}
        try:
            response = requests.put(
                url, data=data, headers=headers)
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

        return {'response': response, 'error': error}

'''
class Mechanize_Put_Request_class(mechanize.Request):
    "Extend the mechanize Request class to allow a http PUT"

    def get_method(self):
        return "PUT"


class Mechanize_Delete_Request_class(mechanize.Request):
    "Extend the mechanize Request class to allow a http DELETE"

    def get_method(self):
        return "DELETE"
'''