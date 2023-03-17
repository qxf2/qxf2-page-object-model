"""
This class models the main page on the Weather shoper
This page allows the user to buy the product based on the temperature mentioned on the page
If the temperature is more thaln 30, clicks on Buy Sunscreen button
else, clicks on Buy Moisturizer button
"""

import conf.locators_conf as locators
from utils.Wrapit import Wrapit


class Weather_main_page_object:

    #locators
    degree_temperature = locators.temperature
    product_sunscreen = locators.sunscreen
    product_moisturizer = locators.moisturizer
    confirmation = locators.confirmation

    # redirect_title = "redirect"

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_temperature(self):
        "get the temperature from the website"
        
        temperature_element = self.get_element(self.degree_temperature)
        temperature_value = temperature_element.text.strip().split()[0]

        return temperature_value
    

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def select_product(self, temperature_value):

        if int(temperature_value) > 30:
            result_flag = self.click_sunscreen()
        else:
            result_flag = self.click_moisturizer()

        self.conditional_write(result_flag,
            positive='Successfully clicked on the Buy product button',
            negative='Failed to click on the Buy product button',
            level='debug')
        
        return result_flag


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_sunscreen(self):
        "Click on 'Sunscreen' button"
        result_flag = self.click_element(self.product_sunscreen)
        self.conditional_write(result_flag,
            positive='Clicked on the "Sunscreen" button',
            negative='Failed to click on "click me" button',
            level='debug')

        return result_flag
    

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_moisturizer(self):
        "Click on 'Moisturizer' button"
        result_flag = self.click_element(self.product_moisturizer)
        self.conditional_write(result_flag,
            positive='Clicked on the "Moisturizer" button',
            negative='Failed to click on "click me" button',
            level='debug')

        return result_flag