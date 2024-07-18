"""
Set the desired option for running the test on a remote platform.
"""

import os
import json
import requests
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.ie.options import Options as IeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.safari.options import Options as SafariOptions

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

    @staticmethod
    def saucelab_platform(options, os_name, os_version):
        """Set platform for saucelab."""
        options.platform_name = os_name + ' '+os_version
        return options

    @staticmethod
    def sauce_upload(app_path, app_name):
        """Upload the apk to the sauce temperory storage."""
        username =  os.getenv('REMOTE_USERNAME')
        password =  os.getenv('REMOTE_ACCESS_KEY')
        result_flag = False
        try:
            headers = {'Content-Type':'application/octet-stream'}
            params = os.path.join(app_path, app_name)
            fp = open(params, 'rb')
            data = fp.read()
            fp.close()
            #Checking if the app_name is having spaces and replacing it with blank
            if ' ' in app_name:
                app_name = app_name.replace(' ', '')
                print("The app file name is having spaces, hence replaced the white spaces with blank in the file name:%s"%app_name)

            response = requests.post('https://saucelabs.com/rest/v1/storage/%s/%s?overwrite=true'
                                     %(username, app_name), headers=headers, data=data, auth=(username, password)
                                    )
            if response.status_code == 200:
                result_flag = True
                print("App successfully uploaded to sauce storage")
        except Exception as exception:
            print(str(exception))

        return result_flag

    @staticmethod
    def browser_stack_upload(app_name, app_path):
        """Upload the apk to the BrowserStack storage if its not done earlier."""
        username =  os.getenv('REMOTE_USERNAME')
        access_key =  os.getenv('REMOTE_ACCESS_KEY')
        try:
            #Upload the apk
            apk_file = os.path.join(app_path, app_name)
            files = {'file': open(apk_file, 'rb')}
            post_response = requests.post("https://api-cloud.browserstack.com/app-automate/upload",
                                          files=files, auth=(username, access_key))
            post_json_data = json.loads(post_response.text)
            #Get the app url of the newly uploaded apk
            app_url = post_json_data['app_url']
        except Exception as exception:
            print(str(exception))

        return app_url
