
"""
Get the webdriver for LambdaTest browsers.
"""
import os
import time
import requests
from selenium import webdriver
from .remote_options import RemoteOptions
from conf import remote_url_conf


class LambdaTestRunner(RemoteOptions):
    """Configure and get the webdriver for the LambdaTest"""

    def __init__(self):
        self.username = os.getenv('REMOTE_USERNAME')
        self.password = os.getenv('REMOTE_ACCESS_KEY')
        self.lambdatest_url = remote_url_conf.lambdatest_url.format(self.username, self.password)
        self.lambdatest_api_server_url = remote_url_conf.lambdatest_api_server_url
        self.session_id = None
        self.session_url = None

    def lambdatest_credentials(self, lambdatest_options):
        """Set LambdaTest credentials."""
        lambdatest_options['user'] = self.username
        lambdatest_options['accessKey'] = self.password
        return lambdatest_options

    def set_lambdatest_capabilities(self, remote_project_name, remote_build_name, testname):
        """Set LambdaTest Capabilities"""
        lambdatest_options = {}
        lambdatest_options = self.lambdatest_credentials(lambdatest_options)
        lambdatest_options["build"] = remote_build_name
        lambdatest_options["project"] = remote_project_name
        lambdatest_options["name"] = testname
        lambdatest_options["video"] = True
        lambdatest_options["visual"] = True
        lambdatest_options["network"] = True
        lambdatest_options["w3c"] = True
        lambdatest_options["console"] = True
        lambdatest_options["plugin"] = "python-pytest"
        return lambdatest_options

    def get_lambdatest_webdriver(self, os_name, os_version, browser, browser_version,
                                 remote_project_name, remote_build_name, testname):
        """Run the test in LambdaTest when remote flag is 'Y'."""
        options = self.get_browser(browser, browser_version)

        if options is None:
            raise ValueError(f"Unsupported browser: {browser}")

        #  Set LambdaTest platform
        lambdatest_options = self.set_lambdatest_capabilities(
            remote_project_name, remote_build_name, testname
        )
        lambdatest_options["platformName"] = f"{os_name} {os_version}"
        options.set_capability('LT:options', lambdatest_options)
        web_driver = webdriver.Remote(command_executor=self.lambdatest_url, options=options)

        # Get the session ID and session URL and print it
        self.session_id = web_driver.session_id
        self.session_url = self.get_session_url_with_retries(self.session_id)

        return web_driver, self.session_url

    def get_session_url_with_retries(self, session_id, retries=5, delay=2, timeout=30):
        """Fetch the session URL using the LambdaTest API with retries."""
        api_url = f"{self.lambdatest_api_server_url}/sessions/{session_id}"
        time.sleep(2)
        for _ in range(retries):
            response = requests.get(api_url, auth=(self.username, self.password), timeout=timeout)
            if response.status_code == 200:
                session_data = response.json()
                test_id = session_data['data']['test_id']
                session_url = f"https://automation.lambdatest.com/test?testID={test_id}"
                return session_url
            else:
                print(f"Retrying... Status code: {response.status_code}, Response: {response.text}")
                time.sleep(delay)
        raise Exception(f"Failed to fetch session details after {retries} retries.")
