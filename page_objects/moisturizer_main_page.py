"""
This class models the weathershopper_mainpage page.
The page consists of a temperature text
"""
from .Base_Page import Base_Page
from .moisturizer_page_object import Moisturizer_Object_Page



class Moisturizer_Mainpage(Base_Page,Moisturizer_Object_Page):
    "Page Object for the weather shopper main page"

    def start(self):
        "Use this method to go to specific URL -- if needed"
        url = 'moisturizer'
        self.open(url)
