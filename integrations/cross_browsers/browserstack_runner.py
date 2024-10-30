"""
Get the webdriver and mobiledriver for BrowserStack.
"""
import os
from selenium import webdriver
from integrations.cross_browsers.remote_options import RemoteOptions
from conf import screenshot_conf
from conf import remote_url_conf

class BrowserStackRunner(RemoteOptions):
    """Configure and get the webdriver and the mobiledriver for BrowserStack"""
    def __init__(self):
        self.username = os.getenv('REMOTE_USERNAME')
        self.password = os.getenv('REMOTE_ACCESS_KEY')
        self.browserstack_url = remote_url_conf.browserstack_url
        self.browserstack_app_upload_url = remote_url_conf.browserstack_app_upload_url

    def browserstack_credentials(self, browserstack_options):
        """Set browserstack credentials."""
        browserstack_options['userName'] = self.username
        browserstack_options['accessKey'] = self.password

        return browserstack_options

    def browserstack_capabilities(self, desired_capabilities, app_name, app_path, appium_version):
        """Configure browserstack capabilities"""
        bstack_mobile_options = {}
        bstack_mobile_options['idleTimeout'] = 300
        bstack_mobile_options['sessionName'] = 'Appium Python Test'
        bstack_mobile_options['appiumVersion'] = appium_version
        bstack_mobile_options['realMobile'] = 'true'
        bstack_mobile_options = self.browserstack_credentials(bstack_mobile_options)
        #upload the application to the Browserstack Storage
        desired_capabilities['app'] = self.browserstack_upload(app_name, app_path)
        desired_capabilities['bstack:options'] = bstack_mobile_options

        return desired_capabilities

    def browserstack_snapshots(self, desired_capabilities):
        """Set browserstack snapshots"""
        desired_capabilities['debug'] = str(screenshot_conf.BS_ENABLE_SCREENSHOTS).lower()

        return desired_capabilities

    def browserstack_upload(self, app_name, app_path, timeout = 30):
        """Upload the apk to the BrowserStack storage if its not done earlier."""
        try:
            #Upload the apk
            import requests
            import json
            apk_file = os.path.join(app_path, app_name)
            files = {'file': open(apk_file, 'rb')}
            post_response = requests.post(self.browserstack_app_upload_url, files=files,
                                         auth=(self.username, self.password),timeout= timeout)
            post_response.raise_for_status()
            post_json_data = json.loads(post_response.text)
            #Get the app url of the newly uploaded apk
            app_url = post_json_data['app_url']
            return app_url

        except Exception as exception:
            print('\033[91m'+"\nError while uploading the app:%s"%str(exception)+'\033[0m')

    def get_current_session_url(self, web_driver):
        "Get current session url"
        import json
        current_session = web_driver.execute_script('browserstack_executor: {"action": "getSessionDetails"}')
        session_details = json.loads(current_session)
        # Check if 'public_url' exists and is not None
        if 'public_url' in session_details and session_details['public_url'] is not None:
            session_url = session_details['public_url']
        else:
            session_url = session_details['browser_url']

        return session_url

    def set_os(self, desired_capabilities, os_name, os_version):
        """Set os name and os_version."""      
        desired_capabilities['os'] = os_name
        desired_capabilities['osVersion'] = os_version

        return desired_capabilities

    def get_browserstack_mobile_driver(self, app_path, app_name, desired_capabilities,
                            appium_version):
        """Setup mobile driver to run the test in Browserstack."""
        desired_capabilities = self.browserstack_capabilities(desired_capabilities, app_name,
                                                              app_path, appium_version)
        mobile_driver = self.set_capabilities_options(desired_capabilities,
                                                      url=self.browserstack_url)
        session_url = self.get_current_session_url(mobile_driver)

        return mobile_driver,session_url

    def get_browserstack_webdriver(self, os_name, os_version, browser, browser_version,
                         remote_project_name, remote_build_name):
        """Run the test in browserstack when remote flag is 'Y'."""
        #Set browser
        options = self.get_browser(browser, browser_version)
        desired_capabilities = {}
        #Set os and os_version
        desired_capabilities = self.set_os(desired_capabilities, os_name, os_version)
        #Set remote project name
        if remote_project_name is not None:
            desired_capabilities = self.remote_project_name(desired_capabilities,
                                                            remote_project_name)
        #Set remote build name
        if remote_build_name is not None:
            desired_capabilities = self.remote_build_name(desired_capabilities, remote_build_name)

        desired_capabilities = self.browserstack_snapshots(desired_capabilities)
        desired_capabilities = self.browserstack_credentials(desired_capabilities)
        options.set_capability('bstack:options', desired_capabilities)
        web_driver = webdriver.Remote(command_executor=self.browserstack_url, options=options)
        session_url = self.get_current_session_url(web_driver)

        return web_driver, session_url
