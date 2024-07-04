"""
Page object for Weathershopper application.
"""
# pylint: disable = W0212,E0401
import re
import conf.locators_conf as locators
from utils.Wrapit import Wrapit
from .Mobile_Base_Page import Mobile_Base_Page

class WeatherShopper(Mobile_Base_Page):
    "Page object for Weathershopper application."

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_temperature(self):
        "This method is to get the temperature in the Weather Shopper application."
        temperature = locators.temperature
        current_temperature = self.get_text(temperature)
        self.write(f"Current temperature is {int(current_temperature)}", level='debug')
        return int(current_temperature)
    
    
    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def verify_recommendation_text(self):
        "This method is to verify the recommendation Text based on the temperature."
        temperature = self.get_temperature()
        recommendation = locators.recommendation_text
        recommendation_text = self.get_text(recommendation)
        # Ensure recommendation_text is a string
        if isinstance(recommendation_text, bytes):
            recommendation_text = recommendation_text.decode('utf-8')

        recommendation_text = recommendation_text.strip().replace('\n', '')

        if temperature <= 19:
            expected_recommendation = "It's cold! Consider buying moisturizers"
        elif temperature >= 20 and temperature <= 33:
            expected_recommendation = "Choose products based on your skin type and condition"
        else:
            expected_recommendation = "It's hot!  Stay hydrated and use sunscreen"

        result_flag = expected_recommendation in recommendation_text
        self.conditional_write(result_flag,
            positive='Successfully validated recommendation text',
            negative='Failed to validate recommendation text',
            level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def view_moisturizers(self):
        "This method is to click on Moisturizer tab in the Weather Shopper application."

        moisturizers = locators.moisturizers
        result_flag = self.click_element(moisturizers)
        self.conditional_write(result_flag,
            positive='Successfully clicked on Moisturizer tab',
            negative='Failed to click on Moisturizer tab',
            level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def view_sunscreens(self):
        "This method is to click on Sunscreen tab in the Weather Shopper application."

        sunscreens = locators.sunscreens
        result_flag = self.click_element(sunscreens)
        self.conditional_write(result_flag,
            positive='Successfully clicked on Sunscreen tab',
            negative='Failed to click on Sunscreen tab',
            level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def zoom_in_product_image(self, product_type):
        "This method is to zoom in the product image in the Weather Shopper application."

        if product_type == "Moisturizers":
            product_image = locators.image_of_moisturizer
            result_flag = self.click_element(product_image)
        else:
            product_image = locators.image_of_sunscreen
            result_flag = self.click_element(product_image)

        self.conditional_write(result_flag,
            positive='Successfully zoomed in product image',
            negative='Failed to zoom in product image',
            level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_all_products(self):
        "This method is to get all items from product page."

        all_products = []
        max_scrolls = 50
        for attempt in range(max_scrolls):
            # Get product names and prices
            product_names = self.get_elements(locators.product_name)
            product_prices = self.get_elements(locators.product_price)

            # Loop through the products and store the product names and prices in a list
            for name, price in zip(product_names, product_prices):
                product_name = self.get_text(name, dom_element_flag=True)
                product_price = self.get_text(price, dom_element_flag=True)

                # Append the product name and price to the list if it is not already in the list
                if {"name": product_name.decode(),
                    "price": float(product_price)} not in all_products:
                    all_products.append({"name": product_name.decode(),
                    "price": float(product_price)})

            # Scroll forward
            result_flag = self.scroll_forward()

            # If products are the same as the previous scroll, break the loop
            products_after_scroll = self.get_elements(locators.product_name)
            if products_after_scroll == product_names:
                break

            # If it's the last attempt and we haven't reached the end, set result_flag to False
            if attempt == max_scrolls - 1:
                result_flag &= False

        self.conditional_write(result_flag,
            positive='Successfully scrolled to the end of the page',
            negative='Failed to scroll to the end of the page',
            level='debug')
        return all_products

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_least_expensive_item(self, all_items):
        "This method is to get the least expensive item from the given list of items"

        least_expensive_item = min(all_items, key=lambda x: x['price'])
        self.write(f"Least expensive item is {least_expensive_item}")
        return least_expensive_item

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_most_expensive_item(self, all_items):
        "This method is to get the most expensive item from the given list of items"

        most_expensive_item = max(all_items, key=lambda x: x['price'])
        self.write(f"Most expensive item is {most_expensive_item}")
        return most_expensive_item

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def add_to_cart(self,item):
        "This method is to click on Add to cart button in the Weather Shopper application."

        result_flag = self.scroll_to_bottom()
        result_flag &= self.swipe_to_element(locators.recycler_view,
                    locators.add_to_cart.format(item['name']),
                    direction="down")
        result_flag &= self.click_element(locators.add_to_cart.format(item['name']))
        self.conditional_write(result_flag,
            positive=f"Successfully added {item['name']} to cart",
            negative=f"Failed to add {item['name']} to cart",
            level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def view_cart(self):
        "This method is to click on Cart button in the Weather Shopper application."

        cart = locators.cart
        result_flag = self.click_element(cart)
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def get_cart_total(self):
        "This method is to get the total price in the cart."

        cart_total = self.get_text(locators.total_amount)
        # Extracting the numeric part using regular expression
        match = re.search(r'\d+\.\d+', cart_total.decode())
        total_amount = float(match.group()) if match else None

        if total_amount is None:
            self.write("Total amount is None", level='debug')
        else:
            self.write(f"Total amount is {total_amount}", level='debug')
        return total_amount

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def verify_total(self, cart_total, cart_item_1=0, cart_item_2=0):
        "This method is to verify the total price in the cart."

        if cart_total == cart_item_1 + cart_item_2:
            return True
        return False

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def change_quantity(self, item_to_change, quantity=2):
        "This method is to change the quantity of an item in the cart"

        result_flag = self.set_text(locators.edit_quantity.format(item_to_change), quantity)
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def refresh_total_amount(self):
        "This method is to refresh the total amount in the cart."

        result_flag = self.click_element(locators.refresh_button)
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def delete_from_cart(self, item_to_delete):
        "This method is to delete an item from the cart"

        result_flag = self.click_element(locators.checkbox.format(item_to_delete))
        result_flag &= self.click_element(locators.delete_from_cart_button)
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def checkout(self):
        "This method is to go to the Checkout page"

        result_flag = self.click_element(locators.checkout_button)
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
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
