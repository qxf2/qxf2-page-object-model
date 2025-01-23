"""
Pytest configuration and shared fixtures

This module contains the common pytest fixtures, hooks, and utility functions
used throughout the test suite. These fixtures help to set up test dependencies
such as browser configurations, base URLs, and 
external services (e.g., BrowserStack, SauceLabs, TestRail, Report Portal, etc).
"""

import os
import sys
import glob
import shutil
import pytest
from loguru import logger
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from endpoints.api_player import APIPlayer        # pylint: disable=import-error wrong-import-position
from page_objects.PageFactory import PageFactory    # pylint: disable=import-error wrong-import-position
from utils import interactive_mode                  # pylint: disable=import-error wrong-import-position
from core_helpers.custom_pytest_plugins import CustomTerminalReporter # pylint: disable=import-error wrong-import-position
from core_helpers.logging_objects import Logging_Objects  # pylint: disable=import-error wrong-import-position

from conf.config_factory import ConfigFactory

load_dotenv()

@pytest.fixture
def testname(request):
    "pytest fixture for testname"
    name_of_test = request.node.name.split('[')[0]
    return name_of_test

@pytest.fixture
def config_factory(request, testname):
    "Config Factory fixture"
    return ConfigFactory(testname, request.config)

@pytest.fixture
def uitestconfig(config_factory):
   return config_factory.build_ui_config()
 
@pytest.fixture
def apitestconfig(config_factory):
    "API test config fixture"
    return config_factory.build_api_config()

@pytest.fixture
def mobiletestconfig(config_factory):
    "Mobile test config fixture"
    return config_factory.build_mobile_config()
    
