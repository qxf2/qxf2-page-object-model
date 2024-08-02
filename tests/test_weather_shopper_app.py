"""
Automated test for Weather Shopper mobile application
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

        #Get least and most expensive item from the page
        least_expensive_item, most_expensive_item = get_items(test_mobile_obj)

        #Add items to cart
        result_flag = add_items_to_cart(test_mobile_obj, least_expensive_item, most_expensive_item)
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
        result_flag = verify_cart(test_mobile_obj, least_expensive_item, most_expensive_item)
        test_mobile_obj.log_result(result_flag,
                                positive="Cart total is correct",
                                negative="Total is incorrect")

        #Change quantity of item in cart and verify cart total
        quantity = 2
        result_flag = change_quantity_and_verify(test_mobile_obj, least_expensive_item,
                        most_expensive_item, quantity)

        test_mobile_obj.log_result(result_flag,
                                positive="Successfully changed quantity of item",
                                negative="Failed to change quantity of item")

        #Delete item from cart and verify cart total
        result_flag = delete_item_and_verify(test_mobile_obj, least_expensive_item,
                        most_expensive_item, quantity)
        test_mobile_obj.log_result(result_flag,
                            positive="Total after deletion is accurate",
                            negative="Total after deletion is incorrect")

        #Checkout to payents page
        result_flag = checkout(test_mobile_obj)
        test_mobile_obj.log_result(result_flag,
                                    positive="Successfully entered checkout page",
                                    negative="Failed to checkout",
                                    level="critical")

        #Enter payment details
        payment_details = conf.valid_payment_details
        result_flag = test_mobile_obj.select_payment_method(payment_details["card_type"])
        test_mobile_obj.log_result(result_flag,
                                positive="Successfully selected payment method",
                                negative="Failed to select payment method")

        result_flag = test_mobile_obj.enter_email(payment_details["email"])
        test_mobile_obj.log_result(result_flag,
                            positive="Successfully entered email",
                            negative="Failed to enter email")

        result_flag = test_mobile_obj.enter_card_number(payment_details["card_number"])
        test_mobile_obj.log_result(result_flag,
                               positive="Successfully entered card number",
                               negative="Failed to enter card number")

        result_flag = test_mobile_obj.enter_card_expiry(payment_details["card_expiry"])
        test_mobile_obj.log_result(result_flag,
                               positive="Successfully entered card expiry",
                               negative="Failed to enter card expiry")

        result_flag = test_mobile_obj.enter_card_cvv(payment_details["card_cvv"])
        test_mobile_obj.log_result(result_flag,
                               positive="Successfully entered card CVV",
                               negative="Failed to enter card CVV")

        result_flag = test_mobile_obj.submit_payment()
        test_mobile_obj.log_result(result_flag,
                               positive="Successfully submitted payment",
                               negative="Failed to submit payment")

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
    "Get least and most expensive item from the page"

    # Get all products from page
    all_items = test_mobile_obj.get_all_products()

    # Calculate least and most expensive item
    least_expensive_item = test_mobile_obj.get_least_expensive_item(all_items)
    most_expensive_item = test_mobile_obj.get_most_expensive_item(all_items)

    return least_expensive_item, most_expensive_item

def add_items_to_cart(test_mobile_obj, least_expensive_item, most_expensive_item):
    "Add items to cart"
    result_flag = test_mobile_obj.add_to_cart(least_expensive_item)

    # Add most expensive item to cart
    result_flag &= test_mobile_obj.add_to_cart(most_expensive_item)

    return result_flag

def view_cart(test_mobile_obj):
    "View cart page"
    result_flag = test_mobile_obj.view_cart()

    return result_flag

def verify_cart(test_mobile_obj, least_expensive_item, most_expensive_item):
    "Verify cart total"
    # Verify cart total
    cart_total = test_mobile_obj.get_cart_total()
    item_prices = [least_expensive_item['price'], most_expensive_item['price']]
    result_flag = test_mobile_obj.verify_total(cart_total, item_prices)

    return result_flag

def change_quantity_and_verify(test_mobile_obj, least_expensive_item,
                                most_expensive_item, quantity):
    "Change quantity of item and verify cart total"
    # Change quantity of least expensive item
    result_flag = test_mobile_obj.change_quantity(least_expensive_item['name'], quantity=quantity)
    test_mobile_obj.log_result(result_flag,
                               positive="Successfully changed quantity of item",
                               negative="Failed to change quantity of item",
                               level = "critical")

    # Refresh cart total
    result_flag = test_mobile_obj.refresh_total_amount()
    test_mobile_obj.log_result(result_flag,
                               positive="Successfully refreshed total",
                               negative="Failed to refresh total")

    # Verify cart total after change in quantity
    cart_total_after_change = test_mobile_obj.get_cart_total()
    item_prices = [least_expensive_item['price'] * quantity, most_expensive_item['price']]
    result_flag = test_mobile_obj.verify_total(cart_total_after_change, item_prices)

    return result_flag

def delete_item_and_verify(test_mobile_obj, least_expensive_item, most_expensive_item, quantity):
    "Delete item from cart and verify cart total"
    # Delete item from cart
    result_flag = test_mobile_obj.delete_from_cart(most_expensive_item['name'])
    test_mobile_obj.log_result(result_flag,
                               positive="Successfully deleted item from cart",
                               negative="Failed to delete item from cart",
                               level = "critical")

    # Verify cart total after deletion
    cart_total_after_deletion = test_mobile_obj.get_cart_total()
    item_prices = [least_expensive_item['price'] * quantity]
    result_flag = test_mobile_obj.verify_total(cart_total_after_deletion, item_prices)

    return result_flag

def checkout(test_mobile_obj):
    "Checkout to payments page"
    # Checkout
    result_flag = test_mobile_obj.checkout()

    return result_flag

