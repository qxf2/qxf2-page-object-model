"""
Page object to test Webview Chrome for Weathershopper application.
"""
# pylint: disable = W0212,E0401
from utils.Wrapit import Wrapit
from .Mobile_Base_Page import Mobile_Base_Page
from urllib.parse import unquote

class WebviewChrome(Mobile_Base_Page):
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
        url = unquote(self.driver.current_url)
        return url

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_page_title(self):
        "Get the page title"
        return self.driver.title
