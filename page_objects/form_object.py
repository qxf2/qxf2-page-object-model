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
    username_field = locators.username_field
    password_field = locators.password_field
    login_button = locators.login_button
    signup_button = locators.signup_button
    redirect_title = "redirect"    

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def set_user(self,username):
        "Set the name on the form"
        result_flag = self.set_text(self.username_field,username)
        self.conditional_write(result_flag,
            positive='Set the name to: %s'% username,
            negative='Failed to set the name in the form',
            level='debug')

        return result_flag 


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def set_password(self,password):
        "Set the email on the form"
        result_flag = self.set_text(self.password_field,password)
        self.conditional_write(result_flag,
            positive='Set the email to: %s'%password,
            negative='Failed to set the email in the form',
            level='debug')

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def login(self):
        "Click on 'Click Me' button"
        result_flag = self.click_element(self.login_button)
        self.conditional_write(result_flag,
            positive='Clicked on the "Login" button',
            negative='Failed to click on "Login" button',
            level='debug')

        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def accept_terms(self):
        "Accept the terms and conditions"
        result_flag = self.select_checkbox(self.tac_checkbox)
        self.conditional_write(result_flag,
            positive='Accepted the terms and conditions',
            negative='Failed to accept the terms and conditions',
            level='debug')
            
        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def check_redirect(self):
        "Check if we have been redirected to the redirect page"
        result_flag = False
        if self.redirect_title in self.driver.title:
            result_flag = True
            self.switch_page("redirect")
        
        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def submit_form(self,username,password):
        "Submit the form"
        result_flag = self.set_user(username)
        result_flag &= self.set_password(password)
        result_flag &= self.accept_terms()
        result_flag &= self.login()
        result_flag &= self.check_redirect()

        return result_flag


