"""
This class models the pages of the application as objects
"""
# import configuration files here.
import conf.locators_conf as locators
from .Base_Page import Base_Page
from utils.Wrapit import Wrapit

#Update the class name and name of the file according to your page
class <name_of_page_object>:
    "Page object for the <name of page>"
    
    #specify locators
    <field_name> = locators.<field_name>

    @Wrapit._screenshot
    @Wrapit._exceptionHandler
    #Define methods
    #Use methods from Base_page for handling the web elements
    def <method_name>(<arguments>):
        result_flag = self.<method_name>(<locator_arguments>)
        return result_flag 
