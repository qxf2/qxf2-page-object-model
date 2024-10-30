"""
This class models the redirect page of the Selenium tutorial
URL: selenium-tutorial-redirect
The page consists of a header, footer and some text
"""
from core_helpers.web_app_helper import Web_App_Helper
from .header_object import Header_Object
from .footer_object import Footer_Object
import conf.locators_conf as locators
from utils.Wrapit import Wrapit


class Tutorial_Redirect_Page(Web_App_Helper,Header_Object,Footer_Object):
    "Page Object for the tutorial's redirect page"

    #locators
    heading = locators.heading

    def start(self):
        "Use this method to go to specific URL -- if needed"
        url = 'selenium-tutorial-redirect'
        self.open(url)

    @Wrapit._exceptionHandler
    def check_heading(self):
        "Check if the heading exists"
        result_flag = self.check_element_present(self.heading)
        self.conditional_write(result_flag,
            positive='Correct heading present on redirect page',
            negative='Heading on redirect page is INCORRECT!!',
            level='debug')

        return result_flag
