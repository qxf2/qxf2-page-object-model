"""
This class models the cart page in Weathershopper application.
"""
# pylint: disable = W0212,E0401
import conf.locators_conf as locators
from utils.Wrapit import Wrapit
from core_helpers.mobile_app_helper import Mobile_App_Helper
from .cart_objects import CartObjects

class WeatherShopperCartPage(Mobile_App_Helper, CartObjects):
    "Page objects for the cart page in Weathershopper application."

    def verify_cart_total(self, items):
        "Verify cart total"
        cart_total = self.get_cart_total()
        item_prices = [item['price'] for item in items]
        result_flag = self.verify_total(cart_total, item_prices)

        return result_flag

    def change_quantity_and_verify(self, least_expensive_item,
                                    most_expensive_item, quantity):
        "Change quantity of item and verify cart total"
        # Change quantity of least expensive item
        result_flag = self.change_quantity(least_expensive_item['name'], quantity=quantity)
        self.conditional_write(result_flag,
                                positive="Successfully changed quantity of item",
                                negative="Failed to change quantity of item")

        # Refresh cart total
        result_flag = self.refresh_total_amount()
        self.conditional_write(result_flag,
                                positive="Successfully refreshed total",
                                negative="Failed to refresh total")

        # Verify cart total after change in quantity
        cart_total_after_change = self.get_cart_total()
        item_prices = [least_expensive_item['price'] * quantity, most_expensive_item['price']]
        result_flag = self.verify_total(cart_total_after_change, item_prices)

        return result_flag

    def delete_item_and_verify(self, least_expensive_item, most_expensive_item, quantity):
        "Delete item from cart and verify cart total"
        # Delete item from cart
        result_flag = self.delete_from_cart(most_expensive_item['name'])
        self.conditional_write(result_flag,
                                positive="Successfully deleted item from cart",
                                negative="Failed to delete item from cart")

        # Verify cart total after deletion
        cart_total_after_deletion = self.get_cart_total()
        item_prices = [least_expensive_item['price'] * quantity]
        result_flag = self.verify_total(cart_total_after_deletion, item_prices)

        return result_flag
