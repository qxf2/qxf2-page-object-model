"""
API Async EXAMPLE TEST
This test collects tasks using asyncio.TaskGroup object \
and runs these scenarios asynchronously:
1. Get the list of cars
2. Add a new car
3. Get a specifi car from the cars list
4. Get the registered cars
"""

import asyncio
import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import api_example_conf

@pytest.mark.asyncio
# Skip running the test if Python version < 3.11
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

        # Get an existing car detail from conf
        existing_car = api_example_conf.car_name_1
        brand = api_example_conf.brand
        # Get a new car detail from conf
        car_details = api_example_conf.car_details

        async with asyncio.TaskGroup() as group:
            get_cars = group.create_task(test_api_obj.async_get_cars(auth_details))
            add_new_car = group.create_task(test_api_obj.async_add_car(car_details=car_details,
                                                                       auth_details=auth_details))
            get_car = group.create_task(test_api_obj.async_get_car(auth_details=auth_details,
                                                                   car_name=existing_car,
                                                                   brand=brand))
            get_reg_cars = group.create_task(test_api_obj.async_get_registered_cars(auth_details=auth_details))

        test_api_obj.log_result(get_cars.result(),
                                positive="Successfully obtained the list of cars",
                                negative="Failed to get the cars")
        test_api_obj.log_result(add_new_car.result(),
                                positive=f"Successfully added new car {car_details}",
                                negative="Failed to add a new car")
        test_api_obj.log_result(get_car.result(),
                                positive=f"Successfully obtained a car - {existing_car}",
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

    except Exception as err:
        raise err
