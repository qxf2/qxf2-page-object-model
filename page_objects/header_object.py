"""
This class models the Qxf2.com header as a Page Object.
The header consists of the Qxf2 logo, Qxf2 tag-line and the hamburger menu
Since the hanburger menu is complex, we will model it as a separate object
"""
from .Base_Page import Base_Page
from .hamburger_menu_object import Hamburger_Menu_Object
import conf.locators_conf as locators
from utils.Wrapit import Wrapit


class Header_Object(Hamburger_Menu_Object):
    "Page Object for the header class"

    #locators
    qxf2_logo = locators.qxf2_logo
    qxf2_tagline_part1 = locators.qxf2_tagline_part1
    qxf2_tagline_part2 = locators.qxf2_tagline_part2

    @Wrapit._exceptionHandler
    def check_logo_present(self):
        "Check if a logo is present"
        return self.check_element_present(self.qxf2_logo)

    @Wrapit._exceptionHandler
    def check_tagline_present(self):
        "Check if the tagline is present"
        return self.check_element_present(self.qxf2_tagline_part1) and self.check_element_present(self.qxf2_tagline_part2)


