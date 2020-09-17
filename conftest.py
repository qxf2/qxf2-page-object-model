import os,pytest,sys
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print(sys.path)
from page_objects.PageFactory import PageFactory
from conf import browser_os_name_conf
from conf import base_url_conf
from utils import post_test_reports_to_slack
from utils.email_pytest_report import Email_Pytest_Report
from utils import Tesults

@pytest.fixture
def test_obj(base_url,browser,browser_version,os_version,os_name,remote_flag,testrail_flag,tesults_flag,test_run_id,remote_project_name,remote_build_name,testname):
    "Return an instance of Base Page that knows about the third party integrations"
    try:
        test_obj = PageFactory.get_page_object("Zero",base_url=base_url)
        test_obj.set_calling_module(testname)
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

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))


@pytest.fixture
def test_mobile_obj(mobile_os_name, mobile_os_version, device_name, app_package, app_activity, remote_flag, device_flag, testrail_flag, tesults_flag, test_run_id,app_name,app_path,appium_version):

    "Return an instance of Base Page that knows about the third party integrations"
    try:
        test_mobile_obj = PageFactory.get_page_object("Zero mobile")

        #Setup and register a driver
        test_mobile_obj.register_driver(mobile_os_name,mobile_os_version,device_name,app_package,app_activity,remote_flag,device_flag,app_name,app_path,ud_id,org_id,signing_id,no_reset_flag,appium_version)

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

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))


@pytest.fixture
def testname(request):
    "pytest fixture for testname"
    try:
        name_of_test = request.node.name
        name_of_test = name_of_test.split('[')[0]

        return name_of_test

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))


@pytest.fixture
def browser(request):
    "pytest fixture for browser"
    try:
       return request.config.getoption("--browser")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))


@pytest.fixture
def base_url(request):
    "pytest fixture for base url"
    try:
        return request.config.getoption("--app_url")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))


@pytest.fixture
def api_url(request):
    "pytest fixture for base url"
    try:
        return request.config.getoption("--api_url")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))


@pytest.fixture
def test_run_id(request):
    "pytest fixture for test run id"
    try:
        return request.config.getoption("--test_run_id")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))


@pytest.fixture
def testrail_flag(request):
    "pytest fixture for test rail flag"
    try:
        return request.config.getoption("--testrail_flag")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))


@pytest.fixture
def remote_flag(request):
    "pytest fixture for browserstack/sauce flag"
    try:
        return request.config.getoption("--remote_flag")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))


@pytest.fixture
def browser_version(request):
    "pytest fixture for browser version"
    try:
        return request.config.getoption("--ver")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))


@pytest.fixture
def os_name(request):
    "pytest fixture for os_name"
    try:
        return request.config.getoption("--os_name")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))


@pytest.fixture
def os_version(request):
    "pytest fixture for os version"
    try:
        return request.config.getoption("--os_version")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))


@pytest.fixture
def remote_project_name(request):
    "pytest fixture for browserStack project name"
    try:
        return request.config.getoption("--remote_project_name")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))


@pytest.fixture
def remote_build_name(request):
    "pytest fixture for browserStack build name"
    try:
        return request.config.getoption("--remote_build_name")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))


@pytest.fixture
def slack_flag(request):
    "pytest fixture for sending reports on slack"
    try:
        return request.config.getoption("--slack_flag")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))


@pytest.fixture
def tesults_flag(request):
    "pytest fixture for sending results to tesults"
    try:
        return request.config.getoption("--tesults")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))


@pytest.fixture
def mobile_os_name(request):
    "pytest fixture for mobile os name"
    try:
        return request.config.getoption("--mobile_os_name")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))


@pytest.fixture
def mobile_os_version(request):
    "pytest fixture for mobile os version"
    try:
        return request.config.getoption("--mobile_os_version")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))


@pytest.fixture
def device_name(request):
    "pytest fixture for device name"
    try:
        return request.config.getoption("--device_name")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))


@pytest.fixture
def app_package(request):
    "pytest fixture for app package"
    try:
        return request.config.getoption("--app_package")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))


@pytest.fixture
def app_activity(request):
    "pytest fixture for app activity"
    try:
        return request.config.getoption("--app_activity")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))


@pytest.fixture
def device_flag(request):
    "pytest fixture for device flag"
    try:
        return request.config.getoption("--device_flag")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))


@pytest.fixture
def email_pytest_report(request):
    "pytest fixture for device flag"
    try:
        return request.config.getoption("--email_pytest_report")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))


@pytest.fixture
def app_name(request):
    "pytest fixture for app name"
    try:
        return request.config.getoption("--app_name")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))


@pytest.fixture
def ud_id(request):
    "pytest fixture for iOS udid"
    try:
        return request.config.getoption("--ud_id")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))


@pytest.fixture
def org_id(request):
    "pytest fixture for iOS team id"
    try:
        return request.config.getoption("--org_id")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))

@pytest.fixture
def signing_id(request):
    "pytest fixture for iOS signing id"
    try:
        return request.config.getoption("--signing_id")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))

@pytest.fixture
def appium_version(request):
    "pytest fixture for app name"
    try:
        return request.config.getoption("--appium_version")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))

@pytest.fixture
def no_reset_flag(request):
    "pytest fixture for no_reset_flag"
    try:
        return request.config.getoption("--no_reset_flag")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))

@pytest.fixture
def app_path(request):
    "pytest fixture for app path"
    try:
        return request.config.getoption("--app_path")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))

