from dataclasses import dataclass, field, asdict
from core_helpers.prettytable_object import ConfigSummaryTable

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
    name: list
    version: list
 
@dataclass
class Platform:
    "Platform config"
    name: list
    version: list

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