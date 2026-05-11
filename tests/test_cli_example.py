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
from conf import cli_example_conf as conf


@pytest.mark.CLI
def test_cli_example(test_cli_obj):
    "Run cli example test"
    try:
        expected_pass = 0
        actual_pass = -1

        # Create a test object and execute commands and verify
        test_cli_obj = PageFactory.get_page_object("common_cli_commands")

        # Execute echo command and verify response
        echo_message = conf.echo_message

        result_flag, _ = test_cli_obj.execute_echo_cmd_and_verify_response(echo_message)

        test_cli_obj.log_result(
            result_flag,
            positive="Echo command executed and verified successfully",
            negative="Echo command execution or verification failed"
        )

        # Verify python installed or not by verifing python version
        version_string = conf.version_string
        flag, _ = test_cli_obj.execute_python_version_cmd_and_verify(version_string)

        test_cli_obj.log_result(
            flag,
            positive="Python 3 is installed and verified",
            negative="Python 3 is missing or incorrect version"
        )

        # cat file and verify content
        cat_file_name = conf.cat_file_name
        cat_expected_strings= conf.cat_expected_strings

        flag, _ = test_cli_obj.execute_cat_file_and_verify(file_name=cat_file_name,
                                                expected_strings=cat_expected_strings)

        test_cli_obj.log_result(
            flag,
            positive=f"Successfully verified, file {cat_file_name} contains {cat_expected_strings} words",
            negative=f"In file {cat_file_name} missing few or all word in the list - {cat_expected_strings}"
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
