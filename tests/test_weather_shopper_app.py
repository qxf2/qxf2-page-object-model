"""
Automated test for Weather Shopper mobile application
"""

# pylint: disable=E0401, C0413
import random
import time
import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from page_objects.PageFactory import PageFactory

@pytest.mark.MOBILE
def test_weather_shopper_app(test_mobile_obj):
    "Run the test."
    try:
        # Initalize flags for tests summary.
        expected_pass = 0
        actual_pass = -1

        #1. Create a test object.
        test_mobile_obj = PageFactory.get_page_object("weather shopper app")

        start_time = int(time.time())
        temperature = test_mobile_obj.get_temperature()

        if temperature < 19:
            result_flag = test_mobile_obj.view_moisturizers()
            test_mobile_obj.log_result(result_flag,
                positive="Successfully visited moistorizer page",
                negative="Failed to visit moistorizer page",
                level="critical")
        elif temperature > 32:
            result_flag = test_mobile_obj.view_sunscreens()
            test_mobile_obj.log_result(result_flag,
                positive="Successfully visited sunscreens page",
                negative="Failed to visit sunscreens page",
                level="critical")
        else:
            skin_product = random.choice(['Moisturizers', 'Sunscreens'])
            if skin_product == 'Moisturizers':
                result_flag = test_mobile_obj.view_moisturizers()
            else:
                result_flag = test_mobile_obj.view_sunscreens()

            test_mobile_obj.log_result(result_flag,
                positive="Successfully visited random page",
                negative="Failed to visit random page",
                level="critical")

        #Get all products from page
        all_items = test_mobile_obj.get_all_products()

        #Calculate least and most expensive item
        least_expensive_item = test_mobile_obj.get_least_expensive_item(all_items)
        most_expensive_item = test_mobile_obj.get_most_expensive_item(all_items)

        #Add least expensive item to cart
        result_flag = test_mobile_obj.add_to_cart(least_expensive_item)
        test_mobile_obj.log_result(result_flag,
            positive="Successfully added least expensive item to cart",
            negative="Failed to add least expensive item to cart",
            level="critical")

        #Add most expensive item to cart
        result_flag = test_mobile_obj.add_to_cart(most_expensive_item)
        test_mobile_obj.log_result(result_flag,
            positive="Successfully added most expensive item to cart",
            negative="Failed to add most expensive item to cart",
            level="critical")

        #View cart
        result_flag = test_mobile_obj.view_cart()
        test_mobile_obj.log_result(result_flag,
            positive="Successfully visited cart page",
            negative="Failed to visit cart page",
            level="critical")

        #Verify cart total
        cart_total = test_mobile_obj.get_cart_total()
        resul_flag = test_mobile_obj.verify_total(cart_total,
            least_expensive_item['price'],
            most_expensive_item['price'])

        test_mobile_obj.log_result(resul_flag,
            positive="Cart total is correct",
            negative="Total is incorrect")

        #Change quantity of least expensive item
        quantity=2
        result_flag = test_mobile_obj.change_quantity(least_expensive_item['name'],
                    quantity=quantity)
        test_mobile_obj.log_result(result_flag,
            positive="Successfully changed quantity of item",
            negative="Failed to change quantity of item")

        #Refresh cart total
        result_flag = test_mobile_obj.refresh_total_amount()
        test_mobile_obj.log_result(result_flag,
            positive="Successfully refreshed total",
            negative="Failed to refresh total")

        #Verify cart total after change in quantity
        cart_total_after_change = test_mobile_obj.get_cart_total()
        resul_flag = test_mobile_obj.verify_total(cart_total_after_change,
                least_expensive_item['price']*quantity,
                most_expensive_item['price'])
        test_mobile_obj.log_result(resul_flag,
            positive="Total after changing quantity is accurate",
            negative="Total after changing quantity is incorrect")

        #Delete item from cart
        result_flag = test_mobile_obj.delete_from_cart(most_expensive_item['name'])
        test_mobile_obj.log_result(result_flag,
            positive="Successfully deleted item from cart",
            negative="Failed to delete item from cart")

        #Verify cart total after deletion
        cart_total_after_deletion = test_mobile_obj.get_cart_total()
        resul_flag = test_mobile_obj.verify_total(cart_total_after_deletion,
                 least_expensive_item['price']*quantity)
        test_mobile_obj.log_result(resul_flag,
            positive="Total after deletion is accurate",
            negative="Total after deletion is incorrect")

        #Checkout
        resul_flag = test_mobile_obj.checkout()
        test_mobile_obj.log_result(resul_flag,
            positive="Successfully entered checkout page",
            negative="Failed to checkout",
            level="critical")

        #Enter valid payment details and submit payment
        payment_details = {
            "card_type": "Debit Card",
            "email": "qxf2tester@example.com",
            "card_number": "1234567890123456",
            "card_expiry": "12/25",
            "card_cvv": "123"
        }
        result_flag = test_mobile_obj.enter_valid_payment_details(payment_details)
        test_mobile_obj.log_result(result_flag,
            positive="Successfully completed payment",
            negative="Failure to complete payment")

        test_mobile_obj.write(f'Script duration: {int(time.time() - start_time)} seconds\n')

        #6. Print out the results.
        test_mobile_obj.write_test_summary()

        #7. Teardown and Assertion.
        expected_pass = test_mobile_obj.result_counter
        actual_pass = test_mobile_obj.pass_counter

    except Exception as e:
        print(f"Exception when trying to run test: {__file__}")
        print(f"Python says: {str(e)}")

    assert expected_pass == actual_pass, f"Test failed: {__file__}"
