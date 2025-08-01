"""
Automated test for windows notepad application
"""

# pylint: disable=E0401, C0413
import time
import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from page_objects.PageFactory import PageFactory

@pytest.mark.MOBILE
def test_notepad_app(test_windows_obj):
    "Run the test."
    try:
        # Initialize flags for tests summary.
        expected_pass = 0
        actual_pass = -1

        # # Create a test object.
        test_windows_obj = PageFactory.get_page_object("notepad")
        start_time = int(time.time())

        # Run test steps
        #enter text
        text = "Able to write using Qxf2's POM framework."
        result_flag = test_windows_obj.enter_text(text)

        test_windows_obj.log_result(result_flag,
                                positive="Successfully set text",
                                negative="Failed to set text",
                                level="critical")
        
        result_flag = test_windows_obj.click_on_file_menu()

        test_windows_obj.log_result(result_flag,
                                positive="Successfully clicked on file menu",
                                negative="Failed to click on file menu",
                                level="critical")

        
        # Print out the results.
        test_windows_obj.write(f'Script duration: {int(time.time() - start_time)} seconds\n')
        test_windows_obj.write_test_summary()

        # Teardown and Assertion.
        expected_pass = test_windows_obj.result_counter
        actual_pass = test_windows_obj.pass_counter

    except Exception as e:
        print(f"Exception when trying to run test: {__file__}")
        print(f"Python says: {str(e)}")

    if expected_pass != actual_pass:
        raise AssertionError(f"Test failed: {__file__}")