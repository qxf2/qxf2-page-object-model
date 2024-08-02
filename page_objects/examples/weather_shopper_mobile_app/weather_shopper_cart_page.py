"""
Page objects for cart page in Weathershopper application.
"""
# pylint: disable = W0212,E0401
import re
import conf.locators_conf as locators
from utils.Wrapit import Wrapit
from core_helpers.mobile_app_helper import Mobile_App_Helper

class WeatherShopperCartPage(Mobile_App_Helper):
    "Page object for the cart page in Weathershopper application."

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_cart_total(self):
        "This method is to get the total price in the cart."
        cart_total = self.get_text(locators.total_amount)
        # Extracting the numeric part using regular expression
        match = re.search(r'\d+\.\d+', cart_total.decode())
        total_amount = float(match.group()) if match else None

        if total_amount is None:
            self.write("Total amount is None", level='debug')
        else:
            self.write(f"Total amount is {total_amount}", level='debug')
        return total_amount

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def verify_total(self, cart_total, cart_items):
        "This method is to verify the total price in the cart."
        if cart_total == sum(cart_items):
            return True
        return False

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def change_quantity(self, item_to_change, quantity=2):
        "This method is to change the quantity of an item in the cart"
        result_flag = self.set_text(locators.edit_quantity.format(item_to_change), quantity)
        self.conditional_write(result_flag,
            positive=f"Successfully changed quantity of {item_to_change} to {quantity}",
            negative=f"Failed to change quantity of {item_to_change} to {quantity}",
            level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def refresh_total_amount(self):
        "This method is to refresh the total amount in the cart."
        result_flag = self.click_element(locators.refresh_button)
        self.conditional_write(result_flag,
            positive="Successfully clicked on refresh button",
            negative="Failed to click on refresh button",
            level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def delete_from_cart(self, item_to_delete):
        "This method is to delete an item from the cart"
        result_flag = self.click_element(locators.checkbox.format(item_to_delete))
        result_flag &= self.click_element(locators.delete_from_cart_button)
        self.conditional_write(result_flag,
            positive=f"Successfully deleted {item_to_delete} from cart",
            negative=f"Failed to delete item from cart",
            level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def checkout(self):
        "This method is to go to the Checkout page"
        result_flag = self.click_element(locators.checkout_button)
        self.conditional_write(result_flag,
            positive="Successfully clicked on checkout button",
            negative="Failed to click on checkout button",
            level='debug')
        self.switch_page("weathershopper payment page")
        return result_flag
