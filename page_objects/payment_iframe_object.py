"""
This class models the iframe on the Weather shoper cart page
The form consists of some input fields and a button
"""
import conf.locators_conf as locators
from utils.Wrapit import Wrapit


class Payment_ifram_objects:
    "iframe objects"

    #Locators
    ifram = locators.ifram
    email_id = locators.email_id
    card_id = locators.card_id
    cc_exp = locators.cc_exp
    cvc_id = locators.cvc_id
    zip_id = locators.zip_id
    pay_button = locators.pay_button
    
    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def switch_frame_to(self):

        result_flag= self.switch_frame(name='stripe_checkout_app',index=None,wait_time=2)
        self.conditional_write(result_flag,
            positive='Successfully switched to the iframe',
            negative='Failed switching to iframe',
            level='debug')


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def email_info(self, email_add):
        result_flag = self.set_text(self.email_id,email_add)

        self.conditional_write(result_flag,
            positive='Set the email to: %s'%email_add,
            negative='Failed to set the email in the form',
            level='debug')

        return result_flag
    

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def cvc_info(self, cvc):
        result_flag = self.set_text(self.cvc_id,cvc)

        self.conditional_write(result_flag,
            positive='Set the cvc to: %s'%cvc,
            negative='Failed to set the email in the form',
            level='debug')

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_pay(self):
        result_flag = self.click_element(self.pay_button)

        self.conditional_write(result_flag,
            positive='Clicked on the Pay button',
            negative='Failed to click on the Pay button',
            level='debug')

        return result_flag
    

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def card_info(self,card_number):
        
        result_flag = self.add_list(self.card_id,card_number)
        self.conditional_write(result_flag,
            positive='Set the card number to: %s'%card_number,
            negative='Failed to set the card number in the form',
            level='debug')
        
        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def cc_exp_info(self,cc_exp_date):
        
        result_flag = self.add_list(self.cc_exp,cc_exp_date)
        self.conditional_write(result_flag,
            positive='Set the CC expiry date to: %s'%cc_exp_date,
            negative='Failed to set the CC expiry in the form',
            level='debug')
        
        return result_flag
    

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def zip_info(self,zip_code):
        
        result_flag = self.set_text(self.zip_id,zip_code)

        self.conditional_write(result_flag,
            positive='Set the zip code to: %s'%zip_code,
            negative='Failed to set the zip code in the form',
            level='debug')

        return result_flag