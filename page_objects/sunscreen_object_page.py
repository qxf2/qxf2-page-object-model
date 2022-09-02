"""
This class models the sunscreen_object page.
"""
import conf.weathershopper_locators_conf as locators

class Sunscreen_Object_Page:
    "Page Object for the sunscreen button"
    #locator for sunscreen button
    sunscreen_button=locators.sunscreen_button
   
    # get the sunscreen button   
    def get_sunscreen_button(self):
     Button=self.click_element(self.sunscreen_button)
     return Button

    

 

