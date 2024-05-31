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
        # Initialize flags for tests summary.
        expected_pass = 0
        actual_pass = -1

        # Create a test object.
        test_mobile_obj = PageFactory.get_page_object("weather shopper app")
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

        #Verify payment
        result_flag = verify_payment(test_mobile_obj)
        test_mobile_obj.log_result(result_flag,
                                positive="Successfully completed payment",
                                negative="Failure to complete payment")

        # Print out the results.
        test_mobile_obj.write(f'Script duration: {int(time.time() - start_time)} seconds\n')
        test_mobile_obj.write_test_summary()

        # Teardown and Assertion.
        expected_pass = test_mobile_obj.result_counter
        actual_pass = test_mobile_obj.pass_counter

    except Exception as e:
        print(f"Exception when trying to run test: {__file__}")
        print(f"Python says: {str(e)}")

    assert expected_pass == actual_pass, f"Test failed: {__file__}"

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
        skin_product = random.choice(['Moisturizers', 'Sunscreens'])
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
    result_flag = test_mobile_obj.verify_total(cart_total,
                                               least_expensive_item['price'],
                                               most_expensive_item['price'])

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
    result_flag = test_mobile_obj.verify_total(cart_total_after_change,
                                               least_expensive_item['price'] * quantity,
                                               most_expensive_item['price'])

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
    result_flag = test_mobile_obj.verify_total(cart_total_after_deletion,
                                               least_expensive_item['price'] * quantity)

    return result_flag

def checkout(test_mobile_obj):
    "Checkout to payments page"
    # Checkout
    result_flag = test_mobile_obj.checkout()

    return result_flag

def verify_payment(test_mobile_obj):
    "Submit payment details and verify payment"
    # Enter valid payment details and submit payment
    payment_details = {
    "card_type": "Debit Card",
    "email": "qxf2tester@example.com",
    "card_number": "1234567890123456",
    "card_expiry": "12/25",
    "card_cvv": "123"
    }
    result_flag = test_mobile_obj.enter_valid_payment_details(payment_details)
    return result_flag
