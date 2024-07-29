"""
Page Objects for Weathershopper payment page
"""
import conf.locators_conf as locators
from utils.Wrapit import Wrapit
from .Mobile_Base_Page import Mobile_Base_Page
import pytesseract
from PIL import Image, ImageEnhance
import glob

class WeatherShopperPayment(Mobile_Base_Page):
    """
    Page Object for Weathershopper payment page
    """    
    def enter_valid_payment_details(self, payment_details):
        "This method is to enter valid payment details"

        result_flag = self.click_element(locators.payment_method_dropdown)
        result_flag &= self.click_element(locators.payment_card_type.format(payment_details["card_type"]))
        result_flag &= self.set_text(locators.payment_email, payment_details["email"])
        result_flag &= self.set_text(locators.payment_card_number, payment_details["card_number"])
        result_flag &= self.set_text(locators.payment_card_expiry, payment_details["card_expiry"])
        result_flag &= self.set_text(locators.payment_card_cvv, payment_details["card_cvv"])
        result_flag &= self.click_element(locators.pay_button)
        if self.get_element(locators.payment_success, verbose_flag=False) is None:
            result_flag &= False

        return result_flag
    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def enter_invalid_email(self, payment_details):
        "this method to validate invalid email entry"
        result_flag = self.click_element(locators.payment_method_dropdown)
        result_flag &= self.click_element(locators.payment_card_type.format(payment_details["card_type"]))
        result_flag &= self.set_text(locators.payment_email, payment_details["email"])
        result_flag &= self.set_text(locators.payment_card_number, payment_details["card_number"])
        result_flag &= self.set_text(locators.payment_card_expiry, payment_details["card_expiry"])
        result_flag &= self.set_text(locators.payment_card_cvv, payment_details["card_cvv"])
        result_flag &= self.click_element(locators.pay_button)
        result_flag &= self.click_element(locators.payment_email)

        return result_flag
    
    @Wrapit._exceptionHandler
    def image_to_string(self, payment_details):
        # Use glob to find the file with a pattern
        image_path  = payment_details["image_path"]
        files = glob.glob(image_path)

        if files:
            # Assuming there is only one file matching the pattern
            file_path = files[0]
            print(f"Found file: {file_path}")
            # Load the image
            image = Image.open(file_path)
            # Perform OCR on the enhanced image
            text = pytesseract.image_to_string(image)
            result_flag = self.find_string(text,payment_details["substring"])
            return result_flag
        else:
            print(f"No matching file found.")
    
    def find_string(self,text,substring):
            # Check if the substring is in the input string
            if substring in text:
                print(substring)
                return True
            else:
                return False
        
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            