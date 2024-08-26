"""
Automated test for Weather Shopper mobile application -
Mock Payment screen field validations Before running this test
**************************************************************
For LINUX Users, please run the below two commands from CLI
- run: sudo apt-get update
- run: sudo apt-get install -y tesseract-ocr
For Windows Users: https://github.com/UB-Mannheim/tesseract/wiki
****************************************************************
The tests validates fields on the Mock Payment validation.
The fields are : Email, cardnumber, Expiration date, CVV.
Provided invalid values for Email, cardnumber, expiry date and cvv.
expiry date: Two more additional validations "Expiration date not in future
and Invalid month"
Due to inconsistency behavior of tessract(OCR), the code is commented for expiry
date, cvv, expiry date future date validation.
"""
# pylint: disable=E0401, C0413
import secrets
import time
import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from page_objects.PageFactory import PageFactory
import conf.weather_shopper_mobile_conf as conf

def visit_product_page(test_mobile_obj, temperature):
    "Visit the product page"
    product = None
    result_flag = False
    if temperature < 19:
        result_flag = test_mobile_obj.view_moisturizers()
        product = "Moisturizers"

    elif temperature > 32:
        result_flag = test_mobile_obj.view_sunscreens()
        product = "Sunscreens"

    else:
        skin_product = secrets.choice(['Moisturizers', 'Sunscreens'])
        if skin_product == 'Moisturizers':
            result_flag = test_mobile_obj.view_moisturizers()
            product = "Moisturizers"
        else:
            result_flag = test_mobile_obj.view_sunscreens()
            product = "Sunscreens"

    return product, result_flag

def get_items(test_mobile_obj):
    "Get most expensive item from the page"

    # Get all products from page
    all_items = test_mobile_obj.get_all_products()

    # Calculate most expensive item
    most_expensive_item = test_mobile_obj.get_most_expensive_item(all_items)

    return most_expensive_item

def add_items_to_cart(test_mobile_obj, most_expensive_item):
    "Add items to cart"
    # Add most expensive item to cart
    result_flag = test_mobile_obj.add_to_cart(most_expensive_item)

    return result_flag

def view_cart(test_mobile_obj):
    "View cart page"
    result_flag = test_mobile_obj.view_cart()

    return result_flag

