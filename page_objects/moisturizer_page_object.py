import conf.weathershopper_locators_conf as locators
class Moisturizer_Object_Page:
    "Page Object for the weather shopper main page"
    #locators
    moisturizer_button=locators.moisturizer_button
    sunscreen_button=locators.sunscreen_button
    # get the temperature text   
    def get_moisturizer_button(self):
     Button=self.click_element(self.moisturizer_button)
     return Button

    

 

