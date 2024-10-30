"""
Page object for the payment page in Weathershopper application.
"""
# pylint: disable = W0212,E0401,W0104,R0913,R1710,W0718,E0402


import conf.locators_conf as locators
from utils.Wrapit import Wrapit
from core_helpers.mobile_app_helper import Mobile_App_Helper

class WeatherShopperPaymentPageObjects(Mobile_App_Helper):
    "Page objects for payment page in Weathershopper application."

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def enter_card_cvv(self, card_cvv):
        "Enter the card CVV"
        result_flag = self.set_text(locators.payment_card_cvv, card_cvv)
        self.conditional_write(result_flag,
            positive=f'Successfully set the card CVV: {card_cvv}',
            negative=f'Failed to set the card CVV: {card_cvv}',
            level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def enter_card_expiry(self, card_expiry):
        "Enter the card expiry date"
        result_flag = self.set_text(locators.payment_card_expiry, card_expiry)
        self.conditional_write(result_flag,
            positive=f'Successfully set the card expiry date: {card_expiry}',
            negative=f'Failed to set the card expiry date: {card_expiry}',
            level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def enter_email(self, email):
        "Enter the email address"
        result_flag = self.set_text(locators.payment_email, email)
        self.conditional_write(result_flag,
            positive=f'Successfully set the email address: {email}',
            negative=f'Failed to set the email address: {email}',
            level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def enter_card_number(self, card_number):
        "Enter the card number"
        result_flag = self.set_text(locators.payment_card_number, card_number)
        self.conditional_write(result_flag,
            positive=f'Successfully set the card number: {card_number}',
            negative=f'Failed to set the card number: {card_number}',
            level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def select_payment_method(self, card_type):
        "Select the payment method"
        result_flag = self.click_element(locators.payment_method_dropdown)
        result_flag &= self.click_element(locators.payment_card_type.format(card_type))
        self.conditional_write(result_flag,
            positive=f'Successfully selected the payment method: {card_type}',
            negative=f'Failed to select the payment method: {card_type}',
            level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def submit_payment(self):
        "Click the pay button"
        result_flag = self.click_element(locators.pay_button)
        self.conditional_write(result_flag,
            positive='Successfully clicked on the pay button',
            negative='Failed to click on the pay button',
            level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def verify_payment_success(self):
        "Verify if the payment was successful"
        result_flag = self.get_element(locators.payment_success, verbose_flag=False) is not None
        self.conditional_write(result_flag,
            positive='Payment was successful',
            negative='Payment failed',
            level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def submit_payment_details(self,card_type,email,card_number,card_expiry,card_cvv):
        "Submit the form"
        result_flag = self.select_payment_method(card_type)
        result_flag &= self.enter_email(email)
        result_flag &= self.enter_card_number(card_number)
        result_flag &= self.enter_card_expiry(card_expiry)
        result_flag &= self.enter_card_cvv(card_cvv)
        result_flag &= self.submit_payment()
        return result_flag
