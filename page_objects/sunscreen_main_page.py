"""
This class models the weathershopper_mainpage page.
The page consists of a temperature text
"""
from .Base_Page import Base_Page
from .sunscreen_object_page import Sunscreen_Object_Page



class Sunscreen_Mainpage(Base_Page,Sunscreen_Object_Page):
    "Page Object for the weather shopper main page"

    def start(self):
        "Use this method to go to specific URL -- if needed"
        url = 'sunscreen'
        self.open(url)
