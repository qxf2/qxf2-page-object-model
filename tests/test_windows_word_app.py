"""
Automated test for windows word application
Our automated test will do the following:
    # Launch the MS Word app
    # Select blank page and enter some text
    # Insert a icon/emoji
    # Verify page content
    # Close the app

Future Enhancement:
    - Handle the "Save" popup that appears when closing the application
"""

# pylint: disable=E0401, C0413
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from page_objects.PageFactory import PageFactory

def test_windows_word_app(test_windows_obj):
    "Run the test."
    try:
        # Initialize flags for tests summary.
        expected_pass = 0
        actual_pass = -1

        # # Create a test object.
        test_windows_obj = PageFactory.get_page_object("word")
        start_time = int(time.time())

        # Run test steps
        # Select blank page and enter text
        text = "Able to write using Qxf2’s POM framework."
        result_flag = test_windows_obj.select_blank_page_and_enter_text(text)
        test_windows_obj.log_result(result_flag,
                                positive="Successfully selected blank page and entered text",
                                negative="Failed to select blank page or enter text",
                                level="critical")

        # Insert icon
        result_flag = test_windows_obj.insert_icon()
        test_windows_obj.log_result(result_flag,
                                positive="Successfully inserted icon",
                                negative="Failed to insert icon",
                                level="critical")

        #verify the text
        result_flag = test_windows_obj.verify_text_on_page(text)
        test_windows_obj.log_result(result_flag,
                                positive="Successfully verified - Text is exist on page",
                                negative="Text is missing on the page",
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
