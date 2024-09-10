"""
Page objects for the product page in Weathershopper application.
"""
# pylint: disable = W0212,E0401
import conf.locators_conf as locators
from utils.Wrapit import Wrapit
from core_helpers.mobile_app_helper import Mobile_App_Helper
from .weather_shopper_product_objects import ProductPageObjects
from .navigation_menu_objects import NavigationMenuObjects

class WeatherShopperProductPage(Mobile_App_Helper, ProductPageObjects, NavigationMenuObjects):
    "Page objects for product page in Weathershopper application."

    def get_least_and_most_expensive_items(self, all_items):
        "Get least and most expensive item from the page"

        # Calculate least and most expensive item
        least_expensive_item = self.get_least_expensive_item(all_items)
        most_expensive_item = self.get_most_expensive_item(all_items)

        return least_expensive_item, most_expensive_item

    def add_items_to_cart(self, items):
        "Add items to cart"
        result_flag = True
        for item in items: 
            result_flag &= self.add_to_cart(item)

        return result_flag
