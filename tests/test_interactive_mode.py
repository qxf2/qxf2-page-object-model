"""
This module contains a few unit tests for the interactive mode util file
"""
import unittest, mock
from unittest.mock import Mock
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils.interactive_mode as interactive_mode

class check_interactive_mode(unittest.TestCase):
    """
    This class contains unit tests for interactive_mode util
    """

    @mock.patch('utils.interactive_mode.get_user_response_gui',return_value="Run")
    def test_ask_questions_gui_one(self, mock_response):
        "This method tests whether the function returns all the arguments passed accurately as a tuple"

        mock_inputs = Mock(browser = "chrome", os_name = [], os_version = [],browser_version = [],remote_flag = "N",testrail_flag = "N",tesults_flag = "N")

        assert interactive_mode.ask_questions_gui(mock_inputs.browser, mock_inputs.browser_version, mock_inputs.os_version, mock_inputs.os_name, mock_inputs.remote_flag, mock_inputs.testrail_flag, mock_inputs.tesults_flag) == ('chrome', [], 'N', [], [], 'N', 'N')

    @mock.patch('utils.interactive_mode.get_user_response_gui',return_value="Run")
    def test_ask_questions_gui_two(self, mock_response):
        "This method tests whether the function updates the browser accurately incase the browser is changed"

        mock_inputs = Mock(browser = "firefox", os_name = [], os_version = [],browser_version = [],remote_flag = "N",testrail_flag = "N",tesults_flag = "N")

        assert interactive_mode.ask_questions_gui(mock_inputs.browser, mock_inputs.browser_version, mock_inputs.os_version, mock_inputs.os_name, mock_inputs.remote_flag, mock_inputs.testrail_flag, mock_inputs.tesults_flag) != ('chrome', [], 'N', [], [], 'N', 'N')

    @mock.patch('utils.interactive_mode.get_user_response_gui',return_value="Run")
    def test_ask_questions_gui_three(self, mock_response):
        "This method tests whether the function updates the testrail and tesults flag"

        mock_inputs = Mock(browser = "firefox", os_name = [], os_version = [],browser_version = [],remote_flag = "N",testrail_flag = "N",tesults_flag = "N")

        assert interactive_mode.ask_questions_gui(mock_inputs.browser, mock_inputs.browser_version, mock_inputs.os_version, mock_inputs.os_name, mock_inputs.remote_flag, mock_inputs.testrail_flag, mock_inputs.tesults_flag) != ('chrome', [], 'N', [], [], 'Y', 'Y')


    @mock.patch('utils.interactive_mode.get_user_response_mobile',return_value="Run")
    def test_ask_mobile_questions_one(self, mock_response):
        "This method tests whether the function returns all the arguments passed accurately as a tuple"

        mock_inputs = Mock(mobile_os_name = "Android", mobile_os_version = "8.0", device_name = "Samsung Galaxy S9", app_package = "com.dudam.rohan.bitcoininfo", app_activity = ".MainActivity", remote_flag = "N", device_flag = "N", testrail_flag = "N", tesults_flag = "N", app_name = "Bitcoin Info_com.dudam.rohan.bitcoininfo.apk", app_path = "D:/code/bitcoin-info/app")

        assert interactive_mode.ask_questions_mobile(mock_inputs.mobile_os_name, mock_inputs.mobile_os_version, mock_inputs.device_name, mock_inputs.app_package, mock_inputs.app_activity, mock_inputs.remote_flag, mock_inputs.device_flag, mock_inputs.testrail_flag, mock_inputs.tesults_flag, mock_inputs.app_name, mock_inputs.app_path) == ('Android', '8.0', 'Samsung Galaxy S9', 'com.dudam.rohan.bitcoininfo', '.MainActivity', 'N', 'N', 'N', 'N', 'Bitcoin Info_com.dudam.rohan.bitcoininfo.apk','D:/code/bitcoin-info/app')

    @mock.patch('utils.interactive_mode.get_user_response_mobile',return_value="Run")
    def test_ask_mobile_questions_two(self, mock_response):
        "This method tests whether the function gets updated when input is changed"

        mock_inputs = Mock(mobile_os_name = "iOS", mobile_os_version = "8.0", device_name = "Samsung Galaxy S9", app_package = "com.dudam.rohan.bitcoininfo", app_activity = ".MainActivity", remote_flag = "N", device_flag = "N", testrail_flag = "N", tesults_flag = "N", app_name = "Bitcoin Info_com.dudam.rohan.bitcoininfo.apk", app_path = "D:/code/bitcoin-info/app")

        assert interactive_mode.ask_questions_mobile(mock_inputs.mobile_os_name, mock_inputs.mobile_os_version, mock_inputs.device_name, mock_inputs.app_package, mock_inputs.app_activity, mock_inputs.remote_flag, mock_inputs.device_flag, mock_inputs.testrail_flag, mock_inputs.tesults_flag, mock_inputs.app_name, mock_inputs.app_path) != ('Android', '8.0', 'Samsung Galaxy S9', 'com.dudam.rohan.bitcoininfo', '.MainActivity', 'N', 'N', 'N', 'N', 'Bitcoin Info_com.dudam.rohan.bitcoininfo.apk','D:/code/bitcoin-info/app')

    @mock.patch('utils.interactive_mode.get_user_response_api',return_value="Run")
    def test_ask_questions_api_one(self, mock_response):
        "This method tests whether the function returns all the arguments passed accurately as a tuple"

        mock_inputs = Mock(api_url = 'http://127.0.0.1:5000', session_flag = True)

        assert interactive_mode.ask_questions_api(mock_inputs.api_url, mock_inputs.session_flag) == ('http://127.0.0.1:5000', 'True')

    @mock.patch('utils.interactive_mode.get_user_response_api',return_value="Run")
    def test_ask_questions_api_two(self, mock_response):
        "This method tests whether the function updates the input accurately"

        mock_inputs = Mock(api_url = 'http://127.0.0.1:5000', session_flag = False)

        assert interactive_mode.ask_questions_api(mock_inputs.api_url, mock_inputs.session_flag) != ('http://127.0.0.1:5000', 'True')





if __name__=="__main__":
    unittest.main()