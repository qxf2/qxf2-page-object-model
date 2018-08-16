"""
API_Player class does the following:
a) serves as an interface between the test and API_Interface
b) contains several useful wrappers around commonly used combination of actions
c) maintains the test context/state 
"""
from base64 import b64encode
from .API_Interface import API_Interface
from utils.results import Results
import json
import urllib
import logging
from utils.__init__ import get_dict_item
from conf import api_example_conf as conf


class API_Player(Results):
    "The class that maintains the test context/state"
    
    def __init__(self, url, log_file_path=None):
        "Constructor"
        super(API_Player, self).__init__(
            level=logging.DEBUG, log_file_path=log_file_path)
        self.api_obj = API_Interface(url=url)
        

    def set_auth_details(self, username, password):
        "encode auth details"
        user = username
        password = password
        b64login = b64encode('%s:%s' % (user, password))
        
        return b64login


    def set_header_details(self, auth_details=None):
        "make header details"
        if auth_details != '' and auth_details is not None:
            headers = {'content-type': 'application/json',
                       'Authorization': 'Basic %s' % auth_details}
        else:
            headers = {'content-type': 'application/json'}

        return headers


    def get_cars(self, auth_details=None):
        "get available cars "
        headers = self.set_header_details(auth_details)
        json_response = self.api_obj.get_cars(headers=headers)
        json_response = json_response['response']
        result_flag = True if json_response['successful'] == True else False
        self.write(msg="Fetched cars list:\n %s"%str(json_response))
        self.conditional_write(result_flag,
                               positive="Successfully fetched cars",
                               negative="Could not fetch cars")

        return json_response


    def get_car(self, car_name, brand, auth_details=None):
        "gets a given car details"
        url_params = {'car_name': car_name, 'brand': brand}
        url_params_encoded = urllib.urlencode(url_params)
        headers = self.set_header_details(auth_details)
        json_response = self.api_obj.get_car(url_params=url_params_encoded,
                                             headers=headers)
        response = json_response['response']
        result_flag = True if response['successful'] == True else False
        self.write(msg='Fetched car details of :%s %s' % (car_name, response))

        return result_flag


    def add_car(self, car_details, auth_details=None):
        "adds a new car"
        car_details = conf.car_details
        data = car_details
        headers = self.set_header_details(auth_details)
        json_response = self.api_obj.add_car(data=json.dumps(data),
                                             headers=headers)
        json_response = json_response['response']
        response = json.loads(json_response.read())
        result_flag = True if response['successful'] == True else False

        return result_flag


    def register_car(self, car_name, brand, auth_details=None):
        "register car"
        url_params = {'car_name': car_name, 'brand': brand}
        url_params_encoded = urllib.urlencode(url_params)
        customer_details = conf.customer_details
        data = customer_details
        headers = self.set_header_details(auth_details)
        json_response = self.api_obj.register_car(url_params=url_params_encoded,
                                                  data=json.dumps(data),
                                                  headers=headers)
        response = json.loads(json_response['response'])
        result_flag = True if response['registered_car']['successful'] == True else False

        return result_flag


    def update_car(self, car_details, car_name='figo', auth_details=None):
        "updates a car"
        data = {'name': car_details['name'],
                'brand': car_details['brand'],
                'price_range': car_details['price_range'],
                'car_type': car_details['car_type']}
        data = json.dumps(data)
        headers = self.set_header_details(auth_details)
        json_response = self.api_obj.update_car(car_name,
                                                data=data,
                                                headers=headers)
        json_response = json_response['response']
        response = json.loads(json_response.read())
        result_flag = True if response['response']['successful'] == True else False

        return result_flag


    def remove_car(self, car_name, auth_details=None):
        "deletes a car entry"
        headers = self.set_header_details(auth_details)
        json_response = self.api_obj.remove_car(car_name,
                                                headers=headers)
        result_flag = True if json_response['response'] == True else False

        return result_flag


    def get_registered_cars(self, auth_details=None):
        "gets registered cars"
        headers = self.set_header_details(auth_details)
        json_response = self.api_obj.get_registered_cars(headers=headers)
        response = json_response['registered_cars']
        result_flag = True if response['successful'] == True else False
        self.write(msg="Fetched registered cars list:\n %s"%str(json_response))
        self.conditional_write(result_flag,
                               positive='Successfully fetched registered cars list',
                               negative='Could not fetch registered cars list')

        return response


    def delete_registered_car(self, auth_details=None):
        "deletes registered car"
        headers = self.set_header_details(auth_details)
        json_response = self.api_obj.delete_registered_car(headers=headers)
        result_flag = True if json_response['response'] == True else False
        self.conditional_write(result_flag,
                               positive='Successfully deleted registered cars',
                               negative='Could not delete registered car')

    def verify_car_count(self, expected_count, auth_details=None):
        "Verify car count"
        self.write('\n*****Verifying car count******')
        car_count = self.get_cars(auth_details)
        car_count = len(car_count['cars_list'])
        result_flag = True if car_count == expected_count else False

        return result_flag


    def verify_registration_count(self, expected_count, auth_details=None):
        "Verify registered car count"
        self.write('\n******Verifying registered car count********')
        car_count = self.get_registered_cars(auth_details)
        car_count = len(car_count['registered'])
        result_flag = True if car_count == expected_count else False

        return result_flag


    def get_user_list(self, auth_details=None):
        "get user list"
        headers = self.set_header_details(auth_details)
        result = self.api_obj.get_user_list(headers=headers)
        self.write("Request & Response:\n%s\n" % str(result))
        user_list = {}
        response_code = None

        """if userlist result is none then return http error code"""
        try:
            response = get_dict_item(result, 'response')
            if response is not None:
                user_list = get_dict_item(response, 'user_list')
                error = get_dict_item(result, 'error')
            if error is not None:
                response_code = error.code
        except (TypeError, AttributeError) as e:
            raise e

        return {'user_list': user_list, 'response_code': response_code}


    def check_validation_error(self, auth_details=None):
        "verify validatin error 403"
        result = self.get_user_list(auth_details)
        user_list = result['user_list']
        response_code = result['response_code']
        result_flag = False
        msg = ''

        "verify result based on user list and response code"
        if user_list is None and response_code == 403:
            msg = "403 FORBIDDEN: Authentication successful but no access for non admin users"

        elif response_code == 200:
            result_flag = True
            msg = "successful authentication and access permission"

        elif response_code == 401:
            msg = "401 UNAUTHORIZED: Authenticate with proper credentials OR Require Basic Authentication"

        elif response_code == 404:
            msg = "404 NOT FOUND: URL not found"

        else:
            msg = "unknown reason"

        return {'result_flag': result_flag, 'msg': msg}
