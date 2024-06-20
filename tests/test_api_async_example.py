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

import asyncio
import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import api_example_conf

@pytest.mark.asyncio
@pytest.mark.skipif(sys.version_info < (3,11),
                    reason="requires Python3.11 or higher")
async def test_api_async_example(test_api_obj):
    "Run api test"
    try:
        expected_pass = 0
        actual_pass = -1

        # set authentication details
        username = api_example_conf.user_name
        password = api_example_conf.password
        auth_details = test_api_obj.set_auth_details(username, password)

        # Get Cars and verify if new car is added
        new_car = api_example_conf.car_name_1
        brand = api_example_conf.brand
        # add cars
        car_details = api_example_conf.car_details

        async with asyncio.TaskGroup() as group:
            get_cars = group.create_task(test_api_obj.async_get_cars(auth_details))
            add_new_car = group.create_task(test_api_obj.async_add_car(car_details=car_details,
                                                                       auth_details=auth_details))
            get_car = group.create_task(test_api_obj.async_get_car(auth_details=auth_details,
                                                                   car_name=new_car,
                                                                   brand=brand))
            get_reg_cars = group.create_task(test_api_obj.async_get_registered_cars(auth_details=auth_details))

        test_api_obj.log_result(get_cars.result(),
                                positive="Successfully obtained the list of cars",
                                negative="Failed to get the cars")
        test_api_obj.log_result(add_new_car.result(),
                                positive=f"Successfully added new car {car_details}",
                                negative="Failed to add a new car")
        test_api_obj.log_result(get_car.result(),
                                positive=f"Successfully obtained a car - {new_car}",
                                negative="Failed to add a new car")
        test_api_obj.log_result(get_reg_cars.result(),
                                positive="Successfully obtained registered cars",
                                negative="Failed to get registered cars")
        # write out test summary
        expected_pass = test_api_obj.total
        actual_pass = test_api_obj.passed
        test_api_obj.write_test_summary()
        # Assertion
        assert expected_pass == actual_pass,f"Test failed: {__file__}"

    except Exception as e:
        test_api_obj.write(f"Exception when trying to run test: {__file__}")
        test_api_obj.write(f"Python says: {str(e)}")
