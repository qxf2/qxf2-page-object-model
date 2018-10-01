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

    '''
    def get(self, url, headers={}):
        "Mechanize Get request"
        #browser = self.get_browser()
        request_headers = []
        response = {}
        error = {}
        text = None
        status_code = None
        #user = user_name
        #passwd = password
        for key, value in headers.items():
            request_headers.append((key, value))
            #browser.addheaders = request_headers
        try:
            #response = browser.open(mechanize.Request(url))
            #response = requests.get(url,auth=('eric','testqxf2'))
            #response = requests.get(url,auth=(conf.user_name,conf.password))
            response = requests.get(url=url,headers=headers)
            try:
                json_response = response.json()
            except:
                json_response = None
            status_code = response.status_code
            text = response.text
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

        return {'response': status_code,'text':text,'json_response':json_response, 'error': error}
    

    def post(self, url,params=None, data=None,json=None,headers={}):
        "Mechanize Post request"
        #browser = self.get_browser()
        response = {}
        error = {}
        try:
            #post_url = 'http://127.0.0.1:5000/cars/add/'
            #response = browser.open(mechanize.Request(
            #url=url, data=data, headers=headers))
            #response = requests.post('http://127.0.0.1:5000/cars/add',json ={'name':'figo','brand':'Ford','price_range':'2-3lacs','car_type':'hatchback'}, auth=('eric','testqxf2'))
            print (url)
            print (json)
            print (headers)
            response = requests.post(url,params=params,data=data,json=json,headers=headers)
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
    '''
    def get(self, url, headers={}):
        "Get request"
        json_response = None 
        #request_headers = []
        error = {}
        #for key, value in headers.items():
        #request_headers.append((key, value))
        try:
            print ('get_url',url)
            print ('get_headerssssssssss',headers)
            response = requests.get(url=url,headers=headers)
            print ('respo_get_users', response)
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

        return {'response': response.status_code,'text':response.text,'json_response':json_response, 'error': error}


    def post(self, url,params=None, data=None,json=None,headers={}):
        "Post request"
        error = {}
        json_response = None
        try:
            response = requests.post(url,params=params,data=data,json=json,headers=headers)
            try:
                json_response = response.json()
            except:
                json_response = None
        except (HTTPError,URLError) as e:
            error = e
            if isinstance(e,HTTPError,URLError):
                error_message = e.read()
                print("\n******\nPOST Error: %s %s %s" %
                    (url, error_message, str(data)))
            elif (e.reason.args[0] == 10061):
                print("\033[1;31m\nURL open error: Please check if the API server is up or there is any other issue accessing the URL\033[1;m")
            else:
                print(e.reason.args)
                # bubble error back up after printing relevant details
            raise e

        return {'response': response.status_code,'text':response.text,'json_response':json_response, 'error': error}

    
    def delete(self, url,headers={}):
        "Mechanize Delete request"
        #browser = self.get_browser()
        response = False
        error = {}
        try:
            #browser.open(Mechanize_Delete_Request_class(url, headers=headers))
            #response = True
            #response = requests.delete('http://127.0.0.1:5000/cars/remove/figo', json = {'name':'figo','brand':'Ford','price_range':'2-3lacs','car_type':'hatchback'},auth=('eric','testqxf2'))
            response = requests.delete(url,headers = headers)
            print ('delete--hh',response)
            try:
                json_response = response.json()
                print ('delete--hh',json_response)
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

        return {'response': response.status_code,'text':response.text,'json_response':json_response, 'error': error}


    def put(self,url,json=None, headers={}):
        "Mechanize Put request"
        #browser = self.get_browser()
        #response = {}
        error = {}
        '''
        try:
            #put_url = 'http://127.0.0.1:5000/cars/update/'+ car_name
            #print (put_url)
           # response = requests.put(
              # url, json = data, headers = headers)
            print (response)
            #response = requests.put(url, json = data,headers=headers)
        '''
        try:
            print ('PUT',json)
            response = requests.put(url,json=json,headers=headers)
            print ('PUT',headers)
            print ('PUT',url)
            print ('PUT',response)
            print (response.text)
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

        return {'response': response.status_code,'text':response.text,'json_response':json_response, 'error': error}

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