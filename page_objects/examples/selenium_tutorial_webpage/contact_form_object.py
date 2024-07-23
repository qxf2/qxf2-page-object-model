"""
This class models the form on contact page
The form consists of some input fields.
"""
import conf.locators_conf as locators
from utils.Wrapit import Wrapit

class Contact_Form_Object:
    "Page object for the contact Form"

    #locators
    contact_name_field = locators.contact_name_field

    @Wrapit._exceptionHandler
    def set_name(self,name):
        "Set the name on the Kick start form"
        result_flag = self.set_text(self.contact_name_field,name)
        self.conditional_write(result_flag,
            positive='Set the name to: %s'%name,
            negative='Failed to set the name in the form',
            level='debug')

        return result_flag
