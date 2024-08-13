"""
Page objects for the home page in Weathershopper application.
"""
# pylint: disable = W0212,E0401
import conf.locators_conf as locators
from utils.Wrapit import Wrapit
from core_helpers.mobile_app_helper import Mobile_App_Helper

class WeatherShopperHomePage(Mobile_App_Helper):
    "Page objects for home page in Weathershopper application."
    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_temperature(self):
        "This method is to get the temperature in the Weather Shopper application."
        temperature = locators.temperature
        current_temperature = self.get_text(temperature)
        self.write(f"Current temperature is {int(current_temperature)}", level='debug')
        return int(current_temperature)

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def view_moisturizers(self):
        "This method is to click on Moisturizer tab in the Weather Shopper application."
        moisturizers = locators.moisturizers
        result_flag = self.click_element(moisturizers)
        self.conditional_write(result_flag,
            positive='Successfully clicked on Moisturizer tab',
            negative='Failed to click on Moisturizer tab',
            level='debug')
        self.switch_page("weathershopper products page")
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def view_sunscreens(self):
        "This method is to click on Sunscreen tab in the Weather Shopper application."
        sunscreens = locators.sunscreens
        result_flag = self.click_element(sunscreens)
        self.conditional_write(result_flag,
            positive='Successfully clicked on Sunscreen tab',
            negative='Failed to click on Sunscreen tab',
            level='debug')
        self.switch_page("weathershopper products page")
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_on_menu_option(self):
        "Click on Menu option"
        result_flag = self.click_element(locators.menu_option)
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_developed_by_label(self):
        "Get the developed by label"
        label = self.get_text(locators.developed_by)
        return label.decode("utf-8")

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_about_app_label(self):
        "Get the about app label"
        label = self.get_text(locators.about_app)
        return label.decode("utf-8")

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_automation_framework_label(self):
        "Get the automation framework label"
        label = self.get_text(locators.framework)
        return label.decode("utf-8")

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_privacy_policy_label(self):
        "Get the privacy policy label"
        label = self.get_text(locators.privacy_policy)
        return label.decode("utf-8")

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_contact_us_label(self):
        "Get the contact us label"
        label = self.get_text(locators.contact_us)
        return label.decode("utf-8")

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_get_developed_by_option(self):
        "Click developed by menu option"
        result_flag = self.click_element(locators.developed_by)
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_about_app_option(self):
        "Click about app menu option"
        result_flag = self.click_element(locators.about_app)
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_automation_framework_option(self):
        "Click automation framework menu option"
        result_flag = self.click_element(locators.framework)
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_contact_us_option(self):
        "Click contact us menu option"
        result_flag = self.click_element(locators.contact_us)
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def dismiss_chrome_welcome(self):
        "Dismiss Chrome welcome setting"
        self.handle_chrome_welcome_page(locators.chrome_welcome_dismiss, locators.turn_off_sync_button)

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def switch_to_app_context(self):
        "Switch to app context to access mobile app elements"
        result_flag = self.switch_context("NATIVE_APP")
        self.conditional_write(result_flag,
                               positive="Switched to NATIVE_APP context",
                               negative="Unable to switch to NATIVE_APP context")
