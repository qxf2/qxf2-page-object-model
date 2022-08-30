import conf.weathershopper_locators_conf as locators
class Sunscreen_Object_Page:
    "Page Object for the weather shopper main page"
    #locators
    moisturizer_button=locators.moisturizer_button
    sunscreen_button=locators.sunscreen_button
    # get the temperature text   
    def get_sunscreen_button(self):
     Button=self.click_element(self.sunscreen_button)
     return Button

    

 

