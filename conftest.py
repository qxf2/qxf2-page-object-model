import os,pytest,sys
import glob
import shutil
from loguru import logger
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from dotenv import load_dotenv
from page_objects.PageFactory import PageFactory
from conf import browser_os_name_conf
from conf import base_url_conf
from endpoints.API_Player import API_Player
from utils import interactive_mode

load_dotenv()

@pytest.fixture
def test_obj(base_url, browser, browser_version, os_version, os_name, remote_flag, testrail_flag, tesults_flag, test_run_id, remote_project_name, remote_build_name, testname, reportportal_service, interactivemode_flag):
    "Return an instance of Base Page that knows about the third party integrations"
    try:
        if interactivemode_flag.lower() == "y":
            default_flag = interactive_mode.set_default_flag_gui(browser, browser_version, os_version, os_name, remote_flag, testrail_flag, tesults_flag)
            if default_flag == False:
                browser,browser_version,remote_flag,os_name,os_version,testrail_flag,tesults_flag = interactive_mode.ask_questions_gui(browser,browser_version,os_version,os_name,remote_flag,testrail_flag,tesults_flag)

        test_obj = PageFactory.get_page_object("Zero",base_url=base_url)
        test_obj.set_calling_module(testname)
        #Setup and register a driver
        test_obj.register_driver(remote_flag, os_name, os_version, browser, browser_version, remote_project_name, remote_build_name, testname)

        #Setup TestRail reporting
        if testrail_flag.lower()=='y':
            if test_run_id is None:
                test_obj.write('\033[91m'+"\n\nTestRail Integration Exception: It looks like you are trying to use TestRail Integration without providing test run id. \nPlease provide a valid test run id along with test run command using --test_run_id and try again. for eg: pytest --testrail_flag Y --test_run_id 100\n"+'\033[0m')
                testrail_flag = 'N'
            if test_run_id is not None:
                test_obj.register_testrail()
                test_obj.set_test_run_id(test_run_id)

        if tesults_flag.lower()=='y':
            test_obj.register_tesults()

        if reportportal_service:
            test_obj.set_rp_logger(reportportal_service)

        yield test_obj

        #Teardown
        if os.getenv('REMOTE_BROWSER_PLATFORM') == 'LT' and remote_flag.lower() == 'y':
            if test_obj.pass_counter == test_obj.result_counter:
                test_obj.execute_javascript("lambda-status=passed")
                test_obj.teardown()
            else:
                test_obj.execute_javascript("lambda-status=failed")
                test_obj.teardown()

        elif os.getenv('REMOTE_BROWSER_PLATFORM') == 'BS' and remote_flag.lower() == 'y':
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
                    test_obj.write("Log file uploaded to BrowserStack session successfully.")
                else:
                    test_obj.write(f"Failed to upload log file. Status code: {response.status_code}",level='error')
                    test_obj.write(response.text,level='error')

            test_obj.teardown()

        else:
            test_obj.wait(3)
            test_obj.teardown()

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))
        if os.getenv('REMOTE_BROWSER_PLATFORM') == 'LT' and remote_flag.lower() == 'y':
            test_obj.execute_javascript("lambda-status=error")