@pytest.fixture
def test_obj(uitestconfig, 
             reportportal_service,
             interactivemode_flag,
             highlighter_flag,
             testreporter):
    "Return an instance of Base Page that knows about the third party integrations"
    # Test, Browser & Platform
    testname = uitestconfig.test.name
    base_url = uitestconfig.base_url.url
    browser = uitestconfig.browser.name
    browser_version = uitestconfig.browser.version
    os_name = uitestconfig.platform.name
    os_version = uitestconfig.platform.version
    # Remote test execution
    remote_flag = uitestconfig.remote_test_execution.flag
    remote_project_name = uitestconfig.remote_test_execution.browserstack.project_name
    remote_build_name = uitestconfig.remote_test_execution.browserstack.build_name
    # Reporting
    testrail_flag = uitestconfig.reporting.testrail.flag
    tesults_flag = uitestconfig.reporting.tesults.flag
    test_run_id = uitestconfig.reporting.testrail.test_run_id
    try:
        if interactivemode_flag.lower() == "y":
            default_flag = interactive_mode.set_default_flag_gui(browser, browser_version,
                                    os_version, os_name, remote_flag, testrail_flag, tesults_flag)
            if default_flag is False:
                browser,browser_version,remote_flag,os_name,os_version,testrail_flag,tesults_flag =\
                    interactive_mode.ask_questions_gui(browser,browser_version,os_version,os_name,
                                                       remote_flag,testrail_flag,tesults_flag)

        test_obj = PageFactory.get_page_object("Zero",base_url=base_url)   # pylint: disable=redefined-outer-name
        test_obj.set_calling_module(testname)
        #Setup and register a driver
        test_obj.register_driver(remote_flag, os_name, os_version, browser, browser_version,
                                remote_project_name, remote_build_name, testname)

        test_obj.write(f"Starting UI Test - {testname} Execution:")
        test_obj.write(uitestconfig)

        #Set highlighter
        if highlighter_flag.lower()=='y':
            test_obj.turn_on_highlight()

        #Setup TestRail reporting
        if testrail_flag.lower()=='y':
            if test_run_id is None:
                test_obj.write("\n\nTestRail Integration Exception:"\
                    " It looks like you are trying to use TestRail Integration without"\
                    " providing test run id. \nPlease provide a valid test run id along"\
                    " with test run command using --test_run_id and try again."\
                    " for eg: pytest --testrail_flag Y --test_run_id 100\n", level='critical')
                testrail_flag = 'N'
            if test_run_id is not None:
                test_obj.register_testrail()
                test_obj.set_test_run_id(test_run_id)

        if tesults_flag.lower()=='y':
            test_obj.register_tesults()

        if reportportal_service:
            test_obj.set_rp_logger(reportportal_service)

        yield test_obj

        # Collect the failed scenarios, these scenarios will be printed as table \
        # by the pytest's custom testreporter
        if test_obj.failed_scenarios:
            testreporter.failed_scenarios[testname] = test_obj.failed_scenarios

        if os.getenv('REMOTE_BROWSER_PLATFORM') == 'LT' and remote_flag.lower() == 'y':
            if test_obj.pass_counter == test_obj.result_counter:
                test_obj.execute_javascript("lambda-status=passed")
            else:
                test_obj.execute_javascript("lambda-status=failed")

        elif os.getenv('REMOTE_BROWSER_PLATFORM') == 'BS' and remote_flag.lower() == 'y':
            #Upload test logs to BrowserStack
            response = upload_test_logs_to_browserstack(test_obj.log_name,test_obj.session_url)
            if isinstance(response, dict) and "error" in response:
                # Handle the error response returned as a dictionary
                test_obj.write(f"Error: {response['error']}",level='error')
                if "details" in response:
                    test_obj.write(f"Details: {response['details']}",level='error')
                    test_obj.write("Failed to upload log file to BrowserStack",level='error')
            else:
                # Handle the case where the response is assumed to be a response object
                if response.status_code == 200:
                    test_obj.write("Log file uploaded to BrowserStack session successfully.",
                                   level='success')
                else:
                    test_obj.write(f"Failed to upload log file. Status code:{response.status_code}",
                                   level='error')
                    test_obj.write(response.text,level='error')

            #Update test run status to respective BrowserStack session
            if test_obj.pass_counter == test_obj.result_counter:
                test_obj.write("Test Status: PASS",level='success')
                result_flag = test_obj.execute_javascript("""browserstack_executor:
                        {"action": "setSessionStatus",
                        "arguments": {"status":"passed", "reason": "All test cases passed"}}""")
                test_obj.conditional_write(result_flag,
                        positive="Successfully set BrowserStack Test Session Status to PASS",
                        negative="Failed to set Browserstack session status to PASS")
            else:
                test_obj.write("Test Status: FAILED",level='error')
                result_flag = test_obj.execute_javascript("""browserstack_executor:
                             {"action": "setSessionStatus","arguments": {"status":"failed",
                              "reason": "Test failed. Look at terminal logs for more details"}}""")
                test_obj.conditional_write(result_flag,
                        positive="Successfully set BrowserStack Test Session Status to FAILED",
                        negative="Failed to set Browserstack session status to FAILED")
            test_obj.write("*************************")
        else:
            test_obj.wait(3)

        #Teardown
        test_obj.teardown()

    except Exception as e:      # pylint: disable=broad-exception-caught
        print(Logging_Objects.color_text(f"Exception when trying to run test:{__file__}","red"))
        print(Logging_Objects.color_text(f"Python says:{str(e)}","red"))
        if os.getenv('REMOTE_BROWSER_PLATFORM') == 'LT' and remote_flag.lower() == 'y':
            test_obj.execute_javascript("lambda-status=error")
        elif os.getenv('REMOTE_BROWSER_PLATFORM') == 'BS' and remote_flag.lower() == 'y':
            test_obj.execute_javascript("""browserstack_executor: {"action": "setSessionStatus",
                        "arguments": {"status":"failed", "reason": "Exception occured"}}""")
        if browser.lower() == "edge":
            print(Logging_Objects.color_text("Selenium Manager requires administrator permissions"\
                                        " to install Microsoft Edge in Windows automatically."))

