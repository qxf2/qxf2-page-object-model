"""
Page object for Bitcoin price Page.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import conf.locators_conf as locators
from Mobile_Base_Page import Mobile_Base_Page
from utils.Wrapit import Wrapit
from bitcoin_main_page_object import Bitcoin_Main_Page_Object


class Bitcoin_Price_Page(Mobile_Base_Page, Bitcoin_Main_Page_Object):
    "Page object for real time prices of bitcoin page."

    # Locators of the bitcoin real time price page elements.
    bitcoin_price_in_usd = locators.bitcoin_price_in_usd  

    
    @Wrapit._screenshot
    def get_bitcoin_real_time_price(self):
        "This method is to get the real time price of the bitcoin."
        # Final result flag is to return False if expected price and real time price is different.
        try:
            # Get real time price of the bitcoin in usd.
            result_flag = None
            bitcoin_price_in_usd = self.get_text_by_locator(self.bitcoin_price_in_usd)
            if bitcoin_price_in_usd is not None:
                result_flag = True
            else:
                result_flag = False    

            self.conditional_write(result_flag,
                positive='Get the bitcoin real time price in usd.',
                negative='Failed to get the bitcoin real time price in usd.',
                level='debug')

        except Exception,e:
            self.write("Exception while verifying real time price of the bitcoin.")  
            self.write(str(e))

        return result_flag



    	   	

    

    		

        
        
       




