import os
from selenium import webdriver
from integrations.remote_options import RemoteOptions
from conf import remote_url_conf

class LambdaTestRunner(RemoteOptions):
    def __init__(self):
        self.username = os.getenv('REMOTE_USERNAME')
        self.password = os.getenv('REMOTE_ACCESS_KEY')
        self.lambdatest_url = remote_url_conf.lambdatest_url.format(self.username, self.password)
        self.session_id = None
        self.session_url = None

    def lambdatest_credentials(self, lambdatest_options):
        """Set LambdaTest credentials."""
        lambdatest_options['user'] = self.username
        lambdatest_options['accessKey'] = self.password
        return lambdatest_options

    def run_lambdatest(self, os_name, os_version, browser, browser_version,
                       remote_project_name, remote_build_name, testname):
        """Run the test in LambdaTest when remote flag is 'Y'."""
        options = self.get_browser(browser, browser_version)

        if options is None:
            raise ValueError(f"Unsupported browser: {browser}")

        # Set LambdaTest platform
        options.platformName = f"{os_name} {os_version}"
        
        lambdatest_options = {}
        lambdatest_options = self.lambdatest_credentials(lambdatest_options)
        lambdatest_options["video"] = True
        lambdatest_options["visual"] = False  # Make it true to capture screenshots
        lambdatest_options["network"] = True
        lambdatest_options["build"] = remote_build_name
        lambdatest_options["project"] = remote_project_name
        lambdatest_options["name"] = testname
        lambdatest_options["w3c"] = True
        lambdatest_options["plugin"] = "python-pytest"
        
        options.set_capability('LT:options', lambdatest_options)
        web_driver = webdriver.Remote(command_executor=self.lambdatest_url, options=options)

        # Store the session ID and session URL
        self.session_id = web_driver.session_id

        # Get the session URL
        self.session_url = self.get_session_url_with_retries(self.session_id)

        print(f"Session ID: {self.session_id}")
        print(f"Session url: {self.session_url}")

        return web_driver
    
    def get_session_url_with_retries(self, session_id, retries=5, delay=2):
        """Fetch the session URL using the LambdaTest API with retries."""
        import requests,time
        api_url = f"https://api.lambdatest.com/automation/api/v1/sessions/{session_id}"
        for _ in range(retries):
            response = requests.get(api_url, auth=(self.username, self.password))
            if response.status_code == 200:
                session_data = response.json()
                test_id = session_data['data']['test_id']
                return f"https://automation.lambdatest.com/test?testID={test_id}"
            elif response.status_code == 404:
                print(f"Retrying... Status code: {response.status_code}, Response: {response.text}")
                time.sleep(delay)
            else:
                raise Exception(f"Failed to fetch session details. Status code: {response.status_code}, Response: {response.text}")
        raise Exception(f"Failed to fetch session details after {retries} retries.")    