@pytest.hookimpl()
def pytest_configure(config):
    "Sets the launch name based on the marker selected."
    global if_reportportal
    if_reportportal =config.getoption('--reportportal')

    try:
        config._inicache["rp_uuid"]="34ec4436-1a3c-4079-9ca0-e177e530fa47"
        config._inicache["rp_endpoint"]="http://web.demo.reportportal.io"
        config._inicache["rp_project"]="personal"
        config._inicache["rp_launch"]="TEST_EXAMPLE"

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))

    #Registering custom markers to supress warnings
    config.addinivalue_line("markers", "GUI: mark a test as part of the GUI regression suite.")
    config.addinivalue_line("markers", "API: mark a test as part of the GUI regression suite.")
    config.addinivalue_line("markers", "MOBILE: mark a test as part of the GUI regression suite.")


def pytest_terminal_summary(terminalreporter, exitstatus):
    "add additional section in terminal summary reporting."
    try:
        if  terminalreporter.config.getoption("--slack_flag").lower() == 'y':
            post_test_reports_to_slack.post_reports_to_slack()
        if terminalreporter.config.getoption("--email_pytest_report").lower() == 'y':
            #Initialize the Email_Pytest_Report object
            email_obj = Email_Pytest_Report()
            # Send html formatted email body message with pytest report as an attachment
            email_obj.send_test_report_email(html_body_flag=True,attachment_flag=True,report_file_path='default')
        if terminalreporter.config.getoption("--tesults").lower() == 'y':
            Tesults.post_results_to_tesults()

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))


def pytest_generate_tests(metafunc):
    "test generator function to run tests across different parameters"
    try:
        if 'browser' in metafunc.fixturenames:
            if metafunc.config.getoption("--remote_flag").lower() == 'y':
                if metafunc.config.getoption("--browser") == ["all"]:
                    metafunc.parametrize("browser,browser_version,os_name,os_version",
                                        browser_os_name_conf.cross_browser_cross_platform_config)
                elif metafunc.config.getoption("--browser") == []:
                    metafunc.parametrize("browser,browser_version,os_name,os_version",
                                        browser_os_name_conf.default_config_list)
                else:
                    config_list = [(metafunc.config.getoption("--browser")[0],metafunc.config.getoption("--ver")[0],metafunc.config.getoption("--os_name")[0],metafunc.config.getoption("--os_version")[0])]
                    metafunc.parametrize("browser,browser_version,os_name,os_version",
                                        config_list)
            if metafunc.config.getoption("--remote_flag").lower() !='y':
                if metafunc.config.getoption("--browser") == ["all"]:
                    metafunc.config.option.browser = browser_os_name_conf.local_browsers
                    metafunc.parametrize("browser", metafunc.config.option.browser)
                elif metafunc.config.getoption("--browser") == []:
                    metafunc.parametrize("browser",browser_os_name_conf.default_browser)
                else:
                    config_list_local = [(metafunc.config.getoption("--browser")[0])]
                    metafunc.parametrize("browser", config_list_local)

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))




def pytest_addoption(parser):
    "Method to add the option to ini."
    try:
        parser.addini("rp_uuid",'help',type="pathlist")
        parser.addini("rp_endpoint",'help',type="pathlist")
        parser.addini("rp_project",'help',type="pathlist")
        parser.addini("rp_launch",'help',type="pathlist")

        parser.addoption("--browser",
                            dest="browser",
                            action="append",
                            default=[],
                            help="Browser. Valid options are firefox, ie and chrome")
        parser.addoption("--app_url",
                            dest="url",
                            default=base_url_conf.base_url,
                            help="The url of the application")
        parser.addoption("--api_url",
                            dest="url",
                            default="http://35.167.62.251",
                            help="The url of the api")
        parser.addoption("--testrail_flag",
                            dest="testrail_flag",
                            default='N',
                            help="Y or N. 'Y' if you want to report to TestRail")
        parser.addoption("--test_run_id",
                            dest="test_run_id",
                            default=None,
                            help="The test run id in TestRail")
        parser.addoption("--remote_flag",
                            dest="remote_flag",
                            default="N",
                            help="Run the test in Browserstack/Sauce Lab: Y or N")
        parser.addoption("--os_version",
                            dest="os_version",
                            action="append",
                            help="The operating system: xp, 7",
                            default=[])
        parser.addoption("--ver",
                            dest="browser_version",
                            action="append",
                            help="The version of the browser: a whole number",
                            default=[])
        parser.addoption("--os_name",
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
        parser.addoption("--slack_flag",
                            dest="slack_flag",
                            default="N",
                            help="Post the test report on slack channel: Y or N")
        parser.addoption("--mobile_os_name",
                            dest="mobile_os_name",
                            help="Enter operating system of mobile. Ex: Android, iOS",
                            default="Android")
        parser.addoption("--mobile_os_version",
                            dest="mobile_os_version",
                            help="Enter version of operating system of mobile: 8.1.0",
                            default="8.0")
        parser.addoption("--device_name",
                            dest="device_name",
                            help="Enter device name. Ex: Emulator, physical device name",
                            default="Samsung Galaxy S9")
        parser.addoption("--app_package",
                            dest="app_package",
                            help="Enter name of app package. Ex: bitcoininfo",
                            default="com.dudam.rohan.bitcoininfo")
        parser.addoption("--app_activity",
                            dest="app_activity",
                            help="Enter name of app activity. Ex: .MainActivity",
                            default=".MainActivity")
        parser.addoption("--device_flag",
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
        parser.addoption("--app_name",
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
        parser.addoption("--app_path",
                            dest="app_path",
                            help="Enter app path")
        parser.addoption("--appium_version",
                            dest="appium_version",
                            help="The appium version if its run in BrowserStack",
                            default="1.17.0")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))
