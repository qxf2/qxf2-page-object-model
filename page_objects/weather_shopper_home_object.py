"""
This class models the weather shopper home page
The page consists of some texts, buttons, links
"""
import conf.locators_conf as locators
from utils.Wrapit import Wrapit

class Weather_Shopper_Home_Object:
    "Page object for the weather shopper home page"

    # locators
    temperature_text = locators.temperature_text
    moisturizers_button = locators.moisturizers_button
    sunscreens_button = locators.sunscreens_button
    information_icon = locators.information_icon
    qxf2_link = locators.qxf2_link
    buy_button = locators.buy_button
    
    # Get temperature text
    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_temperature_text(self):
        "Get the temperature text"
        temp_text = self.get_text(self.temperature_text)
        temper_text = temp_text.decode('utf-8')
        temperature = int(temper_text.split()[0])
        print("current temperature is :",temperature)
        return temperature
        
    # Click moisturizers button
    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_moisturizers_button(self):
        "Click moisturizers button"
        moisturizer_button = self.click_element(self.moisturizers_button)
        return moisturizer_button

    # Click sunscreens button
    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_sunscreens_button(self):
        "Click sunscreens button"
        sunscreen_button = self.click_element(self.sunscreens_button)
        return sunscreen_button

    # Click information icon
    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_information_icon(self):
        "Click information icon"
        info_icon = self.click_element(self.information_icon)
        return info_icon

    # Click qxf2 services link
    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_qxf2_link(self):
        "Click qxf2 sevices link"
        click_link = self.click_element(self.qxf2_link)
        return click_link

    