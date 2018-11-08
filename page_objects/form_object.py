"""
This class models the form on the Selenium tutorial page
The form consists of some input fields, a dropdown, a checkbox and a button
"""

from .Base_Page import Base_Page
import conf.locators_conf as locators
from utils.Wrapit import Wrapit


class Form_Object:
    "Page object for the Form"
    
    #locators
    name_field = locators.name_field
    email_field = locators.email_field
    phone_no_field = locators.phone_no_field
    click_me_button = locators.click_me_button
    gender_dropdown = locators.gender_dropdown
    gender_option = locators.gender_option
    tac_checkbox = locators.tac_checkbox
    redirect_title = "redirect"    

    @Wrapit._screenshot
    @Wrapit._exceptionHandler
    def set_name(self,name):
        "Set the name on the form"
        result_flag = self.set_text(self.name_field,name)
        self.conditional_write(result_flag,
            positive='Set the name to: %s'%name,
            negative='Failed to set the name in the form',
            level='debug')

        return result_flag 


    @Wrapit._screenshot
    @Wrapit._exceptionHandler
    def set_email(self,email):
        "Set the email on the form"
        result_flag = self.set_text(self.email_field,email)
        self.conditional_write(result_flag,
            positive='Set the email to: %s'%email,
            negative='Failed to set the email in the form',
            level='debug')

        return result_flag


    @Wrapit._screenshot
    @Wrapit._exceptionHandler
    def set_phone(self,phone):
        "Set the phone on the form"
        result_flag = self.set_text(self.phone_no_field,phone)
        self.conditional_write(result_flag,
            positive='Set the phone to: %s'%phone,
            negative='Failed to set the phone in the form',
            level='debug')

        return result_flag


    @Wrapit._screenshot
    @Wrapit._exceptionHandler
    def set_gender(self,gender,wait_seconds=1):
        "Set the gender on the form"
        result_flag = self.click_element(self.gender_dropdown)
        self.wait(wait_seconds)
        result_flag &= self.click_element(self.gender_option%gender)
        self.conditional_write(result_flag,
            positive='Set the gender to: %s'%gender,
            negative='Failed to set the gender in the form',
            level='debug')

        return result_flag


    @Wrapit._screenshot
    @Wrapit._exceptionHandler
    def click_me(self):
        "Click on 'Click Me' button"
        result_flag = self.click_element(self.click_me_button)
        self.conditional_write(result_flag,
            positive='Clicked on the "click me" button',
            negative='Failed to click on "click me" button',
            level='debug')

        return result_flag


    @Wrapit._screenshot
    @Wrapit._exceptionHandler
    def accept_terms(self):
        "Accept the terms and conditions"
        result_flag = self.select_checkbox(self.tac_checkbox)
        self.conditional_write(result_flag,
            positive='Accepted the terms and conditions',
            negative='Failed to accept the terms and conditions',
            level='debug')
            
        return result_flag


    @Wrapit._screenshot
    @Wrapit._exceptionHandler
    def check_redirect(self):
        "Check if we have been redirected to the redirect page"
        result_flag = False
        if self.redirect_title in self.driver.title:
            result_flag = True
            self.switch_page("redirect")
        
        return result_flag


    @Wrapit._screenshot
    @Wrapit._exceptionHandler
    def submit_form(self,username,email,phone,gender):
        "Submit the form"
        result_flag = self.set_name(username)
        result_flag &= self.set_email(email)
        result_flag &= self.set_phone(phone)
        result_flag &= self.set_gender(gender)
        result_flag &= self.accept_terms()
        result_flag &= self.click_me()
        result_flag &= self.check_redirect()

        return result_flag


