"""
This class models the redirect page of the Selenium tutorial
URL: selenium-tutorial-redirect
The page consists of a header, footer and some text
"""
from .Base_Page import Base_Page
from .header_object import Header_Object
from .footer_object import Footer_Object
import conf.locators_conf as locators
from utils.Wrapit import Wrapit


class Redirect_checkout_page(Base_Page,Header_Object,Footer_Object):
    "Page Object for the tutorial's redirect page"

    #locators
    checkout_confirmation = locators.checkout_confirmation

    def start(self):
        "Use this method to go to specific URL -- if needed"
        url = 'confirmation'
        self.open(url)

    @Wrapit._exceptionHandler
    def check_heading(self):
        "Check if the heading exists"
        result_flag = self.check_element_present(self.checkout_confirmation)
        self.conditional_write(result_flag,
            positive='Correct heading present on redirect page',
            negative='Heading on redirect page is INCORRECT!!',
            level='debug')

        return result_flag