@pytest.fixture
def test_mobile_obj(mobiletestconfig, interactivemode_flag, testreporter):
    "Return an instance of Base Page that knows about the third party integrations"
    try:
        testname = mobiletestconfig.test.name
        mobile_os_name = mobiletestconfig.mobile_os.name
        mobile_os_version = mobiletestconfig.mobile_os.version
        device_name = mobiletestconfig.mobile_device.name
        device_flag = mobiletestconfig.mobile_device.flag
        app_package = mobiletestconfig.mobile_app.package
        app_activity = mobiletestconfig.mobile_app.activity
        remote_flag = mobiletestconfig.remote_test_execution.flag
        remote_build_name = mobiletestconfig.remote_test_execution.browserstack.build_name
        remote_project_name = mobiletestconfig.remote_test_execution.browserstack.project_name
        tesults_flag = mobiletestconfig.reporting.tesults.flag
        app_name = mobiletestconfig.mobile_app.name
        app_path = mobiletestconfig.mobile_app.path
        ud_id = mobiletestconfig.ios_config.ud_id
        org_id = mobiletestconfig.ios_config.org_id
        signing_id = mobiletestconfig.ios_config.signing_id
        no_reset_flag = mobiletestconfig.mobile_app.no_reset_flag
        orientation = mobiletestconfig.mobile_app.orientation
        appium_version = mobiletestconfig.appium_config.version
        test_run_id = mobiletestconfig.reporting.testrail.test_run_id
        testrail_flag = mobiletestconfig.reporting.testrail.flag


        if interactivemode_flag.lower()=="y":

            mobile_os_name, mobile_os_version, device_name, app_package, app_activity, \
            remote_flag, device_flag, testrail_flag, tesults_flag, app_name, app_path= \
            interactive_mode.ask_questions_mobile(mobile_os_name, mobile_os_version, device_name,
                            app_package, app_activity, remote_flag, device_flag, testrail_flag,
                              tesults_flag, app_name, app_path, orientation)

        test_mobile_obj = PageFactory.get_page_object("Zero mobile")  # pylint: disable=redefined-outer-name
        test_mobile_obj.set_calling_module(testname)
        #Setup and register a driver
        test_mobile_obj.register_driver(mobile_os_name, mobile_os_version, device_name,
                        app_package, app_activity, remote_flag, device_flag, app_name,
                        app_path, ud_id,org_id, signing_id, no_reset_flag, appium_version,
                        remote_project_name, remote_build_name, orientation)

        test_mobile_obj.write(f"Starting Mobile test - {testname} Execution:")
        test_mobile_obj.write(mobiletestconfig)

        #3. Setup TestRail reporting
        if testrail_flag.lower()=='y':
            if test_run_id is None:
                test_mobile_obj.write("\n\nTestRail Integration Exception: "\
                    "It looks like you are trying to use TestRail Integration "\
                    "without providing test run id. \nPlease provide a valid test run id "\
                    "along with test run command using --test_run_id and try again."\
                    " for eg: pytest --testrail_flag Y --test_run_id 100\n",level='critical')
                testrail_flag = 'N'
            if test_run_id is not None:
                test_mobile_obj.register_testrail()
                test_mobile_obj.set_test_run_id(test_run_id)

        if tesults_flag.lower()=='y':
            test_mobile_obj.register_tesults()

        yield test_mobile_obj

        # Collect the failed scenarios, these scenarios will be printed as table \
        # by the pytest's custom testreporter
        if test_mobile_obj.failed_scenarios:
            testreporter.failed_scenarios[testname] = test_mobile_obj.failed_scenarios

        if os.getenv('REMOTE_BROWSER_PLATFORM') == 'BS' and remote_flag.lower() == 'y':
            response = upload_test_logs_to_browserstack(test_mobile_obj.log_name,
                                                        test_mobile_obj.session_url,
                                                        appium_test = True)
            if isinstance(response, dict) and "error" in response:
                # Handle the error response returned as a dictionary
                test_mobile_obj.write(f"Error: {response['error']}",level='error')
                if "details" in response:
                    test_mobile_obj.write(f"Details: {response['details']}",level='error')
                    test_mobile_obj.write("Failed to upload log file to BrowserStack",level='error')
            else:
                # Handle the case where the response is assumed to be a response object
                if response.status_code == 200:
                    test_mobile_obj.write("Log file uploaded to BrowserStack session successfully.",
                                          level='success')
                else:
                    test_mobile_obj.write("Failed to upload log file. "\
                                          f"Status code: {response.status_code}",level='error')
                    test_mobile_obj.write(response.text,level='error')
            #Update test run status to respective BrowserStack session
            if test_mobile_obj.pass_counter == test_mobile_obj.result_counter:
                test_mobile_obj.write("Test Status: PASS",level='success')
                result_flag = test_mobile_obj.execute_javascript("""browserstack_executor:
                                {"action": "setSessionStatus", "arguments": {"status":"passed",
                                "reason": "All test cases passed"}}""")
                test_mobile_obj.conditional_write(result_flag,
                            positive="Successfully set BrowserStack Test Session Status to PASS",
                            negative="Failed to set Browserstack session status to PASS")
            else:
                test_mobile_obj.write("Test Status: FAILED",level='error')
                result_flag = test_mobile_obj.execute_javascript("""browserstack_executor:
                            {"action": "setSessionStatus", "arguments": {"status":"failed",
                            "reason": "Test failed. Look at terminal logs for more details"}}""")
                test_mobile_obj.conditional_write(result_flag,
                            positive="Successfully set BrowserStack Test Session Status to FAILED",
                            negative="Failed to set Browserstack session status to FAILED")
            test_mobile_obj.write("*************************")
        #Teardown
        test_mobile_obj.wait(3)
        test_mobile_obj.teardown()

    except Exception as e:                      # pylint: disable=broad-exception-caught
        print(Logging_Objects.color_text(f"Exception when trying to run test:{__file__}","red"))
        print(Logging_Objects.color_text(f"Python says:{str(e)}","red"))
        if os.getenv('REMOTE_BROWSER_PLATFORM') == 'BS' and remote_flag.lower() == 'y':
            test_mobile_obj.execute_javascript("""browserstack_executor:
                            {"action": "setSessionStatus", "arguments":
                            {"status":"failed", "reason": "Exception occured"}}""")

