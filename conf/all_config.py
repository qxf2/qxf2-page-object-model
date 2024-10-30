from dataclasses import dataclass

@dataclass
class BaseURL:
    url: str

@dataclass
class Browser:
    name: str = "chrome"
    version: str = "122"
    
@dataclass
class Platform:
    name: str
    version: str
    
@dataclass
class UITestConfig:
    base_url: BaseURL
    browser: Browser
    Platform: Platform
    