"""
This class models the pages of the application as object
"""

from .Base_Page import Base_Page
# import configuration files here.
import conf.<locators_conf_template> as locators
from utils.Wrapit import Wrapit


class Form_Object:
    "Page object for the <name of page>"
    
    #locators
    <field_name> = loctors.<field_name>

    @Wrapit._screenshot
    @Wrapit._exceptionHandler
    #call the appropriate method from Base_page for interaction with the web elements
    def <method_name>(<arguments>):
        result_flag = self.<method_name>(arguments)
        self.conditional_write(result_flag,
            positive='',
            negative='',
            level='debug')

        return result_flag 

    #Sameple method
    """
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
    """


