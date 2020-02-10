"""
This class models the view buses object on the redBus search results page
<TBD>It consists of
"""

from .Base_Page import Base_Page
import conf.locators_conf as locators
from utils.Wrapit import Wrapit


class redBus_View_Buses_Object:
    "Page object for the View Buses Object"
    
    #locators
    view_seats_button = locators.view_seats_button
    seat_selection_message = locators.seat_selection_message

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_on_view_seats_button(self):
        "Click on 'View Seats' button under the first available bus"
        result_flag = self.click_element(self.view_seats_button)
        
        self.conditional_write(result_flag,
            positive='Clicked on the "View Seats" button',
            negative='Failed to click on "View Seats" button',
            level='debug')

        return result_flag

    def check_seat_selection_msg(self):
        "Verify if the seat selection message appears on click of view seats under the first available bus"    
        result_flag = self.check_element_present(self.seat_selection_message)
      
        self.conditional_write(result_flag,
            positive='Seat selection message appears on click of view seats',
            negative='Seat selection message does not appear on click of view seats',
            level='debug')

        return result_flag

    