@pytest.fixture
def test_mobile_obj(mobile_os_name, mobile_os_version, device_name, app_package, app_activity, remote_flag, device_flag, testrail_flag, tesults_flag, test_run_id, app_name, app_path, appium_version, interactivemode_flag, testname, remote_project_name, remote_build_name, orientation):

    "Return an instance of Base Page that knows about the third party integrations"
    try:

        if interactivemode_flag.lower()=="y":

            mobile_os_name, mobile_os_version, device_name, app_package, app_activity, remote_flag, device_flag, testrail_flag, tesults_flag, app_name, app_path=interactive_mode.ask_questions_mobile(mobile_os_name, mobile_os_version, device_name, app_package, app_activity, remote_flag, device_flag, testrail_flag, tesults_flag, app_name, app_path, orientation)

        test_mobile_obj = PageFactory.get_page_object("Zero mobile")
        test_mobile_obj.set_calling_module(testname)
        #Setup and register a driver
        test_mobile_obj.register_driver(mobile_os_name, mobile_os_version, device_name, app_package, app_activity, remote_flag, device_flag, app_name, app_path, ud_id,org_id, signing_id, no_reset_flag, appium_version, remote_project_name, remote_build_name, orientation)

        #3. Setup TestRail reporting
        if testrail_flag.lower()=='y':
            if test_run_id is None:
                test_mobile_obj.write('\033[91m'+"\n\nTestRail Integration Exception: It looks like you are trying to use TestRail Integration without providing test run id. \nPlease provide a valid test run id along with test run command using --test_run_id and try again. for eg: pytest --testrail_flag Y --test_run_id 100\n"+'\033[0m')
                testrail_flag = 'N'
            if test_run_id is not None:
                test_mobile_obj.register_testrail()
                test_mobile_obj.set_test_run_id(test_run_id)

        if tesults_flag.lower()=='y':
            test_mobile_obj.register_tesults()

        yield test_mobile_obj

        if os.getenv('REMOTE_BROWSER_PLATFORM') == 'BS' and remote_flag.lower() == 'y':
            response = upload_test_logs_to_browserstack(test_mobile_obj.log_name,test_mobile_obj.session_url,appium_test = True)
            if isinstance(response, dict) and "error" in response:
                # Handle the error response returned as a dictionary
                test_obj.write(f"Error: {response['error']}",level='error')
                if "details" in response:
                    test_obj.write(f"Details: {response['details']}",level='error')
                    test_obj.write("Failed to upload log file to BrowserStack",level='error')
            else:
                # Handle the case where the response is assumed to be a response object
                if response.status_code == 200:
                    test_mobile_obj.write("Log file uploaded to BrowserStack session successfully.")
                else:
                    test_mobile_obj.write(f"Failed to upload log file. Status code: {response.status_code}",level='error')
                    test_mobile_obj.write(response.text,level='error')

        #Teardown
        test_mobile_obj.wait(3)
        test_mobile_obj.teardown()

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))

@pytest.fixture
def test_api_obj(request, interactivemode_flag, api_url=base_url_conf.api_base_url):
    "Return an instance of Base Page that knows about the third party integrations"
    # request.module._name__ is tests.<module_name> strip and get the module name
    log_file = request.module.__name__.split('.')[-1] + '.log'
    try:
        if interactivemode_flag.lower()=='y':
            api_url,session_flag = interactive_mode.ask_questions_api(api_url)
            test_api_obj = API_Player(api_url,
                                      session_flag,
                                      log_file_path=log_file)
        else:
            test_api_obj = API_Player(url=api_url,
                                      session_flag=True,
                                      log_file_path=log_file)
        yield test_api_obj

    except Exception as e:
        print("Exception when trying to run test:%s" % __file__)
        print("Python says:%s" % str(e))

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

    except Exception as e:
        # Handle any other unexpected exceptions
        return {"error": "An unexpected error occurred while uploading logs to BrowserStack.", "details": str(e)}

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

@pytest.fixture
def interactivemode_flag(request):
    "pytest fixture for questionary module"
    try:
        return request.config.getoption("--interactive_mode_flag")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))

@pytest.fixture
def reportportal_service(request):
    "pytest service fixture for reportportal"
    reportportal_pytest_service = None
    try:
        if request.config.getoption("--reportportal"):
            reportportal_pytest_service = request.node.config.py_test_service
    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))
        solution = "It looks like you are trying to use report portal to run your test. \nPlease make sure you have updated .env with the right credentials ."
        print('\033[92m'+"\nSOLUTION: %s\n"%solution+'\033[0m')

    return reportportal_pytest_service

@pytest.fixture
def summary_flag(request):
    "pytest fixture for generating summary using LLM"
    try:
        return request.config.getoption("--summary")
    except Exception as error:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(error))

@pytest.fixture
def orientation(request):
    "pytest fixture for device orientation"
    try:
        return request.config.getoption("--orientation")

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))

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
                print(f"Error removing existing consolidated log file: {error}")

        # Delete all temporary log files if present
        for temp_log_file in glob.glob(os.path.join(source_directory, log_file_name)):
            try:
                os.remove(temp_log_file)
            except OSError as error:
                print(f"Error removing temporary log file: {error}")

def pytest_sessionfinish(session, exitstatus):
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
            with open(consolidated_log_file, "a") as final_log:
                for file_name in glob.glob(os.path.join(source_directory, log_file_name)):
                    source_file = None
                    try:
                        with open(file_name, "r") as source_file:
                            shutil.copyfileobj(source_file, final_log)
                        os.remove(file_name)
                    except FileNotFoundError as error:
                        print(f"Temporary log file not found: {error}")
                    except Exception as error:
                        print(f"Error processing the temporary log file: {error}")
        except OSError as error:
            print(f"Error processing consolidated log file: {error}")

