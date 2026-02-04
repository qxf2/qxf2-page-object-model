"""
CLI Example Tests

These tests demonstrate how to use the CliHelper to execute and validate CLI commands in
Qxf2's automation framework.
Our automated test will do the following:
    # Execute echo command and verify response
    # Verify Python 3 is installed
    # Execute cat <file> command and verify file contents
"""

import os
import sys
import traceback
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from page_objects import PageFactory


@pytest.mark.CLI
def test_cli_example(test_cli_obj):
    "Run api test"
    try:
        expected_pass = 0
        actual_pass = -1

        # Create a test object and execute commands and verify
        test_cli_obj = PageFactory.get_page_object("common_cli_commands")

        # Execute echo command and verify response
        result_flag, _ = test_cli_obj.execute_echo_cmd_and_verify_response("hello-qxf2")

        test_cli_obj.log_result(
            result_flag,
            positive="Echo command executed and verified successfully",
            negative="Echo command execution or verification failed"
        )

        # Verify python installed or not by verifing python version
        flag, _ = test_cli_obj.execute_python_version_cmd_and_verify()

        test_cli_obj.log_result(
            flag,
            positive="Python 3 is installed and verified",
            negative="Python 3 is missing or incorrect version"
        )

        # cat ./conf/base_url_conf.py and verify
        flag, _ = test_cli_obj.execute_cat_file_and_verify(file_name="./conf/base_url_conf.py",
                                                expected_strings=["ui_base_url", "api"])

        test_cli_obj.log_result(
            flag,
            positive="./conf/base_url_conf.py contains ui_base_url and api words",
            negative="./conf/base_url_conf.py missing ui_base_url and/or api words"
        )

        #Print out the result
        test_cli_obj.write_test_summary(cli_test=True)
        expected_pass = test_cli_obj.result_counter
        actual_pass = test_cli_obj.pass_counter

    except Exception as e:
        print(e)
        traceback.print_exc()
        test_cli_obj.write(f"Exception when trying to run test: {__file__}")
        test_cli_obj.write(f"Python says: {str(e)}")

    # Assertion
    if expected_pass != actual_pass:
        raise AssertionError(f"Test failed: {__file__}")