@pytest.fixture
def test_api_obj(interactivemode_flag, testname, api_url):  # pylint: disable=redefined-outer-name
    "Return an instance of Base Page that knows about the third party integrations"
    api_url = apitestconfig.api_url.url
    testname = apitestconfig.test.name
    log_file = testname + '.log'
    try:
        if interactivemode_flag.lower()=='y':
            api_url,session_flag = interactive_mode.ask_questions_api(api_url)
            test_api_obj = APIPlayer(api_url,                                         # pylint: disable=redefined-outer-name
                                      log_file_path=log_file)
        else:
            test_api_obj = APIPlayer(url=api_url,
                                      log_file_path=log_file)
        yield test_api_obj

    except Exception as e:                    # pylint: disable=broad-exception-caught
        print(Logging_Objects.color_text(f"Exception when trying to run test:{__file__}","red"))
        print(Logging_Objects.color_text(f"Python says:{str(e)}","red"))

def upload_test_logs_to_browserstack(log_name, session_url, appium_test = False):
    "Upload log file to provided BrowserStack session"
    try:
        from integrations.cross_browsers.BrowserStack_Library import BrowserStack_Library # pylint: disable=import-error,import-outside-toplevel
        # Initialize BrowserStack object
        browserstack_obj = BrowserStack_Library()

        # Build log file path
        log_file_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'log'))
        log_file = log_file_dir + os.sep + 'temp_' + log_name

        # Check if the log file exists
        if not os.path.isfile(log_file):
            raise FileNotFoundError(f"Log file '{log_file}' not found.")

        # Extract session ID from the provided session URL
        session_id = browserstack_obj.extract_session_id(session_url)
        if not session_id:
            raise ValueError(f"Invalid session URL provided: '{session_url}'")

        # Upload the log file to BrowserStack
        response = browserstack_obj.upload_terminal_logs(log_file,session_id,appium_test)

        return response

    except ImportError as e:
        return {"error": "Failed to import BrowserStack_Library.", "details": str(e)}

    except FileNotFoundError as e:
        return {"error": "Log file not found.", "details": str(e)}

    except ValueError as e:
        return {"error": "Invalid session URL.", "details": str(e)}

    except Exception as e:                                     # pylint: disable=broad-exception-caught
        # Handle any other unexpected exceptions
        return {"error": "An unexpected error occurred while uploading logs"\
                " to BrowserStack.", "details": str(e)}

