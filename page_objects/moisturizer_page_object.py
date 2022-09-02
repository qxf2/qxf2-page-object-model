"""
This class models the moisturizer page_object page.
"""
import conf.weathershopper_locators_conf as locators

class Moisturizer_Object_Page:
    "Page Object for the moisturizer button"
    #locator for moisturizer button
    moisturizer_button=locators.moisturizer_button
    
# get the moisturizer button   
    def get_moisturizer_button(self):
     Button=self.click_element(self.moisturizer_button)
     return Button

    

 

