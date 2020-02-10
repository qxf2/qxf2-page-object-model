"""
This class models the redirect page i.e the search results page of the redBus Main Page 
The page consists of a header, footer and view buses object
"""
from .Base_Page import Base_Page
from .redBus_header_object import redBus_Header_Object
from .redBus_footer_object import redBus_Footer_Object
from .redBus_view_buses_object import redBus_View_Buses_Object
import conf.locators_conf as locators
import re
from utils.Wrapit import Wrapit


class redBus_Search_Results_Page(Base_Page,redBus_Header_Object,redBus_Footer_Object,redBus_View_Buses_Object):
    "Page Object for the redirect page of redBus main page i.e search results page"

    #locators
    source_locator = locators.source_location_in_search_results_page
    destination_locator = locators.destination_location_in_search_results_page

    def start(self):
        "Use this method to go to specific URL -- if needed"
        url = 'search?fromCityName=Bangalore%20(All%20Locations)&fromCityId=122&toCityName=Coimbatore%20(All%20Locations)&toCityId=141&busType=Any&opId=0&onward=24-Apr-2020&return=30-Apr-2020'
        self.open(url)

    

    @Wrapit._exceptionHandler
    @Wrapit._screenshot        
    def check_source_and_destination(self):
        "Check if the source and destination elements are present on the search results page"
        
        result_flag = self.check_element_present(self.source_locator)
        result_flag &= self.check_element_present(self.destination_locator)
                   
        self.conditional_write(result_flag,
            positive='Source and destination elements found on the redirect page!',
            negative='Source and destination elements NOT found on the redirect page!!',
            level='debug')
        
        return result_flag


  
    