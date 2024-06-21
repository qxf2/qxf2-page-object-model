"""
Set the desired option for running the test on a remote platform.
"""
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.ie.options import Options as IeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from appium.options.android import UiAutomator2Options
from appium import webdriver as mobile_webdriver

class RemoteOptions():
    """Class contains methods for various remote options for browserstack and saucelab."""

    @staticmethod
    def firefox(browser_version):
        """Set web browser as firefox."""
        options = FirefoxOptions()
        options.browser_version = browser_version
        
        return options

    @staticmethod
    def explorer(browser_version):
        """Set web browser as Explorer."""
        options = IeOptions()
        options.browser_version = browser_version

        return options

    @staticmethod
    def chrome(browser_version):
        """Set web browser as Chrome."""
        options = ChromeOptions()
        options.browser_version = browser_version

        return options

    @staticmethod
    def safari(browser_version):
        """Set web browser as Safari."""
        options = SafariOptions()
        options.browser_version = browser_version

        return options
    
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
            print("\nDriverFactory does not know the browser\t%s\n" % browser)
            desired_capabilities = None

        return desired_capabilities
    
    def remote_project_name(self, desired_capabilities, remote_project_name):
        """Set remote project name for browserstack."""
        desired_capabilities['projectName'] = remote_project_name

        return desired_capabilities

    def remote_build_name(self, desired_capabilities, remote_build_name):
        """Set remote build name for browserstack."""
        from datetime import datetime
        desired_capabilities['buildName'] = remote_build_name+"_"+str(datetime.now().strftime("%c"))

        return desired_capabilities
    
    def set_capabilities_options(self, desired_capabilities, url):
        """Set the capabilities options for the mobile driver."""
        capabilities_options = UiAutomator2Options().load_capabilities(desired_capabilities)
        mobile_driver = mobile_webdriver.Remote(command_executor=url,options=capabilities_options)

        return mobile_driver
    
    