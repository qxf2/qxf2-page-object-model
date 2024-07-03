"""
Automated test for Weather Shopper application recommndation app
"""

# pylint: disable=E0401, C0413
import secrets
import time
import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from page_objects.PageFactory import PageFactory


@pytest.mark.MOBILE
@pytest.mark.SMOKE
def test_recommendation_text(test_mobile_obj):
    "Run the test."
    try:
        # Initialize flags for tests summary.
        expected_pass = 0
        actual_pass = -1 

        # Create a test object.
        test_mobile_obj = PageFactory.get_page_object("weather shopper app")
        start_time = int(time.time())

        # Verify the recommendation text.
        result_flag = test_mobile_obj.verify_recommendation_text()
        
        test_mobile_obj.log_result(result_flag,
                                   positive="Successfully verified the recommendation text",
                                   negative="Recommendation text verification failed",
                                   level="debug")

        # Teardown and Assertion.
        expected_pass = 1 
        actual_pass = test_mobile_obj.pass_counter if result_flag else 0

        # Print out the results.
        test_mobile_obj.write(f'Script duration: {int(time.time() - start_time)} seconds\n')
        test_mobile_obj.write_test_summary()

    except Exception as e:
        print(f"Exception when trying to run test: {__file__}")
        print(f"Python says: {str(e)}")
        raise 

    if expected_pass != actual_pass:
        raise AssertionError(f"Test failed: {__file__}")
    
def verify_recommendation_text(test_mobile_obj):
    "check recommendation text"
    result_flag = test_mobile_obj.view_recommendation_text()

    return result_flag