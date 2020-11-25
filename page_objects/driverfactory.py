"""
DriverFactory class
This module gets the webdrivers for different browsers and sets up the remote testing platforms for automation tests and mobile tests.
"""
import os
import sys
from selenium import webdriver
from selenium.webdriver.remote.webdriver import RemoteConnection
from appium import webdriver as mobile_webdriver
from conf import remote_credentials
from page_objects.drivers.remote_options import RemoteOptions
from page_objects.drivers.local_browsers import LocalBrowsers
from conf import ports_conf

localhost_url = 'http://localhost:%s/wd/hub'%ports_conf.port #Set the url of localhost

class DriverFactory(RemoteOptions, LocalBrowsers):
    """Class contains methods for getting web drivers and setting up remote testing platforms."""

    def __init__(self, browser='ff', browser_version=None, os_name=None):
        """Constructor for the Driver factory."""
        self.browser = browser
        self.browser_version = browser_version
        self.os_name = os_name


    def get_web_driver(self, remote_flag, os_name, os_version, browser,
                       browser_version, remote_project_name, remote_build_name):
        """Return the appropriate driver."""
        if remote_flag.lower() == 'y':
            web_driver = self.select_remote_platform(remote_flag, os_name, os_version,
                                                     browser, browser_version, remote_project_name,
                                                     remote_build_name)

        elif remote_flag.lower() == 'n':
            web_driver = self.run_local(browser)

        return web_driver


    def get_browser(self, browser, browser_version):
        """Select the browser."""

        if browser.lower() == 'ff' or browser.lower() == 'firefox':
            desired_capabilities = self.firefox(browser_version)
        elif browser.lower() == 'ie':
            desired_capabilities = self.explorer(browser_version)
        elif browser.lower() == 'chrome':
            desired_capabilities = self.chrome(browser_version)
        elif browser.lower() == 'opera':
            desired_capabilities = self.opera(browser_version)
        elif browser.lower() == 'safari':
            desired_capabilities = self.safari(browser_version)
        else:
            print("\nDriverFactory does not know the browser\t%s\n"%(browser))

        print(desired_capabilities)
        return desired_capabilities


    def select_remote_platform(self, remote_flag, os_name, os_version, browser,
                               browser_version, remote_project_name, remote_build_name):
        """Select the remote platform to run the test when the remote_flag is Y."""
        try:
            if remote_credentials.REMOTE_BROWSER_PLATFORM == 'BS':
                web_driver = self.run_browserstack(os_name, os_version, browser, browser_version,
                                                   remote_project_name, remote_build_name)
            else:
                web_driver = self.run_sauce_lab(os_name, os_version, browser, browser_version)

        except Exception as exception:
            self.print_exception(exception, remote_flag)

        return web_driver


    def run_browserstack(self, os_name, os_version, browser, browser_version,
                         remote_project_name, remote_build_name):
        """Run the test in browser stack when remote flag is 'Y'."""
        #Get the browser stack credentials from browser stack credentials file
        username = remote_credentials.USERNAME
        password = remote_credentials.ACCESS_KEY

        #Set browser
        desired_capabilities = self.get_browser(browser, browser_version)

        #Set os and os_version
        desired_capabilities = self.set_os(desired_capabilities, os_name, os_version)

        #Set remote project name
        if remote_project_name is not None:
            desired_capabilities = self.remote_project_name(desired_capabilities, remote_project_name)

        #Set remote build name
        if remote_build_name is not None:
            desired_capabilities = self.remote_build_name(desired_capabilities, remote_build_name)

        web_driver = webdriver.Remote(RemoteConnection("http://%s:%s@hub-cloud.browserstack.com/wd/hub"
                                                       %(username, password), resolve_ip=False), desired_capabilities=desired_capabilities)

        return web_driver


    def run_sauce_lab(self, os_name, os_version, browser, browser_version):
        """Run the test in sauce labs when remote flag is 'Y'."""
        #Get the sauce labs credentials from sauce.credentials file
        username = remote_credentials.USERNAME
        password = remote_credentials.ACCESS_KEY

        #set browser
        desired_capabilities = self.get_browser(browser, browser_version)

        #set saucelab platform
        desired_capabilities = self.saucelab_platform(desired_capabilities, os_name, os_version)

        web_driver = webdriver.Remote(command_executor="http://%s:%s@ondemand.saucelabs.com:80/wd/hub"
                                      %(username, password), desired_capabilities=desired_capabilities)

        return web_driver


    def run_local(self, browser):
        """Run the test on local system."""
        local_driver = None
        if browser.lower() == "ff" or browser.lower() == 'firefox':
            local_driver = self.firefox_local()
        elif  browser.lower() == "ie":
            local_driver = self.explorer_local()
        elif browser.lower() == "chrome":
            local_driver = self.chrome_local()
        elif browser.lower() == "opera":
            local_driver = self.opera_local()
        elif browser.lower() == "safari":
            local_driver = self.safari_local()
        elif browser.lower() == "headless-chrome":
            local_driver = self.headless_chrome()

        print(local_driver)
        return local_driver


    def run_mobile(self, mobile_os_name, mobile_os_version, device_name, app_package,
                   app_activity, remote_flag, device_flag, app_name, app_path,
                   ud_id, org_id, signing_id, no_reset_flag, appium_version):
        """Specify the mobile device configurations and get the mobile driver."""
        #Get the remote credentials from remote_credentials file
        username = remote_credentials.USERNAME
        password = remote_credentials.ACCESS_KEY

        #setup mobile device
        desired_capabilities = self.set_mobile_device(mobile_os_name, mobile_os_version, device_name)

        #Check wether the OS is android or iOS and get the mobile driver
        if mobile_os_name in 'Android':
            mobile_driver = self.android(remote_flag, desired_capabilities, app_path, app_name,
                                         appium_version, app_package, app_activity, username,
                                         password, device_flag)

        elif mobile_os_name == 'iOS':
            mobile_driver = self.ios(remote_flag, desired_capabilities, app_path, app_name,
                                     username, password, app_package, no_reset_flag, ud_id,
                                     org_id, signing_id, appium_version)

        return mobile_driver


    def android(self, remote_flag, desired_capabilities, app_path, app_name, appium_version,
                app_package, app_activity, username, password, device_flag):
        """Gets mobile driver for either local or remote setup of Android devices."""
        #Get the driver when test is run on a remote platform
        if remote_flag.lower() == 'y':
            mobile_driver = self.remote_platform_mobile(remote_flag, app_path, app_name, desired_capabilities,
                                                        username, password, appium_version)

        #Get the driver when test is run on local setup
        else:
            try:
                desired_capabilities['appPackage'] = app_package
                desired_capabilities['appActivity'] = app_activity
                if device_flag.lower() == 'y':
                    mobile_driver = mobile_webdriver.Remote(localhost_url, desired_capabilities)
                else:
                    desired_capabilities['app'] = os.path.join(app_path, app_name)
                    mobile_driver = mobile_webdriver.Remote(localhost_url, desired_capabilities)
            except Exception as exception:
                self.print_exception(exception, remote_flag)

        return mobile_driver


    def ios(self, remote_flag, desired_capabilities, app_path, app_name, username,
            password, app_package, no_reset_flag, ud_id, org_id, signing_id,
            appium_version):
        """Gets mobile driver for either local or remote setup of Android devices."""
        #Get the driver when test is run on a remote platform
        if remote_flag.lower() == 'y':
            mobile_driver = self.remote_platform_mobile(remote_flag, app_path, app_name,
                                                        desired_capabilities, username,
                                                        password, appium_version)

        #Get the driver when test is run on local setup
        else:
            try:
                desired_capabilities['app'] = os.path.join(app_path, app_name)
                desired_capabilities['bundleId'] = app_package
                desired_capabilities['noReset'] = no_reset_flag
                if ud_id is not None:
                    desired_capabilities['udid'] = ud_id
                    desired_capabilities['xcodeOrgId'] = org_id
                    desired_capabilities['xcodeSigningId'] = signing_id

                mobile_driver = mobile_webdriver.Remote(localhost_url, desired_capabilities)

            except Exception as exception:
                self.print_exception(exception, remote_flag)

        return mobile_driver


    def remote_platform_mobile(self, remote_flag, app_path, app_name, desired_capabilities,
                               username, password, appium_version):
        """
        Checks wether the test is to be run on either browserstack or saucelab and gets the
        remote mobile driver.
        """
        desired_capabilities['idleTimeout'] = 300
        desired_capabilities['name'] = 'Appium Python Test'
        try:
            #Gets driver when test is run on Saucelab
            if remote_credentials.REMOTE_BROWSER_PLATFORM == 'SL':
                mobile_driver = self.saucelab_mobile(app_path, app_name, desired_capabilities,
                                                     username, password)
            #Gets driver when test is run on Browserstack
            else:
                mobile_driver = self.browserstack_mobile(app_path, app_name, desired_capabilities,
                                                         username, password, appium_version)
        except Exception as exception:
            self.print_exception(exception, remote_flag)

        return mobile_driver


    def saucelab_mobile(self, app_path, app_name, desired_capabilities, username, password):
        """Setup mobile driver to run the test in Saucelab."""
        self.sauce_upload(app_path, app_name) #Saucelabs expects the app to be uploaded to Sauce storage everytime the test is run

        #Checking if the app_name is having spaces and replacing it with blank
        if ' ' in app_name:
            app_name = app_name.replace(' ', '')
            print("The app file name is having spaces, hence replaced the white spaces with blank in the file name:%s"%app_name)
        desired_capabilities['app'] = 'sauce-storage:'+app_name
        desired_capabilities['autoAcceptAlert'] = 'true'
        mobile_driver = mobile_webdriver.Remote(command_executor="http://%s:%s@ondemand.saucelabs.com:80/wd/hub"
                                                %(username, password), desired_capabilities=desired_capabilities)

        return mobile_driver


    def browserstack_mobile(self, app_path, app_name, desired_capabilities, username, password,
                            appium_version):
        """Setup mobile driver to run the test in Browserstack."""
        desired_capabilities['browserstack.appium_version'] = appium_version
        desired_capabilities['realMobile'] = 'true'
        desired_capabilities['app'] = self.browser_stack_upload(app_name, app_path) #upload the application to the Browserstack Storage
        mobile_driver = mobile_webdriver.Remote(command_executor="http://%s:%s@hub.browserstack.com:80/wd/hub"
                                                %(username, password), desired_capabilities=desired_capabilities)

        return mobile_driver

    @staticmethod
    def print_exception(exception, remote_flag):
        """Print out the exception message and suggest the solution based on the remote flag."""
        if remote_flag.lower() == 'y':
            solution = "It looks like you are trying to use a cloud service provider(BrowserStack or Sauce Labs) to run your test. \nPlease make sure you have updated ./conf/remote_credentials.py with the right credentials and try again. \nTo use your local browser please run the test with the -M N flag"
        else:
            solution = "It looks like you are trying to run test cases with Local Appium Setup. \nPlease make sure to run Appium Server and try again."

        print('\033[91m'+"\nException when trying to get remote webdriver:%s"%sys.modules[__name__]+'\033[0m')
        print('\033[91m'+"\nPython says:%s"%str(exception)+'\033[0m')
        print('\033[92m'+"\nSOLUTION: %s\n"%solution+'\033[0m')


    def get_firefox_driver(self):
        """Return the Firefox driver."""
        driver = webdriver.Firefox(firefox_profile=self.set_firefox_profile())

        return driver


    def set_firefox_profile(self):
        """Setup firefox with the right preferences and return a profile."""
        try:
            self.download_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'downloads'))
            if not os.path.exists(self.download_dir):
                os.makedirs(self.download_dir)
        except Exception as exception:
            print("Exception when trying to set directory structure")
            print(str(exception))

        profile = webdriver.firefox.firefox_profile.FirefoxProfile()
        set_pref = profile.set_preference
        set_pref('browser.download.folderList', 2)
        set_pref('browser.download.dir', self.download_dir)
        set_pref('browser.download.useDownloadDir', True)
        set_pref('browser.helperApps.alwaysAsk.force', False)
        set_pref('browser.helperApps.neverAsk.openFile',
                 'text/csv,application/octet-stream,application/pdf')
        set_pref('browser.helperApps.neverAsk.saveToDisk',
                 'text/csv,application/vnd.ms-excel,application/pdf,application/csv,application/octet-stream')
        set_pref('plugin.disable_full_page_plugin_for_types', 'application/pdf')
        set_pref('pdfjs.disabled', True)

        return profile
