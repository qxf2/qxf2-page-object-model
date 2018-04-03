import pytest
import os
from conf import browser_os_name_conf
from utils import post_test_reports_to_slack


@pytest.fixture
def browser():
    "pytest fixture for browser"
    return pytest.config.getoption("-B")


@pytest.fixture
def base_url():
    "pytest fixture for base url"
    return pytest.config.getoption("-U")

@pytest.fixture
def api_url():
    "pytest fixture for base url"
    return pytest.config.getoption("-A")

@pytest.fixture
def test_run_id():
    "pytest fixture for test run id"
    return pytest.config.getoption("-R")


@pytest.fixture
def testrail_flag():
    "pytest fixture for test rail flag"
    return pytest.config.getoption("-X")


@pytest.fixture
def remote_flag():
    "pytest fixture for browserstack/sauce flag"
    return pytest.config.getoption("-M")


@pytest.fixture
def browser_version():
    "pytest fixture for browser version"
    return pytest.config.getoption("-V") 


@pytest.fixture
def os_name():
    "pytest fixture for os_name"
    return pytest.config.getoption("-P") 


@pytest.fixture
def os_version():
    "pytest fixture for os version"
    return pytest.config.getoption("-O")


@pytest.fixture
def slack_flag():
    "pytest fixture for sending reports on slack"
    return pytest.config.getoption("-S")


@pytest.fixture
def mobile_os_name():
    "pytest fixture for mobile os name"
    return pytest.config.getoption("-G")


@pytest.fixture
def mobile_os_version():
    "pytest fixture for mobile os version"
    return pytest.config.getoption("-H")


@pytest.fixture
def device_name():
    "pytest fixture for device name"
    return pytest.config.getoption("-I")


@pytest.fixture
def app_package():
    "pytest fixture for app package"
    return pytest.config.getoption("-J")


@pytest.fixture
def app_activity():
    "pytest fixture for app activity"
    return pytest.config.getoption("-K")


@pytest.fixture
def device_flag():
    "pytest fixture for device flag"
    return pytest.config.getoption("-Q")


def pytest_terminal_summary(terminalreporter, exitstatus):
    "add additional section in terminal summary reporting."
    if pytest.config.getoption("-S").lower() == 'y':
        post_test_reports_to_slack.post_reports_to_slack()


def pytest_generate_tests(metafunc):
    "test generator function to run tests across different parameters"
    if metafunc.config.getoption("-B") == []:
      metafunc.config.option.browser = browser_os_name_conf.default_browser
    if 'browser' in metafunc.fixturenames:
        if metafunc.config.getoption("-M").lower() == 'y':
            if metafunc.config.getoption("-B") == ["all"]:
                metafunc.parametrize("browser,browser_version,os_name,os_version", 
                                    browser_os_name_conf.cross_browser_cross_platform_config)
            else:
                metafunc.parametrize("browser,browser_version,os_name,os_version", 
                                    browser_os_name_conf.default_config_list)
        if metafunc.config.getoption("-M").lower() !='y':
            if metafunc.config.getoption("-B") == ["all"]:
                metafunc.config.option.browser = browser_os_name_conf.local_browsers
            metafunc.parametrize("browser",
                                metafunc.config.option.browser)


def pytest_addoption(parser):
    parser.addoption("-B","--browser",
                      dest="browser",
                      action="append",
                      default=[],
                      help="Browser. Valid options are firefox, ie and chrome")                      
    parser.addoption("-U","--app_url",
                      dest="url",
                      default="https://qxf2.com",
                      help="The url of the application")
    parser.addoption("-X","--testrail_flag",
                      dest="testrail_flag",
                      default='N',
                      help="Y or N. 'Y' if you want to report to TestRail")
    parser.addoption("-R","--test_run_id",
                      dest="test_run_id",
                      default=None,
                      help="The test run id in TestRail")
    parser.addoption("-M","--remote_flag",
                      dest="remote_flag",
                      default="N",
                      help="Run the test in Browserstack/Sauce Lab: Y or N")
    parser.addoption("-O","--os_version",
                      dest="os_version",
                      action="append",
                      help="The operating system: xp, 7",
                      default=[])
    parser.addoption("-V","--ver",
                      dest="browser_version",
                      action="append",
                      help="The version of the browser: a whole number",
                      default=[])
    parser.addoption("-P","--os_name",
                      dest="os_name",
                      action="append",
                      help="The operating system: Windows 7, Linux",
                      default=[])
    parser.addoption("-S","--slack_flag",
                      dest="slack_flag",
                      default="N",
                      help="Post the test report on slack channel: Y or N")
    parser.addoption("-G","--mobile_os_name",
                      dest="mobile_os_name",
                      help="Enter operating system of mobile. Ex: Android, iOS",
                      default="Android")
    parser.addoption("-H","--mobile_os_version",
                      dest="mobile_os_version",
                      help="Enter version of operating system of mobile: 8.1.0",
                      default="6.0")
    parser.addoption("-I","--device_name",
                      dest="device_name",
                      help="Enter device name. Ex: Emulator, physical device name",
                      default="Google Nexus 6")
    parser.addoption("-J","--app_package",
                      dest="app_package",
                      help="Enter name of app package. Ex: bitcoininfo",
                      default="com.dudam.rohan.bitcoininfo")
    parser.addoption("-K","--app_activity",
                      dest="app_activity",
                      help="Enter name of app activity. Ex: .MainActivity",
                      default=".MainActivity")
    parser.addoption("-Q","--device_flag",
                      dest="device_flag",
                      help="Enter Y or N. 'Y' if you want to run the test on device. 'N' if you want to run the test on emulator.",
                      default="N")