@pytest.fixture
def testreporter(request):
    "pytest summary reporter"
    return request.config.pluginmanager.get_plugin("terminalreporter")

@pytest.fixture
def highlighter_flag(request):
    "pytest fixture for element highlighter flag"
    return request.config.getoption("--highlighter_flag")

@pytest.fixture
def slack_flag(request):
    "pytest fixture for sending reports on slack"
    return request.config.getoption("--slack_flag")

@pytest.fixture
def email_pytest_report(request):
    "pytest fixture for device flag"
    return request.config.getoption("--email_pytest_report")

@pytest.fixture
def interactivemode_flag(request):
    "pytest fixture for questionary module"
    return request.config.getoption("--interactive_mode_flag")

@pytest.fixture
def reportportal_service(request):
    "pytest service fixture for reportportal"
    try:
        reportportal_pytest_service = None
        if request.config.getoption("--reportportal"):
            reportportal_pytest_service = request.node.config.py_test_service

    except Exception as e:                  # pylint: disable=broad-exception-caught
        print(Logging_Objects.color_text(f"Exception when trying to run test:{__file__}","red"))
        print(Logging_Objects.color_text(f"Python says:{str(e)}","red"))
        solution = "It looks like you are trying to use report portal to run your test."\
            "\nPlease make sure you have updated .env with the right credentials."
        print(Logging_Objects.color_text(f"\nSOLUTION: {solution}\n", "green"))

    return reportportal_pytest_service

@pytest.fixture
def summary_flag(request):
    "pytest fixture for generating summary using LLM"
    return request.config.getoption("--summary")

def pytest_sessionstart(session):
    """
    Perform cleanup at the start of the test session.
    Delete the consolidated log file and temporary log files if present.
    """
    if not hasattr(session.config, "workerinput"):  # Executes during the main session only
        source_directory = "log"
        log_file_name = "temp_*.log"
        consolidated_log_file = os.path.join(source_directory, "consolidated_log.txt")

        # Delete the consolidated log file
        if os.path.exists(consolidated_log_file):
            try:
                os.remove(consolidated_log_file)
            except OSError as error:
                print(Logging_Objects.color_text(
                    f"Error removing existing consolidated log file: {error}"))

        # Delete all temporary log files if present
        for temp_log_file in glob.glob(os.path.join(source_directory, log_file_name)):
            try:
                os.remove(temp_log_file)
            except OSError as error:
                print(Logging_Objects.color_text(f"Error removing temporary log file: {error}"))

def pytest_sessionfinish(session):
    """
    Called after the entire test session finishes.
    The temporary log files are consolidated into a single log file 
    and later deleted.
    """
    if not hasattr(session.config, "workerinput"):  # Executes during the main session only
        source_directory = "log"
        log_file_name = "temp_*.log"
        consolidated_log_file = os.path.join(source_directory, "consolidated_log.txt")

        #Detach all handlers from the logger inorder to release the file handle
        #which can be used for deleting the temp files later
        logger.remove(None)

        #Consolidate the temporary log files into the consolidated log file
        try:
            with open(consolidated_log_file, "a", encoding="utf-8") as final_log:
                for file_name in glob.glob(os.path.join(source_directory, log_file_name)):
                    source_file = None
                    try:
                        with open(file_name, "r", encoding="utf-8") as source_file:
                            shutil.copyfileobj(source_file, final_log)
                        os.remove(file_name)
                    except FileNotFoundError as error:
                        print(Logging_Objects.color_text(f"Temporary log file not found: {error}"))
                    except Exception as error:      # pylint: disable=broad-exception-caught
                        print(Logging_Objects.color_text(
                                f"Error processing the temporary log file: {error}"))
        except OSError as error:
            print(Logging_Objects.color_text(f"Error processing consolidated log file: {error}"))