def verify_cart(test_mobile_obj, most_expensive_item):
    "Verify cart total"
    # Verify cart total
    cart_total = test_mobile_obj.get_cart_total()
    item_prices = [most_expensive_item['price']]
    result_flag = test_mobile_obj.verify_total(cart_total, item_prices)

    return result_flag

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
        product,result_flag = visit_product_page(test_mobile_obj, temperature)

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

        #Get most expensive item from the page
        most_expensive_item = get_items(test_mobile_obj)

        #Add items to cart
        result_flag = add_items_to_cart(test_mobile_obj, most_expensive_item)
        test_mobile_obj.log_result(result_flag,
                                    positive="Successfully added items item to cart",
                                    negative="Failed to add one or mre items to the cart",
                                    level="critical")

        #View cart
        result_flag = view_cart(test_mobile_obj)
        test_mobile_obj.log_result(result_flag,
                                    positive="Successfully viewed cart",
                                    negative="Failed to view cart",
                                    level="critical")

        #Verify cart total
        result_flag = verify_cart(test_mobile_obj, most_expensive_item)
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

        result_flag = test_mobile_obj.navigate_to_field(fieldname="email", screenshotname="navigate_to_email_field")
        test_mobile_obj.log_result(result_flag,
                                   positive="Successfully navigated to email field",
                                   negative="Failed to navigate to email field")

        result_flag = test_mobile_obj.image_to_string(payment_details["image_path"],payment_details["substring"])
        test_mobile_obj.log_result(result_flag,
            positive="Successfully completed conversion",
            negative="Failure to complete conversion")
        time.sleep(10)
        #Enter payment details - cardnumber field validation
        payment_details = conf.invalid_cardnum_in_payment_details
        result_flag = test_mobile_obj.submit_payment_details(payment_details["card_type"],
                        payment_details["email"], payment_details["card_number"],
                        payment_details["card_expiry"], payment_details["card_cvv"])

        test_mobile_obj.log_result(result_flag,
                                positive="Successfully submitted payment details",
                                negative="Failed to submit payment details")

        result_flag = test_mobile_obj.navigate_to_field(fieldname="card number", screenshotname="navigate_to_cardnumber_field")
        test_mobile_obj.log_result(result_flag,
                                   positive="Successfully navigated to cardnumber field",
                                   negative="Failed to navigate to cardnumber field")

        result_flag = test_mobile_obj.image_to_string(payment_details["image_path"], 
                      payment_details["substring"])
        test_mobile_obj.log_result(result_flag,
            positive="Successfully completed conversion",
            negative="Failure to complete conversion")
        """
        time.sleep(10)
        #Enter payment details - expiry date field validation
        payment_details = conf.invalid_expirydate_in_payment_details
        result_flag = test_mobile_obj.submit_payment_details(payment_details["card_type"],
                        payment_details["email"], payment_details["card_number"],
                        payment_details["card_expiry"], payment_details["card_cvv"])

        test_mobile_obj.log_result(result_flag,
                                positive="Successfully submitted payment details",
                                negative="Failed to submit payment details")

        result_flag = test_mobile_obj.navigate_to_field(fieldname="date", screenshotname="navigate_to_cardexpiry_field")
        test_mobile_obj.log_result(result_flag,
                                   positive="Successfully navigated to expiry date field",
                                   negative="Failed to navigate to expiry date field")

        result_flag = test_mobile_obj.image_to_string(payment_details["image_path"], 
                      payment_details["substring"])
        test_mobile_obj.log_result(result_flag,
            positive="Successfully completed conversion",
            negative="Failure to complete conversion")
        

        #Enter payment details - expiration date in future validation
        payment_details = conf.invalid_futuredate_in_payment_details
        result_flag = test_mobile_obj.submit_payment_details(payment_details["card_type"],
                        payment_details["email"], payment_details["card_number"],
                        payment_details["card_expiry"], payment_details["card_cvv"])

        test_mobile_obj.log_result(result_flag,
                                positive="Successfully submitted payment details",
                                negative="Failed to submit payment details")

        result_flag = test_mobile_obj.navigate_to_field(fieldname="future date",screenshotname="navigate_to_futuredate_field")
        test_mobile_obj.log_result(result_flag,
                                   positive="Successfully navigated to expirydate(futuredate) field",
                                   negative="Failed to navigate to expirydate(futuredate) field")

        time.sleep(10)
        result_flag = test_mobile_obj.image_to_string(payment_details["image_path"], 
                      payment_details["substring"])
        test_mobile_obj.log_result(result_flag,
            positive="Successfully completed conversion",
            negative="Failure to complete conversion")

        
        #Enter payment details - cvv field validation
        payment_details = conf.invalid_cvv_in_payment_details
        result_flag = test_mobile_obj.submit_payment_details(payment_details["card_type"],
                        payment_details["email"], payment_details["card_number"],
                        payment_details["card_expiry"], payment_details["card_cvv"])

        test_mobile_obj.log_result(result_flag,
                                positive="Successfully submitted payment details",
                                negative="Failed to submit payment details")

        result_flag = test_mobile_obj.navigate_to_field(fieldname="cvv",screenshotname="navigate_to_cardcvv_field")
        test_mobile_obj.log_result(result_flag,
                                   positive="Successfully navigated to cvv field",
                                   negative="Failed to navigate to cvv field")
        
        time.sleep(10)
        result_flag = test_mobile_obj.image_to_string(payment_details["image_path"], 
                      payment_details["substring"])
        test_mobile_obj.log_result(result_flag,
            positive="Successfully completed conversion",
            negative="Failure to complete conversion")
        """
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
    
    
