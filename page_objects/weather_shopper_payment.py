"""
Page Objects for Weathershopper payment page
"""
import conf.locators_conf as locators
from utils.Wrapit import Wrapit
from .Mobile_Base_Page import Mobile_Base_Page

class WeatherShopperPayment(Mobile_Base_Page):
    """
    Page Object for Weathershopper payment page
    """
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
