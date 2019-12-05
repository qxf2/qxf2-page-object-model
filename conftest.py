import os,pytest
from page_objects.PageFactory import PageFactory
from conf import browser_os_name_conf
from conf import base_url_conf
from utils import post_test_reports_to_slack
from utils.email_pytest_report import Email_Pytest_Report
from utils import Tesults

@pytest.fixture
def test_obj(base_url,browser,browser_version,os_version,os_name,remote_flag,testrail_flag,tesults_flag,test_run_id,remote_project_name,remote_build_name):
    
    "Return an instance of Base Page that knows about the third party integrations"
    test_obj = PageFactory.get_page_object("Zero",base_url=base_url)

    #Setup and register a driver
    test_obj.register_driver(remote_flag,os_name,os_version,browser,browser_version,remote_project_name,remote_build_name)

    #Setup TestRail reporting
    if testrail_flag.lower()=='y':
        if test_run_id is None:
            test_obj.write('\033[91m'+"\n\nTestRail Integration Exception: It looks like you are trying to use TestRail Integration without providing test run id. \nPlease provide a valid test run id along with test run command using -R flag and try again. for eg: pytest -X Y -R 100\n"+'\033[0m')
            testrail_flag = 'N'   
        if test_run_id is not None:
            test_obj.register_testrail()
            test_obj.set_test_run_id(test_run_id)

    if tesults_flag.lower()=='y':
        test_obj.register_tesults()
    
    yield test_obj
    
    #Teardown
    test_obj.wait(3)
    test_obj.teardown() 
   
@pytest.fixture
def test_mobile_obj(mobile_os_name, mobile_os_version, device_name, app_package, app_activity, remote_flag, device_flag, testrail_flag, tesults_flag, test_run_id,app_name,app_path):
    
    "Return an instance of Base Page that knows about the third party integrations"
    test_mobile_obj = PageFactory.get_page_object("Zero mobile")

    #Setup and register a driver
    test_mobile_obj.register_driver(mobile_os_name,mobile_os_version,device_name,app_package,app_activity,remote_flag,device_flag,app_name,app_path,ud_id,org_id,signing_id,no_reset_flag)

    #3. Setup TestRail reporting
    if testrail_flag.lower()=='y':
        if test_run_id is None:
            test_mobile_obj.write('\033[91m'+"\n\nTestRail Integration Exception: It looks like you are trying to use TestRail Integration without providing test run id. \nPlease provide a valid test run id along with test run command using -R flag and try again. for eg: pytest -X Y -R 100\n"+'\033[0m')
            testrail_flag = 'N'   
        if test_run_id is not None:
            test_mobile_obj.register_testrail()
            test_mobile_obj.set_test_run_id(test_run_id)

    if tesults_flag.lower()=='y':
        test_mobile_obj.register_tesults()

    yield test_mobile_obj
    
    #Teardown
    test_mobile_obj.wait(3)
    test_mobile_obj.teardown() 
   
@pytest.fixture
def browser(request):
    "pytest fixture for browser"
    return request.config.getoption("-B")


@pytest.fixture
def base_url(request):
    "pytest fixture for base url"
    return request.config.getoption("-U")


@pytest.fixture
def api_url(request):
    "pytest fixture for base url"
    return request.config.getoption("-A")
    

@pytest.fixture
def test_run_id(request):
    "pytest fixture for test run id"
    return request.config.getoption("-R")


@pytest.fixture
def testrail_flag(request):
    "pytest fixture for test rail flag"
    return request.config.getoption("-X")


@pytest.fixture
def remote_flag(request):
    "pytest fixture for browserstack/sauce flag"
    return request.config.getoption("-M")


@pytest.fixture
def browser_version(request):
    "pytest fixture for browser version"
    return request.config.getoption("-V") 


@pytest.fixture
def os_name(request):
    "pytest fixture for os_name"
    return request.config.getoption("-P") 


@pytest.fixture
def os_version(request):
    "pytest fixture for os version"
    return request.config.getoption("-O")


@pytest.fixture
def remote_project_name(request):
    "pytest fixture for browserStack project name"
    return request.config.getoption("--remote_project_name")


@pytest.fixture
def remote_build_name(request):
    "pytest fixture for browserStack build name"
    return request.config.getoption("--remote_build_name")


@pytest.fixture
def slack_flag(request):
    "pytest fixture for sending reports on slack"
    return request.config.getoption("-S")


@pytest.fixture
def tesults_flag(request):
    "pytest fixture for sending results to tesults"
    return request.config.getoption("--tesults")


@pytest.fixture
def mobile_os_name(request):
    "pytest fixture for mobile os name"
    return request.config.getoption("-G")


@pytest.fixture
def mobile_os_version(request):
    "pytest fixture for mobile os version"
    return request.config.getoption("-H")


@pytest.fixture
def device_name(request):
    "pytest fixture for device name"
    return request.config.getoption("-I")


@pytest.fixture
def app_package(request):
    "pytest fixture for app package"
    return request.config.getoption("-J")


@pytest.fixture
def app_activity(request):
    "pytest fixture for app activity"
    return request.config.getoption("-K")


@pytest.fixture
def device_flag(request):
    "pytest fixture for device flag"
    return request.config.getoption("-Q")


