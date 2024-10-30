"""
The payment page in Weathershopper application.
"""
# pylint: disable = W0212,E0401,W0104,R0913,R1710,W0718,E0402

import os
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import conf.locators_conf as locators
from utils.Wrapit import Wrapit
from .weather_shopper_payment_objects import WeatherShopperPaymentPageObjects


class WeatherShopperPaymentPage(WeatherShopperPaymentPageObjects):

    "Page objects for payment page in Weathershopper application."

    @Wrapit._exceptionHandler
    def capture_payment_field_error(self,fieldname,screenshotname):
        """
        Navigating the cursor to the payment error field
        and capture the screenshot of the error prompt.
        """
        result_flag = self.click_payment_error_field(fieldname)
        self.hide_keyboard()
        self.save_screenshot(screenshot_name=screenshotname)

        return result_flag

    def click_payment_error_field(self,fieldname):
        """
        This method will show the error message
        """
        if fieldname == "email":
            result_flag = self.click_element(locators.payment_email)
        elif fieldname == "card number":
            result_flag = self.click_element(locators.payment_card_number)
        return result_flag

    @Wrapit._exceptionHandler
    def get_string_from_image(self, image_name):
        """
        This method opens the image, enhances it, and
        extracts the text from the image using Tesseract.
        """
        # Construct the full image path
        image_dir = self.screenshot_dir
        full_image_path = os.path.join(image_dir, f"{image_name}.png")
        result_flag = False
        # Check if the file exists
        if os.path.exists(full_image_path):
            # Load the image
            image = Image.open(full_image_path)
            # Enhance the image before OCR
            enhanced_image = self.preprocess_image(image)
            # Perform OCR on the enhanced image
            text = pytesseract.image_to_string(enhanced_image)
            result_flag = True
        else:
            text = ""
        return result_flag,text

    @Wrapit._exceptionHandler
    def compare_string(self,image_text,validation_string):
        """
        Check if the substring is in the input string
        """
        if validation_string in image_text:
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
            enhanced_image = enhancer.enhance(2)
            # Apply a filter to sharpen the image
            sharpened_image = enhanced_image.filter(ImageFilter.SHARPEN)
            return sharpened_image
        except Exception as preproc:
            print(f"Error during image preprocessing: {preproc}")
            return image  # Return original image if preprocessing fails
