"""
This class models the main Selenium tutorial page.
URL: selenium-tutorial-main
The page consists of a header, footer, form and table objects
"""

from .Base_Page import Base_Page
from .sunscreen_page_object import Sunscreen_page_object
from .moisturizer_page_object import Moisturizer_page_object
from .cart_page_object import Cart_object
from .iframe_object import Iframe_objects
from .header_object import Header_Object
from .footer_object import Footer_Object
import conf.locators_conf as locators
from utils.Wrapit import Wrapit


class Tutorial_Main_Page(Base_Page,Header_Object,Footer_Object,Sunscreen_page_object,Moisturizer_page_object,
                            Cart_object,Iframe_objects):
    "Page Object for the tutorial's main page"


    #locators
    degree_temperature = locators.temperature
    product_sunscreen = locators.sunscreen
    product_moisturizer = locators.moisturizer
    # price_list = locators.price_list
    # add_button = locators.add_button
    # cart_button = locators.cart_id
    # card_pay = locators.card_pay
    # ifram = locators.ifram
    # add_item = locators.add_item

    # email_id = locators.email_id
    # card_id = locators.card_id
    # cc_exp = locators.cc_exp
    # cvc_id = locators.cvc_id
    # zip_id = locators.zip_id
    # submit = locators.submit
    confirmation = locators.confirmation

    #4. Get the test details from the conf file
    # card_number = conf.card_number

    redirect_title = "redirect"
    
    def start(self):
        "Use this method to go to specific URL -- if needed"
        url = '/'
        self.open(url)


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
    
#-------------------------SUNSCREEN----------------------------
    # @Wrapit._exceptionHandler
    # @Wrapit._screenshot
    # def add_to_cart(self):

    #     result_flag = self.click_element(self.add_item)

    #     self.conditional_write(result_flag,
    #         positive='Clicked on the "ADD" button',
    #         negative='Failed to click on "ADD" button',
    #         level='debug')
        
    #     return result_flag
    

    # @Wrapit._exceptionHandler
    # @Wrapit._screenshot
    # def click_cart(self):
    #     "Click on 'Cart' button"
    #     result_flag = self.click_element(self.cart_button)
    #     self.conditional_write(result_flag,
    #         positive='Clicked on the "Cart" button',
    #         negative='Failed to click on "Cart button" button',
    #         level='debug')
        
    #     return result_flag
#-------------------------SUNSCREEN----------------------------


    # @Wrapit._exceptionHandler
    # @Wrapit._screenshot
    # def click_pay_with_card(self):
    #     "Click on 'Pay with card' button"
    #     result_flag = self.click_element(self.card_pay)
    #     self.conditional_write(result_flag,
    #         positive='Clicked on the "Pay with card" button',
    #         negative='Failed to click on "Pay with card" button',
    #         level='debug')
        
    #     return result_flag
    
#-------------------------CART----------------------------

    # @Wrapit._exceptionHandler
    # @Wrapit._screenshot
    # def switch_frame_to(self):

    #     result_flag= self.switch_frame(name='stripe_checkout_app',index=None,wait_time=2)
    #     print("sssssssssssssssssssssssss")
    #     self.conditional_write(result_flag,
    #         positive='Successfully switched to the iframe',
    #         negative='Failed switching to iframe',
    #         level='debug')

#-------------------------------------------------filling form

    # @Wrapit._exceptionHandler
    # @Wrapit._screenshot
    # def email_info(self, email_add):
    #     result_flag = self.set_text(self.email_id,email_add)

    #     self.conditional_write(result_flag,
    #         positive='Set the email to: %s'%email_add,
    #         negative='Failed to set the email in the form',
    #         level='debug')

    #     return result_flag
    
#   ----------------------------------------------CARD NUMBER----------------------------------------------
#     @Wrapit._exceptionHandler
#     @Wrapit._screenshot
#     def card_info(self,card_num):
# # Retrives the Card number and card expiry date from the external file and sends it to the payment form
        
#         num = card_num

#         for nm in num:
#             result_flag &= self.set_text(self.card_id, nm)
        
#         self.conditional_write(result_flag,
#             positive='Set the card_number to: %s'%nm,
#             negative='Failed to set the card_number in the form',
#             level='debug')

#         return result_flag


        # num1 = conf.card_number
        # for nm in num1:
        #     conf.card_num.send_keys(nm)

        # cc_expx = self.driver.find_element(*cc)

        # for date in cc_date:
        #     cc_expx.send_keys(date)
            
#----------------------------------------------++++++----------------------------------------------
    # @Wrapit._exceptionHandler
    # @Wrapit._screenshot
    # def cvc_info(self, cvc):
    #     result_flag = self.set_text(self.email_id,cvc)

    #     self.conditional_write(result_flag,
    #         positive='Set the cvc to: %s'%cvc,
    #         negative='Failed to set the email in the form',
    #         level='debug')

    #     return result_flag