@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    "Sets the launch name based on the marker selected."
    global if_reportportal   # pylint: disable=global-variable-undefined
    if_reportportal =config.getoption('--reportportal')

    # Unregister the old terminalreporter plugin
    # Register the custom terminalreporter plugin
    if config.pluginmanager.has_plugin("terminalreporter"):
        old_reporter = config.pluginmanager.get_plugin("terminalreporter")
        config.pluginmanager.unregister(old_reporter, "terminalreporter")
        reporter = CustomTerminalReporter(config)
        config.pluginmanager.register(reporter, "terminalreporter")

    try:
        config._inicache["rp_api_key"] = os.getenv('report_portal_api_key')   # pylint: disable=protected-access
        config._inicache["rp_endpoint"]= os.getenv('report_portal_endpoint')  # pylint: disable=protected-access
        config._inicache["rp_project"]= os.getenv('report_portal_project')    # pylint: disable=protected-access
        config._inicache["rp_launch"]= os.getenv('report_portal_launch')      # pylint: disable=protected-access

    except Exception as e:          # pylint: disable=broad-exception-caught
        print(Logging_Objects.color_text(f"Exception when trying to run test:{__file__}","red"))
        print(Logging_Objects.color_text(f"Python says:{str(e)}","red"))

    #Registering custom markers to supress warnings
    config.addinivalue_line("markers", "GUI: mark a test as part of the GUI regression suite.")
    config.addinivalue_line("markers", "API: mark a test as part of the GUI regression suite.")
    config.addinivalue_line("markers", "MOBILE: mark a test as part of the GUI regression suite.")

def pytest_terminal_summary(terminalreporter):
    "add additional section in terminal summary reporting."
    try:
        if not hasattr(terminalreporter.config, 'workerinput'):
            if  terminalreporter.config.getoption("--slack_flag").lower() == 'y':
                from integrations.reporting_channels import post_test_reports_to_slack # pylint: disable=import-error,import-outside-toplevel
                post_test_reports_to_slack.post_reports_to_slack()
            if terminalreporter.config.getoption("--email_pytest_report").lower() == 'y':
                from integrations.reporting_channels.email_pytest_report import EmailPytestReport # pylint: disable=import-error,import-outside-toplevel
                #Initialize the Email_Pytest_Report object
                email_obj = EmailPytestReport()
                # Send html formatted email body message with pytest report as an attachment
                email_obj.send_test_report_email(html_body_flag=True,attachment_flag=True,
                                                 report_file_path='default')
            if terminalreporter.config.getoption("--tesults").lower() == 'y':
                from integrations.reporting_tools import Tesults # pylint: disable=import-error,import-outside-toplevel
                Tesults.post_results_to_tesults()
            if  terminalreporter.config.getoption("--summary").lower() == 'y':
                from utils import gpt_summary_generator # pylint: disable=import-error,import-outside-toplevel
                gpt_summary_generator.generate_gpt_summary()
    except Exception as e:                  # pylint: disable=broad-exception-caught
        print(Logging_Objects.color_text(f"Exception when trying to run test:{__file__}","red"))
        print(Logging_Objects.color_text(f"Python says:{str(e)}","red"))
        solution = "It looks like you are trying to use email pytest report to run your test." \
                   "\nPlease make sure you have updated .env with the right credentials ."
        print(Logging_Objects.color_text(f"\nSOLUTION: {solution}\n","green"))


