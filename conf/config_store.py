"""
A config store module to store the test setup configurations
"""
import os
import platform
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core_helpers.prettytable_object import ConfigSummaryTable

cwd = Path.cwd()
env_file = os.path.join(cwd, '.env.remote')
load_dotenv(env_file)

# pylint: disable=line-too-long
@dataclass
class TestName:
    "Test function name"
    name: str

@dataclass
class BaseURL:
    "Base URL config"
    url: str = "https://qxf2.com/"

@dataclass
class Browser:
    "Browser config"
    name: str
    version: str

@dataclass
class Chrome(Browser):
    "Chrome config"
    name: str = "chrome"
    version: str = "latest"

@dataclass
class Firefox(Browser):
    "Firefox config"
    name: str = "firefox"
    version: str = "latest"

@dataclass
class Safari(Browser):
    "Safari config"
    name: str = "safari"
    version: str = "18"

@dataclass
class Platform:
    "Platform config"
    name: str = platform.uname()[0]
    version: str = platform.uname()[2]

@dataclass
class LocalBrowsers():
    "Local Browsers config"
    entries: List[Browser] = field(default_factory=lambda:[Chrome(),
                                                           Firefox()])

@dataclass
class LocalPlatforms():
    "Local Platform config"
    entries: List[Platform] = field(default_factory=lambda:[Platform()])

@dataclass
class BrowserStackBrowsers():
    "BrowserStack Browser config"
    entries: List[Browser] = field(default_factory=lambda:[Chrome(version="latest"),
                                                           Firefox(version="latest")])

@dataclass
class BrowserStackPlatforms():
    "BrowserStack Platform config"
    entries: List[Platform] = field(default_factory=lambda:[Platform(name="windows",
                                                                     version='10'),
                                                            Platform(name="OS X",version="Sequoia")])

@dataclass
class BrowserStackConfig:
    "BrowserStack config"
    project_name: Optional[str] = None
    build_name: Optional[str] = None

@dataclass
class RemoteTestExecution:
    "Remote test exec config"
    flag: str
    browserstack: BrowserStackConfig

@dataclass
class TestRail:
    "TestRail config"
    flag: str = "N"
    test_run_id: Optional[str] = None

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
class UiTestConfig:
    "Consolidated UI test config"
    test: TestName
    base_url: BaseURL
    browser: Browser
    platform: Platform
    remote_test_execution: RemoteTestExecution
    reporting: Reporting

    def __str__(self):
        config_table = ConfigSummaryTable(self.test.name)
        return config_table.return_table_string(asdict(self))

@dataclass
class APIURL:
    "API app URL"
    url: str = "https://cars-app.qxf2.com"

@dataclass
class APITestConfig:
    "Consolidated API test config"
    test: TestName
    api_url: APIURL

    def __str__(self):
        config_table = ConfigSummaryTable(self.test.name)
        return config_table.return_table_string(asdict(self))

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

# pylint: disable=too-many-instance-attributes
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

    def __str__(self):
        config_table = ConfigSummaryTable(self.test.name)
        return config_table.return_table_string(asdict(self))