@pytest.hookimpl()
def pytest_configure(config):
    "Sets the launch name based on the marker selected."
    global if_reportportal
    if_reportportal =config.getoption('--reportportal')

    try:
        config._inicache["rp_api_key"] = os.getenv('report_portal_api_key')
        config._inicache["rp_endpoint"]= os.getenv('report_portal_endpoint')
        config._inicache["rp_project"]=os.getenv('report_portal_project')
        config._inicache["rp_launch"]=os.getenv('report_portal_launch')

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
        if not hasattr(terminalreporter.config, 'workerinput'):
            if  terminalreporter.config.getoption("--slack_flag").lower() == 'y':
                from integrations.reporting_channels import post_test_reports_to_slack # pylint: disable=import-error,import-outside-toplevel
                post_test_reports_to_slack.post_reports_to_slack()
            if terminalreporter.config.getoption("--email_pytest_report").lower() == 'y':
                from integrations.reporting_channels.email_pytest_report import EmailPytestReport # pylint: disable=import-error,import-outside-toplevel
                #Initialize the Email_Pytest_Report object
                email_obj = EmailPytestReport()
                # Send html formatted email body message with pytest report as an attachment
                email_obj.send_test_report_email(html_body_flag=True,attachment_flag=True,report_file_path='default')
            if terminalreporter.config.getoption("--tesults").lower() == 'y':
                from integrations.reporting_tools import Tesults # pylint: disable=import-error,import-outside-toplevel
                Tesults.post_results_to_tesults()
            if  terminalreporter.config.getoption("--summary").lower() == 'y':
                from utils import gpt_summary_generator # pylint: disable=import-error,import-outside-toplevel
                gpt_summary_generator.generate_gpt_summary()
    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))
        solution = "It looks like you are trying to use email pytest report to run your test. \nPlease make sure you have updated .env with the right credentials ."
        print('\033[92m'+"\nSOLUTION: %s\n"%solution+'\033[0m')


def pytest_generate_tests(metafunc):
    "test generator function to run tests across different parameters"
    try:
        if 'browser' in metafunc.fixturenames:
            if metafunc.config.getoption("--remote_flag").lower() == 'y':
                if metafunc.config.getoption("--browser") == ["all"]:
                    metafunc.parametrize("browser,browser_version,os_name,os_version",
                                        browser_os_name_conf.cross_browser_cross_platform_config)
                elif not metafunc.config.getoption("--browser") or not metafunc.config.getoption("--ver") or not metafunc.config.getoption("--os_name") or not metafunc.config.getoption("--os_version"):
                    print("Feedback: Missing command-line arguments. Falling back to default values.")
                    # Use default values from the default list if not provided
                    default_config_list = browser_os_name_conf.default_config_list
                    config_list = []
                    if not metafunc.config.getoption("--browser"):
                        config_list.append(default_config_list[0][0])
                    else:
                        config_list.append(metafunc.config.getoption("--browser")[0])

                    if not metafunc.config.getoption("--ver"):
                        config_list.append(default_config_list[0][1])
                    else:
                        config_list.append(metafunc.config.getoption("--ver")[0])

                    if not metafunc.config.getoption("--os_name"):
                        config_list.append(default_config_list[0][2])
                    else:
                        config_list.append(metafunc.config.getoption("--os_name")[0])

                    if not metafunc.config.getoption("--os_version"):
                        config_list.append(default_config_list[0][3])
                    else:
                        config_list.append(metafunc.config.getoption("--os_version")[0])

                    metafunc.parametrize("browser, browser_version, os_name, os_version", [tuple(config_list)])
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
        parser.addoption("--browser",
                            dest="browser",
                            action="append",
                            default=[],
                            help="Browser. Valid options are firefox, ie and chrome")
        parser.addoption("--app_url",
                            dest="url",
                            default=base_url_conf.ui_base_url,
                            help="The url of the application")
        parser.addoption("--api_url",
                            dest="url",
                            default="https://cars-app.qxf2.com/",
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
                            help="Enter application name to be uploaded.Ex:Bitcoin Info_com.dudam.rohan.bitcoininfo.apk",
                            default="app-release-v1.2.apk")
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

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))
