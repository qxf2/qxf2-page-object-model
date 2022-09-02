"""
This class models the weathershopper_mainpage page.
The page consists of a temperature text
"""
from .Base_Page import Base_Page
from .weathershopper_page_object import Weathershopper_Object_Page

class Weathershopper_Mainpage(Base_Page,Weathershopper_Object_Page):
    "Page Object for the weather shopper main page"

    def start(self):
        "Use this method to go to specific URL -- if needed"
        url = '/'
        self.open(url)
