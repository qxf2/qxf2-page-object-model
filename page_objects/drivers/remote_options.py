"""
Set the desired option for running the test on a remote platform.
"""
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from conf import remote_credentials
import os
import requests
import json
from datetime import datetime

class RemoteOptions():
    """Class contains methods for various remote options for browserstack and saucelab."""

    @staticmethod
    def firefox(browser_version):
        """Set web browser as firefox."""
        desired_capabilities = DesiredCapabilities.FIREFOX
        desired_capabilities['browser_version'] = browser_version

        return desired_capabilities

    @staticmethod
    def explorer(browser_version):
        """Set web browser as Explorer."""
        desired_capabilities = DesiredCapabilities.INTERNETEXPLORER
        desired_capabilities['browser_version'] = browser_version

        return desired_capabilities

    @staticmethod
    def chrome(browser_version):
        """Set web browser as Chrome."""
        desired_capabilities = DesiredCapabilities.CHROME
        desired_capabilities['browser_version'] = browser_version

        return desired_capabilities

    @staticmethod
    def opera(browser_version):
        """Set web_browser as Opera."""
        desired_capabilities = DesiredCapabilities.OPERA
        desired_capabilities['browser_version'] = browser_version

        return desired_capabilities

    @staticmethod
    def safari(browser_version):
        """Set web browser as Safari."""
        desired_capabilities = DesiredCapabilities.SAFARI
        desired_capabilities['browser_version'] = browser_version

        return desired_capabilities

    @staticmethod
    def set_os(desired_capabilities, os_name, os_version):
        """Set os name and os_version."""
        desired_capabilities['os'] = os_name
        desired_capabilities['os_version'] = os_version

        return desired_capabilities

    @staticmethod
    def remote_project_name(desired_capabilities, remote_project_name):
        """Set remote project name for browserstack."""
        desired_capabilities['project'] = remote_project_name

        return desired_capabilities

    @staticmethod
    def remote_build_name(desired_capabilities, remote_build_name):
        """Set remote build name for browserstack."""
        desired_capabilities['build'] = remote_build_name+"_"+str(datetime.now().strftime("%c"))

        return desired_capabilities

    @staticmethod
    def saucelab_platform(desired_capabilities, os_name, os_version):
        """Set platform for saucelab."""
        desired_capabilities['platform'] = os_name + ' '+os_version

        return desired_capabilities

    @staticmethod
    def set_mobile_device(mobile_os_name, mobile_os_version, device_name):
        """Setup the mobile device."""
        desired_capabilities = {}
        desired_capabilities['platformName'] = mobile_os_name
        desired_capabilities['platformVersion'] = mobile_os_version
        desired_capabilities['deviceName'] = device_name

        return desired_capabilities

    @staticmethod
    def sauce_upload(app_path, app_name):
        """Upload the apk to the sauce temperory storage."""
        username = remote_credentials.USERNAME
        password = remote_credentials.ACCESS_KEY
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
        username = remote_credentials.USERNAME
        access_key = remote_credentials.ACCESS_KEY
        try:
            #Upload the apk
            apk_file = os.path.join(app_path, app_name)
            files = {'file': open(apk_file, 'rb')}
            post_response = requests.post("https://api.browserstack.com/app-automate/upload",
                                          files=files, auth=(username, access_key))
            post_json_data = json.loads(post_response.text)
            #Get the app url of the newly uploaded apk
            app_url = post_json_data['app_url']
        except Exception as exception:
            print(str(exception))

        return app_url
