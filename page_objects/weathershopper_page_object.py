import conf.weathershopper_locators_conf as locators
class Weathershopper_Object_Page:
    "Page Object for the weather shopper main page"
    #locators
    temperature_text=locators.temperature_text
    
    # get the temperature text   
    def get_temperature_text(self):
     text=self.get_text(self.temperature_text)
     print(text)
     return text

    

 

