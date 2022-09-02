"""
This class models the Selenium main page.
URL: weathershopper-pythonanywhere
The page consists of a buttons, texts, links 
"""
from .Base_Page import Base_Page
from .weather_shopper_home_object import Weather_Shopper_Home_Object

class Weather_Shopper_Main_Page(Base_Page,Weather_Shopper_Home_Object):
    def start(self):
        url='/'
        self.open(url)


