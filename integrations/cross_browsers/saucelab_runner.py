"""
Get the webdriver and mobiledriver for SauceLab.
"""
import os
from selenium import webdriver
from .remote_options import RemoteOptions

class SauceLabRunner(RemoteOptions):
    """Configure and get the webdriver and the mobiledriver for SauceLab"""
    def __init__(self):
        self.username = os.getenv('REMOTE_USERNAME')
        self.password = os.getenv('REMOTE_ACCESS_KEY')
        self.saucelabs_url = "https://ondemand.eu-central-1.saucelabs.com:443/wd/hub"
        self.saucelabs_app_upload_url = "https://api.eu-central-1.saucelabs.com/v1/storage/upload"

    def saucelab_credentials(self, sauce_options):
        """Set saucelab credentials."""
        sauce_options['username'] = self.username
        sauce_options['accessKey'] = self.password

        return sauce_options

    def saucelab_capabilities(self, desired_capabilities, app_name):
        """Set saucelab capabilities"""
        desired_capabilities['appium:app'] = 'storage:filename='+app_name
        desired_capabilities['autoAcceptAlerts'] = 'true'
        sauce_mobile_options = {}
        sauce_mobile_options = self.saucelab_credentials(sauce_mobile_options)
        desired_capabilities['sauce:options'] = sauce_mobile_options

        return desired_capabilities

    def saucelab_platform(self, options, os_name, os_version):
        """Set platform for saucelab."""
        options.platform_name = os_name + ' '+os_version

        return options

    def sauce_upload(self,app_path, app_name, timeout=30):
        """Upload the apk to the sauce temperory storage."""
        import requests
        from requests.auth import HTTPBasicAuth

        result_flag = False
        try:
            apk_file_path = os.path.join(app_path, app_name)

            # Open the APK file in binary mode
            with open(apk_file_path, 'rb') as apk_file:
                files = {'payload': (app_name, apk_file, 'application/vnd.android.package-archive')}
                params = {'name': app_name,  'overwrite': 'true'}
                # Perform the upload request
                response = requests.post(self.saucelabs_app_upload_url,
                    auth=HTTPBasicAuth(self.username, self.password),
                    files=files, params=params, timeout=timeout)
                # Check the response
                if response.status_code == 201:
                    result_flag = True
                    print('App successfully uploaded to sauce storage')
                    #print('Response:', response.json())
                else:
                    print('App upload failed!')
                    print('Status code:', response.status_code)
                    print('Response:', response.text)
                    raise Exception("Failed to upload APK file." +
                                    f"Status code: {response.status_code}")

        except Exception as exception:
            print(str(exception))

        return result_flag

    def get_saucelab_mobile_driver(self, app_path, app_name, desired_capabilities):
        """Setup mobile driver to run the test in Saucelab."""
        #Saucelabs expects the app to be uploaded to Sauce storage everytime the test is run
        result_flag = self.sauce_upload(app_path, app_name)

        if result_flag:
            desired_capabilities = self.saucelab_capabilities(desired_capabilities, app_name)
            mobile_driver = self.set_capabilities_options(desired_capabilities,
                                                          url=self.saucelabs_url)
        else:
            print("Failed to upload an app file")
            raise Exception("Failed to upload APK file.")

        return mobile_driver

    def get_saucelab_webdriver(self, os_name, os_version, browser, browser_version):
        """Setup webdriver to run the test in Saucelab."""
        #set browser
        options = self.get_browser(browser, browser_version)

        #set saucelab platform
        options = self.saucelab_platform(options, os_name, os_version)
        sauce_options = {}
        sauce_options = self.saucelab_credentials(sauce_options)
        options.set_capability('sauce:options', sauce_options)
        web_driver = webdriver.Remote(command_executor=self.saucelabs_url, options=options)

        return web_driver
