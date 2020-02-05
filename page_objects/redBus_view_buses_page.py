"""
This class models the redirect page i.e the view buses page of the redBus Main Page 
URL: selenium-tutorial-redirect
The page consists of a header, footer and some text
"""
from .Base_Page import Base_Page
from .redBus_header_object import redBus_Header_Object
from .redBus_footer_object import redBus_Footer_Object
import conf.locators_conf as locators
#import conf.ticket_booking_conf as 
from utils.Wrapit import Wrapit


class redBus_View_Buses_Page(Base_Page,redBus_Header_Object,redBus_Footer_Object):
    "Page Object for the redirect page of redBus main page i.e view buses page"

    #locators
    #govt_buses_option = locators.govt_buses_option
    source_locator = locators.source_location_in_view_buses_page
    destination_locator = locators.destination_location_in_view_buses_page

    def start(self):
        "Use this method to go to specific URL -- if needed"
        url = 'https://www.redbus.in/search?fromCityName=Bangalore%20(All%20Locations)&toCityName=Coimbatore%20(All%20Locations)&fromCityId=122&toCityId=141&busType=Any&opId=0&onward=06-Feb-2020'
        self.open(url)

    @Wrapit._exceptionHandler    
    def check_source_and_destination(self,source,destination):
        "Check if the source and destination matches with the from and to selections in redBus Main Page"
        
        result_flag = self.check_element_present(self.source_locator)
        result_flag &= self.check_element_present(self.destination_locator)
        if (result_flag is True) :
            if((self.get_text(self.source_locator).casefold() == source.casefold()) and (self.get_text(self.destination_locator).casefold() == destination.casefold())) :
                result_flag = True
        self.conditional_write(result_flag,
            positive='Correct source and destination locations found on the redirect page!',
            negative='Incorrect source and destinations found on the redirect page!!',
            level='debug')

        return result_flag
