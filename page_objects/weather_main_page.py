"""
This class models the main Weather shopper page.
URL: selenium-tutorial-main
The page consists of a header, footer, weather main objects, sunscreen page objects, moisturizer page object, 
Cart objects and Payment page objects objec

"""

from .Base_Page import Base_Page
from .weather_main_page_object import Weather_main_page_object
from .sunscreen_page_object import Sunscreen_page_object
from .moisturizer_page_object import Moisturizer_page_object
from .cart_page_object import Cart_object
from .payment_iframe_object import Payment_ifram_objects
from .header_object import Header_Object
from .footer_object import Footer_Object

class Weather_Main_Page(Base_Page,Header_Object,Footer_Object,Weather_main_page_object,Sunscreen_page_object,Moisturizer_page_object,
                            Cart_object,Payment_ifram_objects):
    "Page Object for the tutorial's main page"


    def start(self):
        "Use this method to go to specific URL -- if needed"
        url = '/'
        self.open(url)