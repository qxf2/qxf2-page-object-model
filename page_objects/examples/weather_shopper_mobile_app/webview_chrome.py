"""
Page object to test Webview Chrome for Weathershopper application.
"""
# pylint: disable = W0212,E0401
from utils import Wrapit
from core_helpers import Mobile_App_Helper
from urllib.parse import unquote

class WebviewChrome(Mobile_App_Helper):
    "Page object for ChromeView interaction"

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def switch_to_chrome_context(self):
        "Switch to Chrome webview context to access the browser methods"
        result_flag = self.switch_context("WEBVIEW_chrome")
        self.conditional_write(result_flag,
                               positive="Switched to WEBVIEW_chrome context",
                               negative="Unable to switch to WEBVIEW_chrome context")

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_current_url(self):
        "This method gets the current URL"
        if len(self.driver.window_handles) > 1:
            self.write("Multiple window handles detected", 'debug')
            for handle in self.driver.window_handles:
                self.driver.switch_to.window(handle)
                if self.driver.current_url == "chrome-native://newtab/":
                    self.write("Current URL is a new tab, switching to next handle", 'debug')
                    continue
                else:
                    break
        url = unquote(self.driver.current_url)
        return url

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_page_title(self):
        "Get the page title"
        return self.driver.title