def pytest_generate_tests(metafunc):
    "test generator function to run tests across different parameters"
    try:
        if metafunc.config.getoption("browser"):
            if len(metafunc.config.getoption("browser")) > 1 or \
            metafunc.config.getoption("browser")[0].lower() == "all":
                if "uitestconfig" in metafunc.fixturenames:
                    testname = metafunc.definition.name
                    config_factory = ConfigFactory(testname, metafunc.config)
                    configs = config_factory.build_iterative_ui_config()
                    metafunc.parametrize("uitestconfig", configs)
    except Exception as e:              # pylint: disable=broad-exception-caught
        print(Logging_Objects.color_text(f"Exception when trying to run test:{__file__}","red"))
        print(Logging_Objects.color_text(f"Python says:{str(e)}","red"))

def pytest_addoption(parser):
    "Method to add the option to ini."
    try:
        parser.addoption("--browser",
                            dest="browser",
                            action="append",
                            default=[],
                            help="Browser. Valid options are firefox, Edge and chrome")
        parser.addoption("--app_url",
                            dest="url",
                            default=ConfigFactory.get_default_ui_url(),
                            help="The url of the application")
        parser.addoption("--api_url",
                            dest="api_url",
                            default=ConfigFactory.get_default_api_url(),
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
                            default="latest")
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
                            help="Enter version of operating system of mobile: 11.0",
                            default="11.0")
        parser.addoption("--device_name",
                            dest="device_name",
                            help="Enter device name. Ex: Emulator, physical device name",
                            default="Samsung Galaxy S21")
        parser.addoption("--app_package",
                            dest="app_package",
                            help="Enter name of app package. Ex: com.dudam.rohan.bitcoininfo",
                            default="com.qxf2.weathershopper")
        parser.addoption("--app_activity",
                            dest="app_activity",
                            help="Enter name of app activity. Ex: .MainActivity",
                            default=".MainActivity")
        parser.addoption("--device_flag",
                            dest="device_flag",
                            help="Enter Y or N. 'Y' if you want to run the test on device." \
                                 "'N' if you want to run the test on emulator.",
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
                            help="Enter application name to be uploaded." \
                                "Ex:Bitcoin Info_com.dudam.rohan.bitcoininfo.apk",
                            default="app-release-v1.2.apk")
        parser.addoption("--ud_id",
                            dest="ud_id",
                            help="Enter your iOS device UDID which is required" \
                                "to run appium test in iOS device",
                            default=None)
        parser.addoption("--org_id",
                            dest="org_id",
                            help="Enter your iOS Team ID which is required" \
                                 "to run appium test in iOS device",
                            default=None)
        parser.addoption("--signing_id",
                            dest="signing_id",
                            help="Enter your iOS app signing id which is required" \
                                 "to run appium test in iOS device",
                            default="iPhone Developer")
        parser.addoption("--no_reset_flag",
                            dest="no_reset_flag",
                            help="Pass false if you want to reset app eveytime you run app",
                            default="true")
        parser.addoption("--app_path",
                            dest="app_path",
                            help="Enter app path")
        parser.addoption("--appium_version",
                            dest="appium_version",
                            help="The appium version if its run in BrowserStack",
                            default="2.4.1")
        parser.addoption("--interactive_mode_flag",
                            dest="questionary",
                            default="n",
                            help="set the questionary flag")
        parser.addoption("--summary",
                            dest="summary",
                            default="n",
                            help="Generate pytest results summary using LLM (GPT): y or n")
        parser.addoption("--orientation",
                            dest="orientation",
                            default=None,
                            help="Enter LANDSCAPE to change device orientation to landscape")
        parser.addoption("--highlighter_flag",
                            dest="highlighter_flag",
                            default='N',
                            help="Y or N. 'Y' if you want turn on element highlighter")

    except Exception as e:              # pylint: disable=broad-exception-caught
        print(Logging_Objects.color_text(f"Exception when trying to run test:{__file__}","red"))
        print(Logging_Objects.color_text(f"Python says:{str(e)}","red"))
