"""
Automated test for Weather Shopper mobile application
"""

# pylint: disable=E0401, C0413
import time
import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from page_objects.PageFactory import PageFactory
import conf.weather_shopper_mobile_conf as conf

@pytest.mark.MOBILE
def test_weather_shopper_app(test_mobile_obj):
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

        #Change quantity of item in cart and verify cart total
        quantity = 2
        result_flag = test_mobile_obj.change_quantity_and_verify(least_expensive_item,
                        most_expensive_item, quantity)

        test_mobile_obj.log_result(result_flag,
                                positive="Successfully changed quantity of item",
                                negative="Failed to change quantity of item")

        #Delete item from cart and verify cart total
        result_flag = test_mobile_obj.delete_item_and_verify(least_expensive_item,
                        most_expensive_item, quantity)
        test_mobile_obj.log_result(result_flag,
                            positive="Total after deletion is accurate",
                            negative="Total after deletion is incorrect")

        #Checkout to payents page
        result_flag = test_mobile_obj.checkout()
        test_mobile_obj.log_result(result_flag,
                                    positive="Successfully entered checkout page",
                                    negative="Failed to checkout",
                                    level="critical")

        #Enter payment details
        payment_details = conf.valid_payment_details
        result_flag = test_mobile_obj.submit_payment_details(payment_details["card_type"],
                        payment_details["email"], payment_details["card_number"],
                        payment_details["card_expiry"], payment_details["card_cvv"])

        test_mobile_obj.log_result(result_flag,
                                positive="Successfully submitted payment details",
                                negative="Failed to submit payment details")

        #Verify if payment was successful
        result_flag = test_mobile_obj.verify_payment_success()
        test_mobile_obj.log_result(result_flag,
                               positive="Payment was successful",
                               negative="Payment was not successful")

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
