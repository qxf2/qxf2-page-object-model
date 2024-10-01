"""
DriverFactory class
This module gets the webdrivers for different browsers and sets up the remote testing platforms for automation tests and mobile tests.
"""
import os
import sys
from dotenv import load_dotenv
from integrations.cross_browsers.remote_options import RemoteOptions
from .local_options import LocalOptions
from conf import ports_conf
from integrations.cross_browsers.lambdatest_runner import LambdaTestRunner

load_dotenv('.env.remote')
localhost_url = 'http://localhost:%s'%ports_conf.port #Set the url of localhost

class DriverFactory(RemoteOptions, LocalOptions):
    """Class contains methods for getting web drivers and setting up remote testing platforms."""

    def __init__(self, browser='ff', browser_version=None, os_name=None):
        """Constructor for the Driver factory."""
        self.browser = browser
        self.browser_version = browser_version
        self.os_name = os_name

    def get_web_driver(self, remote_flag, os_name, os_version, browser,
                       browser_version, remote_project_name, remote_build_name, testname):
        """Return the appropriate driver."""
        session_url = None
        if remote_flag.lower() == 'y':
            web_driver, session_url = self.select_remote_platform(remote_flag, os_name, os_version,
                                                     browser, browser_version, remote_project_name,
                                                     remote_build_name, testname)

        elif remote_flag.lower() == 'n':
            web_driver = self.get_local_driver(browser, browser_version)

        return web_driver,session_url

    def select_remote_platform(self, remote_flag, os_name, os_version, browser,
                               browser_version, remote_project_name, remote_build_name, testname):
        """Select the remote platform to run the test when the remote_flag is Y."""
        try:
            session_url = None
            if os.getenv('REMOTE_BROWSER_PLATFORM') == 'BS':
                from integrations.cross_browsers.browserstack_runner import BrowserStackRunner
                runner = BrowserStackRunner()
                web_driver,session_url = runner.get_browserstack_webdriver(os_name, os_version, browser, browser_version,
                                                    remote_project_name, remote_build_name)
            elif os.getenv('REMOTE_BROWSER_PLATFORM') == 'LT':
                runner = LambdaTestRunner()
                web_driver,session_url = runner.get_lambdatest_webdriver(os_name, os_version, browser, browser_version,
                                                    remote_project_name, remote_build_name, testname)
            else:
                from integrations.cross_browsers.saucelab_runner import SauceLabRunner
                runner = SauceLabRunner()
                web_driver = runner.get_saucelab_webdriver(os_name, os_version, browser, browser_version)

        except Exception as exception:
            self.print_exception(exception, remote_flag)

        return web_driver,session_url

    def get_local_driver(self, browser, browser_version):
        """Run the test on local system."""
        local_driver = None
        if browser_version == []:
            browser_version = None
        if browser.lower() == "ff" or browser.lower() == 'firefox':
            local_driver = self.firefox_local(browser_version)
        elif  browser.lower() == "edge":
            local_driver = self.edge_local(browser_version)
        elif browser.lower() == "chrome":
            local_driver = self.chrome_local(browser_version)
        elif browser.lower() == "opera":
            local_driver = self.opera_local()
        elif browser.lower() == "safari":
            local_driver = self.safari_local()
        elif browser.lower() == "headless-chrome":
            local_driver = self.headless_chrome(browser_version)

        return local_driver

    def get_mobile_driver(self, mobile_os_name, mobile_os_version, device_name, app_package,
                   app_activity, remote_flag, device_flag, app_name, app_path,
                   ud_id, org_id, signing_id, no_reset_flag, appium_version, remote_project_name, remote_build_name, orientation):
        """Specify the mobile device configurations and get the mobile driver."""
        #setup mobile device
        desired_capabilities = self.set_mobile_device(mobile_os_name, mobile_os_version, device_name, orientation)

        if remote_project_name is not None:
            desired_capabilities = self.remote_project_name(desired_capabilities, remote_project_name)

        #Set remote build name
        if remote_build_name is not None:
            desired_capabilities = self.remote_build_name(desired_capabilities, remote_build_name)

        #Check wether the OS is android or iOS and get the mobile driver
        if mobile_os_name in 'Android':
            mobile_driver,session_url = self.get_android_driver(remote_flag, desired_capabilities, app_path, app_name,
                                         appium_version, app_package, app_activity, device_flag)

        elif mobile_os_name == 'iOS':
            mobile_driver,session_url = self.get_ios_driver(remote_flag, desired_capabilities, app_path, app_name,
                                         app_package, no_reset_flag, ud_id, org_id, signing_id, appium_version)

        return mobile_driver,session_url

    def get_android_driver(self, remote_flag, desired_capabilities, app_path, app_name, appium_version,
                app_package, app_activity, device_flag):
        """Gets mobile driver for either local or remote setup of Android devices."""
        session_url = None
        #Get the driver when test is run on a remote platform
        if remote_flag.lower() == 'y':
            mobile_driver,session_url = self.remote_mobile_platform(remote_flag, app_path, app_name, desired_capabilities,
                                                        appium_version)

        #Get the driver when test is run on local setup
        else:
            try:
                desired_capabilities = self.app_details(desired_capabilities,app_package, app_activity)
                if device_flag.lower() == 'y':
                    mobile_driver = self.set_capabilities_options(desired_capabilities,url=localhost_url)
                else:
                    desired_capabilities = self.app_name(desired_capabilities, app_path, app_name)
                    mobile_driver = self.set_capabilities_options(desired_capabilities, url=localhost_url)
            except Exception as exception:
                self.print_exception(exception, remote_flag)

        return mobile_driver,session_url

    def get_ios_driver(self, remote_flag, desired_capabilities, app_path, app_name,app_package, no_reset_flag,
                        ud_id, org_id, signing_id, appium_version):
        """Gets mobile driver for either local or remote setup of Android devices."""
        #Get the driver when test is run on a remote platform
        session_url = None
        if remote_flag.lower() == 'y':
            mobile_driver,session_url = self.remote_mobile_platform(remote_flag, app_path, app_name,
                                                        desired_capabilities, appium_version)

        #Get the driver when test is run on local setup
        else:
            try:
                desired_capabilities = self.app_name(desired_capabilities, app_path, app_name)
                desired_capabilities = self.ios_capabilities(desired_capabilities, app_package, no_reset_flag, ud_id, org_id, signing_id)
                mobile_driver = self.set_capabilities_options(desired_capabilities, url=localhost_url)
            except Exception as exception:
                self.print_exception(exception, remote_flag)

        return mobile_driver,session_url

    def remote_mobile_platform(self, remote_flag, app_path, app_name, desired_capabilities, appium_version):
        """
        Checks wether the test is to be run on either browserstack or saucelab and gets the
        remote mobile driver.
        """
        try:
            session_url = None
            #Gets driver when test is run on Saucelab
            if os.getenv('REMOTE_BROWSER_PLATFORM') == 'SL':
                from integrations.cross_browsers.saucelab_runner import SauceLabRunner
                runner = SauceLabRunner()
                mobile_driver = runner.get_saucelab_mobile_driver(app_path, app_name, desired_capabilities)
            #Gets driver when test is run on Browserstack
            else:
                from integrations.cross_browsers.browserstack_runner import BrowserStackRunner
                runner = BrowserStackRunner()
                mobile_driver,session_url = runner.get_browserstack_mobile_driver(app_path, app_name, desired_capabilities,
                                                                        appium_version)
        except Exception as exception:
            self.print_exception(exception, remote_flag)

        return mobile_driver,session_url

    @staticmethod
    def print_exception(exception, remote_flag):
        """Print out the exception message and suggest the solution based on the remote flag."""
        if remote_flag.lower() == 'y':
            solution = "It looks like you are trying to use a cloud service provider(BrowserStack or Sauce Labs) to run your test. \nPlease make sure you have updated .env.remote with the right credentials and also check for BrowserStack upload url changes and try again. \nTo use your local browser please run the test with the --remote_flag N flag"
        else:
            solution = "It looks like you are trying to run test cases with Local Appium Setup. \nPlease make sure to run Appium Server and try again."

        print('\033[91m'+"\nException when trying to get remote webdriver:%s"%sys.modules[__name__]+'\033[0m')
        print('\033[91m'+"\nPython says:%s"%str(exception)+'\033[0m')
        print('\033[92m'+"\nSOLUTION: %s\n"%solution+'\033[0m')
