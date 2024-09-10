"""
This class models the objects of the home screen in Weathershopper application.
"""
import conf.locators_conf as locators
from utils.Wrapit import Wrapit
import secrets

class HomepageObjects:
    "Page object for the home screen in Weathershopper application."
    
    @Wrapit._exceptionHandler
    def visit_product_page(self, temperature):
        "Visit the product page"
        product = None
        result_flag = False
        if temperature < 19:
            result_flag = self.view_moisturizers()
            product = "Moisturizers"

        elif temperature > 32:
            result_flag = self.view_sunscreens()
            product = "Sunscreens"

        else:
            skin_product = secrets.choice(['Moisturizers', 'Sunscreens'])
            if skin_product == 'Moisturizers':
                result_flag = self.view_moisturizers()
                product = "Moisturizers"
            else:
                result_flag = self.view_sunscreens()
                product = "Sunscreens"

        return product, result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_temperature(self):
        "This method is to get the temperature in the Weather Shopper application."
        temperature = locators.temperature
        current_temperature = self.get_text(temperature)
        self.write(f"Current temperature is {int(current_temperature)}", level='debug')
        return int(current_temperature)

