"""
Page objects for the product page in Weathershopper application.
"""
# pylint: disable = W0212,E0401
from utils.Wrapit import Wrapit
from core_helpers.mobile_app_helper import Mobile_App_Helper
from .product_page_objects import ProductPageObjects
from .navigation_menu_objects import NavigationMenuObjects

class WeatherShopperProductPage(Mobile_App_Helper, ProductPageObjects, NavigationMenuObjects):
    "Page objects for product page in Weathershopper application."

    @Wrapit._exceptionHandler
    def get_least_and_most_expensive_items(self, all_items):
        "Get least and most expensive item from the page"

        # Calculate least and most expensive item
        least_expensive_item = self.get_least_expensive_item(all_items)
        most_expensive_item = self.get_most_expensive_item(all_items)

        return least_expensive_item, most_expensive_item

    @Wrapit._exceptionHandler
    def add_items_to_cart(self, items):
        "Add items to cart"
        result_flag = True
        for item in items:
            result_flag &= self.add_to_cart(item)

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_least_expensive_item(self, all_items):
        "This method is to get the least expensive item from the given list of items"
        least_expensive_item = min(all_items, key=lambda x: x['price'])
        self.write(f"Least expensive item is {least_expensive_item}")
        return least_expensive_item

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_most_expensive_item(self, all_items):
        "This method is to get the most expensive item from the given list of items"
        most_expensive_item = max(all_items, key=lambda x: x['price'])
        self.write(f"Most expensive item is {most_expensive_item}")
        return most_expensive_item
