# pylint: disable=line-too-long
"""
API_Player class does the following:
a) serves as an interface between the test and API_Interface
b) contains several useful wrappers around commonly used combination of actions
c) maintains the test context/state
"""
from base64 import b64encode
import logging
import urllib.parse
from .api_interface import APIInterface
from utils import Results


class APIPlayer(Results):
    "The class that maintains the test context/state"

    def __init__(self, url, log_file_path=None):
        "Constructor"
        super().__init__(level=logging.DEBUG, log_file_path=log_file_path)
        self.api_obj = APIInterface(url=url)


    def set_auth_details(self, username, password):
        "encode auth details"
        user = username
        b64login = b64encode(bytes(f"{user}:{password}","utf-8"))
        return b64login.decode('utf-8')


    def set_header_details(self, auth_details=None):
        "make header details"
        if auth_details != '' and auth_details is not None:
            headers = {'Authorization': f"Basic {auth_details}"}
        else:
            headers = {'content-type': 'application/json'}
        return headers


    def get_cars(self, auth_details=None):
        "get available cars "
        result_flag = False
        headers = self.set_header_details(auth_details)
        json_response = self.api_obj.get_cars(headers=headers)
        json_response = json_response['response']
        if json_response["successful"]:
            result_flag = True
        self.write(msg=f"Fetched cars list: {json_response}")
        self.conditional_write(result_flag,
                               positive="Successfully fetched cars",
                               negative="Could not fetch cars")
        return json_response


    def get_car(self, car_name, brand, auth_details=None):
        "gets a given car details"
        result_flag = False
        url_params = {'car_name': car_name, 'brand': brand}
        url_params_encoded = urllib.parse.urlencode(url_params)
        headers = self.set_header_details(auth_details)
        json_response = self.api_obj.get_car(url_params=url_params_encoded,
                                             headers=headers)
        response = json_response['response']
        if response["successful"]:
            result_flag = True
        self.write(msg=f"Fetched car details of : {car_name} {response}")
        return result_flag


    def add_car(self, car_details, auth_details=None):
        "adds a new car"
        result_flag = False
        data = car_details
        headers = self.set_header_details(auth_details)
        json_response = self.api_obj.add_car(data=data,
                headers=headers)
        if json_response["response"]["successful"]:
            result_flag = True
        return result_flag


    def register_car(self, car_name, brand, auth_details=None):
        "register car"
        result_flag = False
        # pylint: disable=import-outside-toplevel
        from conf import api_example_conf as conf
        url_params = {'car_name': car_name, 'brand': brand}
        url_params_encoded = urllib.parse.urlencode(url_params)
        customer_details = conf.customer_details
        data = customer_details
        headers = self.set_header_details(auth_details)
        json_response = self.api_obj.register_car(url_params=url_params_encoded,
                                                  json=data,
                                                  headers=headers)
        response = json_response['response']
        if response["registered_car"]["successful"]:
            result_flag = True
        return result_flag


    def update_car(self, car_details, car_name='figo', auth_details=None):
        "updates a car"
        result_flag = False
        data = {'name': car_details['name'],
                'brand': car_details['brand'],
                'price_range': car_details['price_range'],
                'car_type': car_details['car_type']}

        headers = self.set_header_details(auth_details)
        json_response = self.api_obj.update_car(car_name,
                                                json=data,
                                                headers=headers)
        json_response = json_response['response']
        if json_response["response"]["successful"]:
            result_flag = True
        return result_flag


    def remove_car(self, car_name, auth_details=None):
        "deletes a car entry"
        result_flag = False
        headers = self.set_header_details(auth_details)
        json_response = self.api_obj.remove_car(car_name,
                                                headers=headers)
        if json_response["response"]["successful"]:
            result_flag = True
        return result_flag


    def get_registered_cars(self, auth_details=None):
        "gets registered cars"
        result_flag = False
        headers = self.set_header_details(auth_details)
        json_response = self.api_obj.get_registered_cars(headers=headers)
        response = json_response['response']
        if response["successful"]:
            result_flag = True
        self.write(msg=f"Fetched registered cars list: {json_response}")
        self.conditional_write(result_flag,
                               positive='Successfully fetched registered cars list',
                               negative='Could not fetch registered cars list')
        return response


    def delete_registered_car(self, auth_details=None):
        "deletes registered car"
        result_flag = False
        headers = self.set_header_details(auth_details)
        json_response = self.api_obj.delete_registered_car(headers=headers)
        if json_response["response"]["successful"]:
            result_flag = True
        self.conditional_write(result_flag,
                               positive='Successfully deleted registered cars',
                               negative='Could not delete registered car')


    def get_car_count(self,auth_details=None):
        "Verify car count at the start"
        self.write('\n*****Verifying car count******')
        car_count = self.get_cars(auth_details)
        car_count = len(car_count['cars_list'])
        return car_count


    def get_regi_car_count(self,auth_details=None):
        "Verify registered car count"
        car_count_registered = self.get_registered_cars(auth_details)
        car_count_registered = len(car_count_registered['registered'])
        return car_count_registered


    def verify_car_count(self, expected_count, auth_details=None):
        "Verify car count"
        result_flag = False
        self.write('\n*****Verifying car count******')
        car_count = self.get_cars(auth_details)
        car_count = len(car_count['cars_list'])
        if car_count == expected_count:
            result_flag = True
        return result_flag


    def verify_registration_count(self, expected_count, auth_details=None):
        "Verify registered car count"
        result_flag = False
        self.write('\n******Verifying registered car count********')
        car_count = self.get_registered_cars(auth_details)
        car_count = len(car_count['registered'])
        if car_count == expected_count:
            result_flag = True
        return result_flag


    def get_user_list(self, auth_details=None):
        "get user list"
        headers = self.set_header_details(auth_details)
        try:
            result = self.api_obj.get_user_list(headers=headers)
            self.write(f"Request & Response: {result}")
        except (TypeError, AttributeError) as e:
            raise e
        return {'user_list': result['user_list'], 'response_code': result['response']}


    def check_validation_error(self, auth_details=None):
        "verify validatin error 403"
        result = self.get_user_list(auth_details)
        response_code = result['response_code']
        result_flag = False
        msg = ''

        if  response_code == 403:
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


    # Async methods
    async def async_get_cars(self, auth_details=None):
        "get available cars asynchronously"
        result_flag = False
        headers = self.set_header_details(auth_details)
        result = await self.api_obj.get_cars_async(headers)
        if result.status_code == 200:
            result_flag = True
        return result_flag


    async def async_get_car(self, car_name, brand, auth_details=None):
        "gets a given car details"
        result_flag = False
        url_params = {'car_name': car_name, 'brand': brand}
        url_params_encoded = urllib.parse.urlencode(url_params)
        headers = self.set_header_details(auth_details)
        response = await self.api_obj.get_car_async(url_params=url_params_encoded,
                                              headers=headers)
        if response.status_code == 200:
            result_flag = True
        return result_flag


    async def async_add_car(self, car_details, auth_details=None):
        "adds a new car"
        result_flag = False
        data = car_details
        headers = self.set_header_details(auth_details)
        response = await self.api_obj.add_car_async(data=data,
                                                    headers=headers)
        if response.status_code == 200:
            result_flag = True
        return result_flag


    async def async_get_registered_cars(self, auth_details=None):
        "get registered cars"
        result_flag = False
        headers = self.set_header_details(auth_details)
        response = await self.api_obj.get_registered_cars_async(headers=headers)
        if response.status_code == 200:
            result_flag = True
        return result_flag
