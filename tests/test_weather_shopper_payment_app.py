"""
Automated test for Weather Shopper mobile application -
Mock Payment screen field validations. 

Pre-requisite: Before running this test-
**************************************************************
For LINUX Users, please run the below two commands from CLI
- run: sudo apt-get update
- run: sudo apt-get install -y tesseract-ocr
For Windows Users: https://github.com/UB-Mannheim/tesseract/wiki
****************************************************************
The tests validates fields on the Mock Payment validation.
The fields are : Email, cardnumber.
Provided invalid values for Email, cardnumber.
"""
# pylint: disable=E0401,C0413,C0301

import time
import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from page_objects.PageFactory import PageFactory
import conf.weather_shopper_mobile_conf as conf

pytest.skip("Skipping test as ocr fail in circleCI", allow_module_level=True)
@pytest.mark.MOBILE
def test_weather_shopper_payment_app(test_mobile_obj):
    "Run the test."
    try:
        # Initialize flags for tests summary.
        expected_pass = 0
        actual_pass = -1

        # Create a test object.
        test_mobile_obj = PageFactory.get_page_object("weathershopper home page")
        start_time = int(time.time())

        # Run test steps
        #Get temperature from hompage
        temperature = test_mobile_obj.get_temperature()

        #Visit the product page
        product,result_flag = test_mobile_obj.visit_product_page(temperature)

        if product == "Moisturizers":
            test_mobile_obj.log_result(result_flag,
                                    positive="Successfully visited moisturizer page",
                                    negative="Failed to visit moisturizer page",
                                    level="critical")
        else:
            test_mobile_obj.log_result(result_flag,
                                    positive="Successfully visited sunscreens page",
                                    negative="Failed to visit sunscreens page",
                                    level="critical")
        # Get all products from page
        all_items = test_mobile_obj.get_all_products()

          #Get least and most expensive item from the page
        least_expensive_item, most_expensive_item = test_mobile_obj.get_least_and_most_expensive_items(all_items)
        items = [least_expensive_item, most_expensive_item]

        #Add items to cart
        result_flag = test_mobile_obj.add_items_to_cart(items)
        test_mobile_obj.log_result(result_flag,
                                    positive="Successfully added items item to cart",
                                    negative="Failed to add one or mre items to the cart",
                                    level="critical")

        #View cart
        result_flag = test_mobile_obj.view_cart()
        test_mobile_obj.log_result(result_flag,
                                    positive="Successfully viewed cart",
                                    negative="Failed to view cart",
                                    level="critical")

        #Verify cart total
        cart_total = test_mobile_obj.get_cart_total()
        item_prices = [item['price'] for item in items]
        result_flag = test_mobile_obj.verify_total(cart_total, item_prices)

        test_mobile_obj.log_result(result_flag,
                                positive="Cart total is correct",
                                negative="Total is incorrect")


        #Checkout to payments page
        result_flag = test_mobile_obj.checkout()
        test_mobile_obj.log_result(result_flag,
                                    positive="Successfully entered checkout page",
                                    negative="Failed to checkout",
                                    level="critical")

        #Enter payment details - email field validation
        payment_details = conf.invalid_email_in_payment_details
        result_flag = test_mobile_obj.submit_payment_details(payment_details["card_type"],
                        payment_details["email"], payment_details["card_number"],
                        payment_details["card_expiry"], payment_details["card_cvv"])

        test_mobile_obj.log_result(result_flag,
                                positive="Successfully submitted payment details",
                                negative="Failed to submit payment details")

        result_flag = test_mobile_obj.capture_payment_field_error(fieldname="email", screenshotname=payment_details["image_name"])
        test_mobile_obj.log_result(result_flag,
                                   positive="Successfully navigated and captured email field",
                                   negative="Failed to navigate to email field")

        result_flag, image_text = test_mobile_obj.get_string_from_image(payment_details["image_name"])
        test_mobile_obj.log_result(result_flag,
            positive="Able to get text from image",
            negative="Failed to get text from image")

        result_flag = test_mobile_obj.compare_string(image_text, payment_details["validation_message"])
        test_mobile_obj.log_result(result_flag,
            positive="Text from image matches the expected text: {0}".format(payment_details["validation_message"]),
            negative="Text from image does not match the expected text")

        #Enter payment details - cardnumber field validation
        payment_details = conf.invalid_cardnum_in_payment_details
        result_flag = test_mobile_obj.submit_payment_details(payment_details["card_type"],
                        payment_details["email"], payment_details["card_number"],
                        payment_details["card_expiry"], payment_details["card_cvv"])

        test_mobile_obj.log_result(result_flag,
                                positive="Successfully submitted payment details",
                                negative="Failed to submit payment details")

        result_flag = test_mobile_obj.capture_payment_field_error(fieldname="card number", screenshotname=payment_details["image_name"])
        test_mobile_obj.log_result(result_flag,
                                   positive="Successfully navigated and captured cardnumber field",
                                   negative="Failed to capture cardnumber field")

        result_flag, image_text = test_mobile_obj.get_string_from_image(payment_details["image_name"])
        test_mobile_obj.log_result(result_flag,
            positive="Able to get text from image",
            negative="Failed to get text from image")

        result_flag = test_mobile_obj.compare_string(image_text, payment_details["validation_message"])
        test_mobile_obj.log_result(result_flag,
            positive="Text from image matches the expected text: {0}".format(payment_details["validation_message"]),
            negative="Text from image does not match the expected text")

        # Print out the results.
        test_mobile_obj.write(f'Script duration: {int(time.time() - start_time)} seconds\n')
        test_mobile_obj.write_test_summary()

        # Teardown and Assertion.
        expected_pass = test_mobile_obj.result_counter
        actual_pass = test_mobile_obj.pass_counter

    except Exception as e:
        print(f"Exception when trying to run test: {__file__}")
        print(f"Python says: {str(e)}")

    if expected_pass != actual_pass:
        raise AssertionError(f"Test failed: {__file__}")
