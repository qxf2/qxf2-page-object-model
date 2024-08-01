"""
Page object for the payment page in Weathershopper application.
"""
# pylint: disable = W0212,E0401
import re
import conf.locators_conf as locators
from utils.Wrapit import Wrapit
from core_helpers.mobile_app_helper import Mobile_App_Helper

class WeatherShopperPaymentPage(Mobile_App_Helper):
    "Page objects for payment page in Weathershopper application."

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def enter_valid_payment_details(self, payment_details):
        "This method is to enter valid payment details"

        result_flag = self.click_element(locators.payment_method_dropdown)
        result_flag &= self.click_element(locators.payment_card_type.format(payment_details["card_type"]))
        result_flag &= self.set_text(locators.payment_email, payment_details["email"])
        result_flag &= self.set_text(locators.payment_card_number, payment_details["card_number"])
        result_flag &= self.set_text(locators.payment_card_expiry, payment_details["card_expiry"])
        result_flag &= self.set_text(locators.payment_card_cvv, payment_details["card_cvv"])
        result_flag &= self.click_element(locators.pay_button)
        if self.get_element(locators.payment_success, verbose_flag=False) is None:
            result_flag &= False

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def select_payment_method(self, card_type):
        "Select the payment method"
        result_flag = self.click_element(locators.payment_method_dropdown)
        result_flag &= self.click_element(locators.payment_card_type.format(card_type))
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def enter_email(self, email):
        "Enter the email address"
        result_flag = self.set_text(locators.payment_email, email)
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def enter_card_number(self, card_number):
        "Enter the card number"
        result_flag = self.set_text(locators.payment_card_number, card_number)
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def enter_card_expiry(self, card_expiry):
        "Enter the card expiry date"
        result_flag = self.set_text(locators.payment_card_expiry, card_expiry)
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def enter_card_cvv(self, card_cvv):
        "Enter the card CVV"
        result_flag = self.set_text(locators.payment_card_cvv, card_cvv)
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def submit_payment(self):
        "Click the pay button"
        result_flag = self.click_element(locators.pay_button)
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def verify_payment_success(self):
        "Verify if the payment was successful"
        result_flag = self.get_element(locators.payment_success, verbose_flag=False) is not None
        return result_flag