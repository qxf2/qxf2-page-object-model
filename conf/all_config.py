from dataclasses import dataclass, field, asdict, astuple
from core_helpers.prettytable_object import ConfigSummaryTable
from pytest import FixtureRequest
from typing import List
import platform

@dataclass
class TestName:
    "Test function name"
    name: str

@dataclass
class BaseURL:
    "Base URL config"
    url: str

@dataclass
class Browser:
    "Browser config"
    name: List|str = field(default_factory=lambda:["headless-chrome", "chrome"])
    version: List|str = field(default_factory=lambda:["latest"])

@dataclass
class Browsers:
    "Browsers config"
    browsers: List[Browser]

@dataclass
class Platform:
    "Platform config"
    name: List|str = field(default_factory=lambda:[platform.uname()[0]])
    version: List|str = field(default_factory=lambda:[platform.uname()[2]])

@dataclass
class Platforms:
    "Platforms config"
    platforms: List[Platform]

@dataclass
class BrowserStack:
    "BrowserStack config"
    project_name: str|None = None
    build_name: str|None = None

@dataclass
class SauceLabs:
    "SauceLabs config"
    pass

@dataclass
class RemoteTestExecution:
    "Remote test exec config"
    flag: str
    browserstack: BrowserStack
    saucelabs: SauceLabs = field(default_factory=dict)

@dataclass
class TestRail:
    "TestRail config"
    flag: str = "N"
    test_run_id: str|None = None

@dataclass
class Tesults:
    "Tesulsts config"
    flag: str = "N"

@dataclass
class Reporting:
    "Remote Integrations config"
    testrail: TestRail
    tesults: Tesults
    
@dataclass
class UITestConfig:
    "Consolidated UI test config"
    test: TestName
    base_url: BaseURL
    browser: Browser
    platform: Platform
    remote_test_execution: RemoteTestExecution
    reporting: Reporting
    
    def __post_init__(self):
        config_table = ConfigSummaryTable(self.test.name)    
        config_table.print_table(asdict(self))

@dataclass
class APIURL:
    "API app URL"
    url: str
 
@dataclass
class APITestConfig:
    "Consolidated API test config"
    test: TestName
    api_url: APIURL

    def __post_init__(self):
        config_table = ConfigSummaryTable(self.test.name)    
        config_table.print_table(asdict(self))

@dataclass
class IOs:
    "ios config"
    signing_id: str
    ud_id: str = None
    org_id: str = None

@dataclass
class MobileOs:
    "Mobile OS config"
    name: str
    version: str

@dataclass
class Emulator:
    "Emulator config"
    name: str

@dataclass
class MobileApp:
    "Mobile app config"
    name: str
    path: str
    package: str
    activity: str
    no_reset_flag: bool
    orientation: str = None

@dataclass
class AppiumConfig:
    "Appium config"
    version: str

@dataclass
class MobileDevice:
    "Mobile device config"
    flag: str
    name: str

@dataclass
class MobileTestConfig:
    "Consolidated Mobile test config"
    test: TestName
    mobile_os: MobileOs
    mobile_device: MobileDevice
    mobile_app: MobileApp
    appium_config: AppiumConfig 
    ios_config: IOs
    remote_test_execution: RemoteTestExecution
    reporting: Reporting
 
    def __post_init__(self):
        config_table = ConfigSummaryTable(self.test.name)    
        config_table.print_table(asdict(self))

class ConfigFactory:
    "Config Factory object to build UI/API/Mobile config"

    def __init__(self, request: FixtureRequest):
        "Initialize"
        self.request = request
        self.testname = self.request.node.name.split('[')[0]
        self.config = self.request.config

    def _get(self, value: str) -> str:
        "Get config values"
        if isinstance(value, tuple):
            return tuple([self._get(v) for v in value if self._get(v)])
        return self.config.getoption(value)
    
    def build_ui_config(self) -> UITestConfig:
        "Build UI config"
        test = TestName(self.testname)
        base_url = BaseURL(self._get("url"))
        browser = Browser(*self._get(("browser", "browser_version")))
        sys_platform = Platform(*self._get(("os_name", "os_version")))
        browserstack = BrowserStack(*self._get(("remote_project_name", "remote_build_name")))
        remote_test_exec = RemoteTestExecution(self._get("remote_flag"),
                                               browserstack)
        testrail = TestRail(*self._get(("testrail_flag", "test_run_id")))
        reporting = Reporting(testrail,
                              Tesults(self._get("tesults_flag")))
        
        return UITestConfig(test,
                            base_url,
                            browser,
                            sys_platform,
                            remote_test_exec,
                            reporting)
        
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
        browserstack = BrowserStack(*self._get(("remote_project_name",
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

    @staticmethod
    def config_as_tuple(config:UITestConfig|MobileTestConfig|APITestConfig):
        "Return config as a tuple"
        return astuple(config)
        