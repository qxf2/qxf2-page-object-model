"""
This class models the Search Buses form object on the redBus main page 
The form consists of two dropdown fields, two date selection calendars and a button
"""

from .Base_Page import Base_Page
import conf.locators_conf as locators
import re, time
from utils.Wrapit import Wrapit


class redBus_Search_Buses_Object():
    "Page object for the Search Buses Form"
    
    #locators
    source_field = locators.source
    destination_field = locators.destination
    onward_date_field = locators.onward_date
    return_date_field = locators.return_date
    search_buses_button = locators.search_buses_button
    

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def set_source(self,source):
        "Set the source location on the form"
        result_flag = self.set_text(self.source_field,source)
        self.conditional_write(result_flag,
            positive='Set the source field to: %s'%source,
            negative='Failed to set the source field in the search buses form',
            level='debug')

        return result_flag 

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def set_destination(self,destination):
        "Set the destination location on the form"
        result_flag = self.set_text(self.destination_field,destination)
        self.conditional_write(result_flag,
            positive='Set the destination field to: %s'%destination,
            negative='Failed to set the destination field in the search buses form',
            level='debug')

        return result_flag 

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def set_onward_date(self,onward_date):
        "Set the onward date on the form"
        result_flag = self.set_text(self.onward_date_field,onward_date)
        self.conditional_write(result_flag,
            positive='Set the onward date to: %s'%onward_date,
            negative='Failed to set the onward date in the search buses form',
            level='debug')

        return result_flag 

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def set_return_date(self,return_date):
        "Set the return date on the form"
        result_flag = self.set_text(self.return_date_field,return_date)
        self.conditional_write(result_flag,
            positive='Set the return date to: %s'%return_date,
            negative='Failed to set the return date in the search buses form',
            level='debug')

        return result_flag 

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_on_search_buses(self):
        "Click on 'Search Buses' button"
        
        result_flag = self.click_element(self.search_buses_button)
        time.sleep(5)
        self.conditional_write(result_flag,
            positive='Clicked on the "Search Buses" button',
            negative='Failed to click on "Search Buses" button',
            level='debug')

        return result_flag
    
    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def submit_form(self,source,destination,onward_date,return_date):
        "Submit the form"
        result_flag = self.set_source(source)
        result_flag &= self.set_destination(destination)
        result_flag &= self.set_onward_date(onward_date)
        result_flag &= self.set_return_date(return_date)
        result_flag &= self.click_on_search_buses()
              
        return result_flag
        
    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def check_redirect(self, source, destination):
        "Check if redirected to the search results page"
        time.sleep(5)
        result_flag = False
                
        if (re.split('[, ]', source)[0] in self.driver.current_url) and (re.split('[, ]', source)[0] in self.driver.current_url):
            result_flag = True
            self.switch_page("redbus search results page")
            
        return result_flag
