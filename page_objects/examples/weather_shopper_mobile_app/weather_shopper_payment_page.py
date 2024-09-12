"""
The payment page in Weathershopper application.
"""
# pylint: disable = W0212,E0401,E0402,W0104,R0913,R1710

import conf.locators_conf as locators
from utils.Wrapit import Wrapit
from .weather_shopper_payment_objects import WeatherShopperPaymentPageObjects



class WeatherShopperPaymentPage(WeatherShopperPaymentPageObjects):
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
