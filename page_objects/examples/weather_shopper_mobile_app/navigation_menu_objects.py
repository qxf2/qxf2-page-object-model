"""
This class models the navigation menu in Weathershopper application.
"""
import conf.locators_conf as locators
from utils.Wrapit import Wrapit

class NavigationMenuObjects:
    "Page objects for the navigation menu in Weathershopper application."

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

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def view_cart(self):
        "This method is to click on Cart button in the Weather Shopper application."
        cart = locators.cart
        result_flag = self.click_element(cart)
        self.switch_page("weathershopper cart page")
        return result_flag
