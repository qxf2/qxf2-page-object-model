"""
This class models the form on the Selenium tutorial page
The form consists of some input fields, a dropdown, a checkbox and a button
"""
import conf.locators_conf as locators
from utils.Wrapit import Wrapit


class Cart_object:
    "Cart page objects"

    #Locator
    card_pay = locators.card_pay


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_pay_with_card(self):
        "Click on 'Pay with card' button"
        result_flag = self.click_element(self.card_pay)
        self.conditional_write(result_flag,
            positive='Clicked on the "Pay with card" button',
            negative='Failed to click on "Pay with card" button',
            level='debug')
        
        return result_flag