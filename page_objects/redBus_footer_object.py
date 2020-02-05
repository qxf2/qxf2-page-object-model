"""
This class models the footer object on redBus.in
We model it as two parts:
1. The menu
2. The copyright
"""
from datetime import datetime
from .Base_Page import Base_Page
import conf.locators_conf as locators
from utils.Wrapit import Wrapit

class redBus_Footer_Object:
    "Page object for the footer class"

    #locators
    redBus_footer_menu = locators.footer_menu_headings
    redBus_foorter_logo = locators.foorter_logo
    redBus_copyright_text = locators.footer_copyright_text
          


    
