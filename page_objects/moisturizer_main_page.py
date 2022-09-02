"""
This class models the moisturizer_mainpage page.
"""
from .Base_Page import Base_Page
from .moisturizer_page_object import Moisturizer_Object_Page

class Moisturizer_Mainpage(Base_Page,Moisturizer_Object_Page):
    "Page Object for the moisturizer main page"

    def start(self):
        "Use this method to go to specific URL -- if needed"
        url = 'moisturizer'
        self.open(url)
