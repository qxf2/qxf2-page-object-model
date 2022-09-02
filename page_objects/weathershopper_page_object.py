import conf.weathershopper_locators_conf as locators
class Weathershopper_Object_Page:
    "Page Object for the weather shopper main page"
    #locators for temperature_text
    temperature_text=locators.temperature_text
    #locators for moisturizer button
    moisturizer_button=locators.moisturizer_button
    #locators for sunscreen buton 
    sunscreen_button=locators.sunscreen_button
    #locators for add button
    add_button=locators.add_button
     #locators for cart button
    cart_button=locators.cart_button
     #locators for pay button
    pay_button=locators.pay_button
    
    # get the temperature text   
    def get_temperature_text(self):
     temp_text=self.get_special_text(self.temperature_text)
     temp_txt = int((temp_text)[0:2])
     print (temp_txt)
     return 
    # get the moisturizer button 
    def get_moisturizer_button(self):
     Button=self.click_element(self.moisturizer_button)
     return Button
    # get the sunscreen button  
    def get_sunscreen_button(self):
     Button=self.click_element(self.sunscreen_button)
     return Button
    # get the add button 
    def get_add_button(self):
     Button=self.click_element(self.add_button)
     return Button
    # get the cart button  
    def get_cart_button(self):
     Button=self.click_element(self.cart_button)
     return Button
    # get the pay button  
    def get_pay_button(self):
     Button=self.click_element(self.pay_button)
     return Button
    

 

