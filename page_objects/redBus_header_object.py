"""
This class models the redBus.in header as a Page Object.
The header consists of the redBus logo and the redBus main menu
"""
from .Base_Page import Base_Page
import conf.locators_conf as locators
from utils.Wrapit import Wrapit


class redBus_Header_Object():
    "Page Object for the header class"

    #locators
    redBus_header_logo = locators.header_logo
    redBus_header_menu = locators.header_menu
    
    @Wrapit._exceptionHandler
    def check_logo_present(self):
        "Check if a logo is present"
        return self.check_element_present(self.redBus_header_logo)

    @Wrapit._exceptionHandler
    def check_header_menu_present(self):
        "Check if the header products navigation menu is present"
        return self.check_element_present(self.redBus_header_menu)
    
    