"""
This class models the main Selenium tutorial page.
URL: selenium-tutorial-main
The page consists of a header, footer, form and table objects
"""
from core_helpers.web_app_helper import Web_App_Helper
from .form_object import Form_Object
from .header_object import Header_Object
from .table_object import Table_Object
from .footer_object import Footer_Object


class Tutorial_Main_Page(Web_App_Helper,Form_Object,Header_Object,Table_Object,Footer_Object):
    "Page Object for the tutorial's main page"

    def start(self):
        "Use this method to go to specific URL -- if needed"
        url = 'selenium-tutorial-main'
        self.open(url)
