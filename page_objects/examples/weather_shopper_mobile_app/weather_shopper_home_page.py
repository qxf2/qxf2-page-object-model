"""
Page objects for the home page in Weathershopper application.
"""
# pylint: disable = W0212,E0401
import re
import conf.locators_conf as locators
from utils.Wrapit import Wrapit
from core_helpers.mobile_app_helper import Mobile_App_Helper

class WeatherShopperHomePage(Mobile_App_Helper):
    "Page objects for home page in Weathershopper application."

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_temperature(self):
        "This method is to get the temperature in the Weather Shopper application."
        temperature = locators.temperature
        current_temperature = self.get_text(temperature)
        self.write(f"Current temperature is {int(current_temperature)}", level='debug')
        return int(current_temperature)

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def view_moisturizers(self):
        "This method is to click on Moisturizer tab in the Weather Shopper application."

        moisturizers = locators.moisturizers
        result_flag = self.click_element(moisturizers)
        self.conditional_write(result_flag,
            positive='Successfully clicked on Moisturizer tab',
            negative='Failed to click on Moisturizer tab',
            level='debug')
        self.switch_page("weathershopper products page")
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def view_sunscreens(self):
        "This method is to click on Sunscreen tab in the Weather Shopper application."

        sunscreens = locators.sunscreens
        result_flag = self.click_element(sunscreens)
        self.conditional_write(result_flag,
            positive='Successfully clicked on Sunscreen tab',
            negative='Failed to click on Sunscreen tab',
            level='debug')
        self.switch_page("weathershopper products page")
        return result_flag
