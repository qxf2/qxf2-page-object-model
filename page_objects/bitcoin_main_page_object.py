"""
Page object for Bitcoin main Page.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import conf.locators_conf as locators
from utils.Wrapit import Wrapit


class Bitcoin_Main_Page_Object():
    "Page object bitcoin main page."

    #Locators of the mobile page elements.
    bitcoin_real_time_price_button = locators.bitcoin_real_time_price_button
    bitcoin_price_page_heading = locators.bitcoin_price_page_heading 


    @Wrapit._screenshot
    def click_on_real_time_price_button(self):
        "This method is to click on real time price page button."
        try:
            # Click on real time price page button.
            result_flag = None
            if self.click_element(self.bitcoin_real_time_price_button):
                result_flag = True
            else:
                result_flag = False    

            self.conditional_write(result_flag,
                positive='Click on bitcoin real time price page button.',
                negative='Failed to click on bitcoin real time price page button.',
                level='debug')

        except Exception,e:
            self.write("Exception while verifying real time price of the bitcoin.")  
            self.write(str(e))

        return result_flag


    @Wrapit._screenshot
    def check_redirect(self, expected_bitcoin_price_page_heading):
        "Check if we have been redirected to the bitcoin real time price page."
        result_flag = None
        bitcoin_price_page_heading = self.get_text_by_locator(self.bitcoin_price_page_heading)
        if bitcoin_price_page_heading == expected_bitcoin_price_page_heading:
            result_flag = True
        else:
            result_flag = False
        
        return result_flag


    @Wrapit._screenshot
    def visit_bitcoin_real_time_price_page(self, expected_bitcoin_price_page_heading):
        "This method is to visit bitcoin real time price page."
        result_flag = self.click_on_real_time_price_button()
        result_flag &= self.check_redirect(expected_bitcoin_price_page_heading)

        return result_flag



            

    

            

        
        
       




