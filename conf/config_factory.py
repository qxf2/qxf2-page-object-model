"""
A config Factory module to build UI, API & Mobile test configs
"""
import os
from typing import List
from pytest import FixtureRequest
from .config_store import (Browser,
                           Platform,
                           Chrome,
                           TestName,
                           BaseURL,
                           BrowserStackConfig,
                           RemoteTestExecution,
                           TestRail,
                           Reporting,
                           Tesults,
                           UiTestConfig,
                           LocalBrowsers,
                           LocalPlatforms,
                           BrowserStackBrowsers,
                           BrowserStackPlatforms,
                           APITestConfig,
                           MobileOs,
                           MobileDevice,
                           MobileApp,
                           MobileTestConfig,
                           AppiumConfig,
                           IOs,
                           APIURL)

class ConfigFactory:
    "Config Factory object to build UI/API/Mobile config"

    def __init__(self, testname: str, config: FixtureRequest.config):
        "Initialize"
        self.testname = testname
        self.config = config

    def _get(self, value: str) -> str:
        "Get config values"
        if isinstance(value, tuple):
            return tuple([self._get(v) for v in value if self._get(v)])
        return self.config.getoption(value)

    def build_ui_config(self,
                        browser_data: None|Browser = None,
                        platform_data: None|Platform = None) -> UiTestConfig:
        "Build UI config"
        test = TestName(self.testname)
        base_url = BaseURL(self._get("url"))
        if not browser_data:
            if not self._get("browser"):
                browser = Chrome()
            else:
                browser = Browser(*self._get("browser"),self._get("browser_version"))
        else:
            browser = browser_data
        if not platform_data:
            sys_platform = Platform(*self._get("os_name"),*self._get("os_version"))
        else:
            sys_platform = platform_data
        browserstack = BrowserStackConfig(*self._get(("remote_project_name", "remote_build_name")))
        remote_test_exec = RemoteTestExecution(self._get("remote_flag"),
                                               browserstack)
        testrail = TestRail(*self._get(("testrail_flag", "test_run_id")))
        reporting = Reporting(testrail,
                              Tesults(self._get("tesults_flag")))
        return UiTestConfig(test,
                            base_url,
                            browser,
                            sys_platform,
                            remote_test_exec,
                            reporting)

    def build_iterative_ui_config(self) -> List[UiTestConfig]:
        "Build a list of UI test config"
        configs = []
        if self._get("browser")[0].lower() == "all":
            if self._get("remote_flag").lower() == "n":
                local_browsers = LocalBrowsers()
                local_platforms = LocalPlatforms()
                browsers = local_browsers.entries
                sys_platforms = local_platforms.entries
            if self._get("remote_flag").lower() == "y":
                remote_platform = os.getenv("REMOTE_BROWSER_PLATFORM")
                if remote_platform.lower() == "bs":
                    browserstack_browsers = BrowserStackBrowsers()
                    browserstack_platforms = BrowserStackPlatforms()
                    browsers = browserstack_browsers.entries
                    sys_platforms = browserstack_platforms.entries
        else:
            browsers = []
            for browser in self._get("browser"):
               browsers.append(Browser(name=browser,
                                       version="latest"))
            sys_platforms = []
            if self._get("os_name") and self._get("os_version"):
                for name, version in zip(self._get("os_name"), self._get("os_version")):
                    sys_platforms.append(Platform(name=name,
                                                  version=version))
            else:
                local_platforms = LocalPlatforms()
                sys_platforms = local_platforms.entries
                
        for browser in browsers:
            for sys_platform in sys_platforms:
                configs.append(self.build_ui_config(browser, sys_platform))
        return configs

    def build_api_config(self) -> APITestConfig:
        "Build API test config"
        return APITestConfig(TestName(self.testname),
                             APIURL(self._get("url")))

    def build_mobile_config(self) -> MobileTestConfig:
        "Build Mobile test config"
        test = TestName(self.testname)
        mobileos = MobileOs(*self._get(("mobile_os_name",
                                       "mobile_os_version")))
        mobile_device = MobileDevice(*self._get(("device_flag",
                                                 "device_name")))
        mobile_app = MobileApp(*self._get(("app_name",
                                           "app_path",
                                           "app_package",
                                           "app_activity",
                                           "no_reset_flag",
                                           "orientation")))
        appium_config = AppiumConfig(self._get("appium_version"))
        ios_config = IOs(*self._get(("signing_id", "ud_id", "org_id")))
        browserstack = BrowserStackConfig(*self._get(("remote_project_name",
                                                "remote_build_name")))
        remote_test_exec = RemoteTestExecution(self._get("remote_flag"),
                                               browserstack)
        testrail = TestRail(*self._get(("testrail_flag",
                                        "test_run_id")))
        reporting = Reporting(testrail,
                              Tesults(self._get("tesults_flag")))
        return MobileTestConfig(test,
                                mobileos,
                                mobile_device,
                                mobile_app,
                                appium_config,
                                ios_config,
                                remote_test_exec,
                                reporting)