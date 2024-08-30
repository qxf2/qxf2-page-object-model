"""
Page object for the payment page in Weathershopper application.
"""
# pylint: disable = W0212,E0401,W0104,R0913,R1710
import glob
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import conf.locators_conf as locators
from utils.Wrapit import Wrapit
from core_helpers.mobile_app_helper import Mobile_App_Helper


class WeatherShopperPaymentPage(Mobile_App_Helper):
    "Page objects for payment page in Weathershopper application."
    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def enter_card_cvv(self, card_cvv):
        "Enter the card CVV"
        result_flag = self.set_text(locators.payment_card_cvv, card_cvv)
        self.conditional_write(result_flag,
            positive=f'Successfully set the card CVV: {card_cvv}',
            negative=f'Failed to set the card CVV: {card_cvv}',
            level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def enter_card_expiry(self, card_expiry):
        "Enter the card expiry date"
        result_flag = self.set_text(locators.payment_card_expiry, card_expiry)
        self.conditional_write(result_flag,
            positive=f'Successfully set the card expiry date: {card_expiry}',
            negative=f'Failed to set the card expiry date: {card_expiry}',
            level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def enter_email(self, email):
        "Enter the email address"
        result_flag = self.set_text(locators.payment_email, email)
        self.conditional_write(result_flag,
            positive=f'Successfully set the email address: {email}',
            negative=f'Failed to set the email address: {email}',
            level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def enter_card_number(self, card_number):
        "Enter the card number"
        result_flag = self.set_text(locators.payment_card_number, card_number)
        self.conditional_write(result_flag,
            positive=f'Successfully set the card number: {card_number}',
            negative=f'Failed to set the card number: {card_number}',
            level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def select_payment_method(self, card_type):
        "Select the payment method"
        result_flag = self.click_element(locators.payment_method_dropdown)
        result_flag &= self.click_element(locators.payment_card_type.format(card_type))
        self.conditional_write(result_flag,
            positive=f'Successfully selected the payment method: {card_type}',
            negative=f'Failed to select the payment method: {card_type}',
            level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def submit_payment(self):
        "Click the pay button"
        result_flag = self.click_element(locators.pay_button)
        self.conditional_write(result_flag,
            positive='Successfully clicked on the pay button',
            negative='Failed to click on the pay button',
            level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def verify_payment_success(self):
        "Verify if the payment was successful"
        result_flag = self.get_element(locators.payment_success, verbose_flag=False) is not None
        self.conditional_write(result_flag,
            positive='Payment was successful',
            negative='Payment failed',
            level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def submit_payment_details(self,card_type,email,card_number,card_expiry,card_cvv):
        "Submit the form"
        result_flag = self.select_payment_method(card_type)
        result_flag &= self.enter_email(email)
        result_flag &= self.enter_card_number(card_number)
        result_flag &= self.enter_card_expiry(card_expiry)
        result_flag &= self.enter_card_cvv(card_cvv)
        result_flag &= self.submit_payment()
        return result_flag

    @Wrapit._exceptionHandler
    def navigate_to_field(self, fieldname,screenshotname):
        """
        Navigating the cursor to the desired field
        and capturing the screenshot of the error prompt.
        """
        if fieldname == "email":
            result_flag = self.click_element(locators.payment_email)
            self.hide_keyboard()
            self.save_screenshot(screenshot_name=screenshotname)
        else:
            result_flag = self.click_element(locators.payment_card_number)
            self.hide_keyboard()
            self.save_screenshot(screenshot_name=screenshotname)

        return result_flag

    @Wrapit._exceptionHandler
    def get_string_from_image(self, image_path, substring):
        """
        get_string_from_image() - The method extracts the text from the 
        image using tesseract.
        find_string() - Search the substring
        preprocess_image() - To enhance the image contrast 
        """
        # Use glob to find the file
        files = glob.glob(image_path)
        if files:
            # Assuming there is only one file matching the pattern
            file_path = files[0]
            print(f"Found file: {file_path}")

            # Load the image
            image = Image.open(file_path)
            # Enhance the image before OCR
            image = self.preprocess_image(image)
            # Perform OCR on the enhanced image
            text = pytesseract.image_to_string(image)
            result_flag = self.find_string(text,substring)

            return result_flag


    @Wrapit._exceptionHandler
    def find_string(self,text,substring):
        """
        Check if the substring is in the input string
        """
        if substring in text:
            print(f'Substring:{substring}')
            return True

    def preprocess_image(self, image):
        """
        Pre-process the image.
        """
        try:
            # Convert to grayscale
            grayscale_image = image.convert('L')

            # Enhance contrast
            enhancer = ImageEnhance.Contrast(grayscale_image)
            enhanced_image = enhancer.enhance(2)  # Adjust contrast factor as needed

            # Apply a filter to sharpen the image
            sharpened_image = enhanced_image.filter(ImageFilter.SHARPEN)

            return sharpened_image
        except Exception as preproc:
            print(f"Error during image preprocessing: {preproc}")
            return image  # Return original image if preprocessing fails
