"""
This class models the selection of products from Sunscreen page

"""
import conf.locators_conf as locators
from utils.Wrapit import Wrapit


class Sunscreen_page_object:
    "Page object for the sunscreen"

    #Locators
    price_list = locators.price_list
    # add_button = locators.add_button
    cart_button = locators.cart_id
    add_item = locators.add_item


    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def add_item_to_cart(self):

        result_flag = self.click_element(self.add_item)

        self.conditional_write(result_flag,
            positive='Clicked on the "ADD" button',
            negative='Failed to click on "ADD" button',
            level='debug')
        
        return result_flag
    

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_cart(self):
        "Click on 'Cart' button"
        result_flag = self.click_element(self.cart_button)
        self.conditional_write(result_flag,
            positive='Clicked on the "Cart" button',
            negative='Failed to click on "Cart button" button',
            level='debug')
        
        return result_flag
