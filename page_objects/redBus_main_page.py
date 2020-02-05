"""
This class models the redBus main page.
URL: redBus.in
The page consists of a header, footer, search menu object
"""
from .Base_Page import Base_Page
from .redBus_header_object import redBus_Header_Object
from .redBus_footer_object import redBus_Footer_Object
from .redBus_search_buses_object import redBus_Search_Buses_Object

from utils.Wrapit import Wrapit


class redBus_Main_Page(Base_Page,redBus_Header_Object,redBus_Footer_Object,redBus_Search_Buses_Object):
    "Page Object for the redBus's main page"
    
    def start(self):
        "Use this method to go to specific URL -- if needed"
        url = 'bus-tickets'
        self.open(url)
