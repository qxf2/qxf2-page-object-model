"""

API EXAMPLE TEST
1. Add new car - POST request(without url_params)
2. Get all cars - GET request(without url_params)
3. Verify car count
4. Update newly added car details -PUT request
5. Get car details -GET request(with url_params)
6. Register car - POST request(with url_params)
7. Get list of registered cars -GET
8. Verify registered cars count
9. Delete newly added car -DELETE request
"""

import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from endpoints.API_Player import API_Player
from conf import api_example_conf as conf

@pytest.mark.API
def test_api_example(api_url='http://127.0.0.1:5000'):
    "Run api test"
    try:
        # Create test object
        test_obj = API_Player(url=api_url)
        expected_pass = 0
        actual_pass = -1

        # set authentication details
        username = conf.user_name
        password = conf.password
        auth_details = test_obj.set_auth_details(username, password)

        initial_car_count = test_obj.get_car_count(auth_details)


        # add cars
        car_details = conf.car_details
        result_flag = test_obj.add_car(car_details=car_details,
                                          auth_details=auth_details)
        test_obj.log_result(result_flag,
                               positive='Successfully added new car with details %s' % car_details,
                               negative='Could not add new car with details %s' % car_details)



        # Get Cars and verify if new car is added
        result_flag = test_obj.get_cars(auth_details)

        result_flag = test_obj.verify_car_count(expected_count=initial_car_count+1,
                                                auth_details=auth_details)
        test_obj.log_result(result_flag,
                            positive='Total car count matches expected count',
                            negative='Total car count doesnt match expected count')

        # Update car
        update_car = conf.update_car
        update_car_name = conf.car_name_2
        result_flag = test_obj.update_car(auth_details=auth_details,
                                          car_name=update_car_name,
                                          car_details=update_car)
        test_obj.log_result(result_flag,
                            positive='Successfully updated car : %s' % update_car_name,
                            negative='Couldnt update car :%s' % update_car_name)

        # Get one car details
        new_car = conf.car_name_1
        brand = conf.brand
        result_flag = test_obj.get_car(auth_details=auth_details,
                                       car_name=new_car,
                                       brand=brand)
        test_obj.log_result(result_flag,
                            positive='Successfully fetched car details of car : %s' % new_car,
                            negative='Couldnt fetch car details of car :%s' % new_car)

        # Register car
        customer_details = conf.customer_details
        result_flag = test_obj.register_car(auth_details=auth_details,
                                            car_name=new_car,
                                            brand=brand)
        test_obj.log_result(result_flag,
                            positive='Successfully registered new car %s with customer details %s' % (new_car, customer_details),
                            negative='Couldnt register new car %s with cutomer details %s' % (new_car, customer_details))

        #Get Registered cars and check count
        result_flag = test_obj.get_registered_cars(auth_details)
        register_car_count = test_obj.get_regi_car_count(auth_details)

        result_flag = test_obj.verify_registration_count(expected_count=register_car_count,
                                                         auth_details=auth_details)
        test_obj.log_result(result_flag,
                            positive='Registered count matches expected value',
                            negative='Registered car count doesnt match expected value')

        # Remove newly added car
        result_flag = test_obj.remove_car(auth_details=auth_details,
                                          car_name=update_car_name)
        test_obj.log_result(result_flag,
                            positive='Successfully deleted car %s' % update_car,
                            negative='Could not delete car %s ' % update_car)

        # validate if car is deleted
        result_flag = test_obj.verify_car_count(expected_count=initial_car_count,
                                                auth_details=auth_details)
        test_obj.log_result(result_flag,
                            positive='Total car count matches expected count after deleting one car',
                            negative='Total car count doesnt match expected count after deleting one car')

        # Deleting registered car
        test_obj.delete_registered_car(auth_details)

        # test for validation http error 403
        result = test_obj.check_validation_error(auth_details)

        test_obj.log_result(not result['result_flag'],
                            positive=result['msg'],
                            negative=result['msg'])

        # test for validation http error 401 when no authentication
        auth_details = None
        result = test_obj.check_validation_error(auth_details)
        test_obj.log_result(not result['result_flag'],
                            positive=result['msg'],
                            negative=result['msg'])

        # test for validation http error 401 for invalid authentication
        # set invalid authentication details
        username = conf.invalid_user_name
        password = conf.invalid_password
        auth_details = test_obj.set_auth_details(username, password)
        result = test_obj.check_validation_error(auth_details)
        test_obj.log_result(not result['result_flag'],
                            positive=result['msg'],
                            negative=result['msg'])

        # write out test summary
        expected_pass = test_obj.total
        actual_pass = test_obj.passed
        test_obj.write_test_summary()

    except Exception as e:
        if api_url=='http://127.0.0.1:5000':
            test_obj.write("Please run the test against http://35.167.62.251/ by changing the api_url in test_api_example.py")  
            test_obj.write("OR")
            test_obj.write("Clone the repo 'https://github.com/qxf2/cars-api.git' and run the cars_app inorder to run the test against your system")
        
        else:
            test_obj.write("Exception when trying to run test:%s" % __file__)
            test_obj.write("Python says:%s" % str(e))

    # Assertion
    assert expected_pass == actual_pass,"Test failed: %s"%__file__


if __name__ == '__main__':
    test_api_example()


