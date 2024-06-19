import os
from selenium import webdriver
from integrations.remote_options import RemoteOptions
from conf import remote_url_conf

class LambdaTestRunner(RemoteOptions):
    def __init__(self):
        self.username = os.getenv('REMOTE_USERNAME')
        self.password = os.getenv('REMOTE_ACCESS_KEY')
        self.lambdatest_url = remote_url_conf.lambdatest_url.format(self.username, self.password)

    def lambdatest_credentials(self, lambdatest_options):
        """Set LambdaTest credentials."""
        lambdatest_options['user'] = self.username
        lambdatest_options['accessKey'] = self.password
        return lambdatest_options

    def run_lambdatest(self, os_name, os_version, browser, browser_version,
                       remote_project_name, remote_build_name):
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
        lambdatest_options["name"] = "UI Selenium Tests"
        lambdatest_options["w3c"] = True
        lambdatest_options["plugin"] = "python-pytest"
        
        options.set_capability('LT:options', lambdatest_options)
        web_driver = webdriver.Remote(command_executor=self.lambdatest_url, options=options)

        return web_driver
