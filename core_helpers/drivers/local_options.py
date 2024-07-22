"""
Get the webrivers for local browsers.
"""
from selenium.webdriver.chrome.options import Options
import sys
from selenium import webdriver

class LocalOptions():
    """Class contains methods for getting webfrivers for various browsers."""

    @staticmethod
    def firefox_local():
        """Get webdriver for firefox."""
        local_driver = webdriver.Firefox()

        return local_driver

    @staticmethod
    def explorer_local():
        """Get webdriver for internet explorer."""
        local_driver = webdriver.Ie()

        return local_driver

    @staticmethod
    def chrome_local():
        """Get webdriver for chrome."""
        local_driver = webdriver.Chrome()

        return local_driver

    @staticmethod
    def opera_local():
        """Get webdriver for opera."""
        from conf import opera_browser_conf
        try:
            opera_browser_location = opera_browser_conf.location
            options = webdriver.ChromeOptions()
            options.binary_location = opera_browser_location # path to opera executable
            local_driver = webdriver.Opera(options=options)

        except Exception as exception:
            print("\nException when trying to get remote webdriver:%s"%sys.modules[__name__])
            print("Python says:%s"%str(exception))
            if  'no Opera binary' in str(exception):
                print("SOLUTION: It looks like you are trying to use Opera Browser. Please update Opera Browser location under conf/opera_browser_conf.\n")

        return local_driver

    @staticmethod
    def safari_local():
        """Get webdriver for safari."""
        local_driver = webdriver.Safari()

        return local_driver

    @staticmethod
    def headless_chrome():
        """Set up headless chrome driver options and get webdriver for headless chrome."""
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-certificate-errors')
        local_driver = webdriver.Chrome(options=options)

        return local_driver

    def app_details(self, desired_capabilities, app_package, app_activity):
        desired_capabilities['appPackage'] = app_package
        desired_capabilities['appActivity'] = app_activity
        return desired_capabilities

    def app_name(self, desired_capabilities, app_path, app_name):
        import os
        desired_capabilities['app'] = os.path.join(app_path, app_name)
        return desired_capabilities

    def ios_capabilities(self, desired_capabilities, app_package, no_reset_flag, ud_id, org_id, signing_id):
        desired_capabilities['bundleId'] = app_package
        desired_capabilities['noReset'] = no_reset_flag
        if ud_id is not None:
            desired_capabilities['udid'] = ud_id
            desired_capabilities['xcodeOrgId'] = org_id
            desired_capabilities['xcodeSigningId'] = signing_id
        return desired_capabilities

    def set_mobile_device(self, mobile_os_name, mobile_os_version, device_name):
        """Setup the mobile device."""
        desired_capabilities = {}
        desired_capabilities['platformName'] = mobile_os_name
        desired_capabilities['platformVersion'] = mobile_os_version
        desired_capabilities['deviceName'] = device_name

        return desired_capabilities