@pytest.fixture
def email_pytest_report(request):
    "pytest fixture for device flag"
    return request.config.getoption("--email_pytest_report")


@pytest.fixture
def app_name(request):
    "pytest fixture for app name"
    return request.config.getoption("-D")


@pytest.fixture
def ud_id(request):
    "pytest fixture for iOS udid"
    return request.config.getoption("--ud_id")


@pytest.fixture
def org_id(request):
    "pytest fixture for iOS team id"
    return request.config.getoption("--org_id")


@pytest.fixture
def signing_id(request):
    "pytest fixture for iOS signing id"
    return request.config.getoption("--signing_id")


@pytest.fixture
def no_reset_flag(request):
    "pytest fixture for no_reset_flag"
    return request.config.getoption("--no_reset_flag")


@pytest.fixture
def app_path(request):
    "pytest fixture for app path"
    return request.config.getoption("-N")    


def pytest_terminal_summary(terminalreporter, exitstatus):
    "add additional section in terminal summary reporting."
    if  terminalreporter.config.getoption("-S").lower() == 'y':
        post_test_reports_to_slack.post_reports_to_slack()
    elif terminalreporter.config.getoption("--email_pytest_report").lower() == 'y':
        #Initialize the Email_Pytest_Report object
        email_obj = Email_Pytest_Report()
        # Send html formatted email body message with pytest report as an attachment
        email_obj.send_test_report_email(html_body_flag=True,attachment_flag=True,report_file_path= 'default')

    if  terminalreporter.config.getoption("--tesults").lower() == 'y':
        Tesults.post_results_to_tesults()
        
def pytest_generate_tests(metafunc):
    "test generator function to run tests across different parameters"

    if 'browser' in metafunc.fixturenames:
        if metafunc.config.getoption("-M").lower() == 'y':               
            if metafunc.config.getoption("-B") == ["all"]:
                metafunc.parametrize("browser,browser_version,os_name,os_version", 
                                    browser_os_name_conf.cross_browser_cross_platform_config)
            elif metafunc.config.getoption("-B") == []:
                metafunc.parametrize("browser,browser_version,os_name,os_version", 
                                    browser_os_name_conf.default_config_list) 
            else:
                config_list = [(metafunc.config.getoption("-B")[0],metafunc.config.getoption("-V")[0],metafunc.config.getoption("-P")[0],metafunc.config.getoption("-O")[0])]
                metafunc.parametrize("browser,browser_version,os_name,os_version", 
                                    config_list) 
        if metafunc.config.getoption("-M").lower() !='y':
            if metafunc.config.getoption("-B") == ["all"]:
                metafunc.config.option.browser = browser_os_name_conf.local_browsers
                metafunc.parametrize("browser", metafunc.config.option.browser)
            elif metafunc.config.getoption("-B") == []:
                metafunc.parametrize("browser",browser_os_name_conf.default_browser)
            else:
                config_list_local = [(metafunc.config.getoption("-B")[0])]
                metafunc.parametrize("browser", config_list_local)          

def pytest_addoption(parser):
    parser.addoption("-B","--browser",
                      dest="browser",
                      action="append",
                      default=[],
                      help="Browser. Valid options are firefox, ie and chrome")                      
    parser.addoption("-U","--app_url",
                      dest="url",
                      default=base_url_conf.base_url,
                      help="The url of the application")
    parser.addoption("-A","--api_url",
                      dest="url",
                      default="http://35.167.62.251",
                      help="The url of the api")
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
    parser.addoption("--remote_project_name",
                      dest="remote_project_name",
                      help="The project name if its run in BrowserStack",
                      default=None)
    parser.addoption("--remote_build_name",
                      dest="remote_build_name",
                      help="The build name if its run in BrowserStack",
                      default=None)
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
                      default="8.0")
    parser.addoption("-I","--device_name",
                      dest="device_name",
                      help="Enter device name. Ex: Emulator, physical device name",
                      default="Google Pixel")
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
    parser.addoption("--email_pytest_report",
                      dest="email_pytest_report",
                      help="Email pytest report: Y or N",
                      default="N")
    parser.addoption("--tesults",
                      dest="tesults_flag",
                      default='N',
                      help="Y or N. 'Y' if you want to report results with Tesults")
    parser.addoption("-D","--app_name",
                      dest="app_name",
                      help="Enter application name to be uploaded.Ex:Bitcoin Info_com.dudam.rohan.bitcoininfo.apk.",
                      default="Bitcoin Info_com.dudam.rohan.bitcoininfo.apk")
    parser.addoption("--ud_id",
                      dest="ud_id",
                      help="Enter your iOS device UDID which is required to run appium test in iOS device",
                      default=None)
    parser.addoption("--org_id",
                      dest="org_id",
                      help="Enter your iOS Team ID which is required to run appium test in iOS device",
                      default=None)
    parser.addoption("--signing_id",
                      dest="signing_id",
                      help="Enter your iOS app signing id which is required to run appium test in iOS device",
                      default="iPhone Developer")
    parser.addoption("--no_reset_flag",
                      dest="no_reset_flag",
                      help="Pass false if you want to reset app eveytime you run app else false",
                      default="true")
    parser.addoption("-N","--app_path",
                      dest="app_path",
                      help="Enter app path")



