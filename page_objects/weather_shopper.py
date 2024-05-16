"""
Page object for Bitcoin price Page.
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import conf.locators_conf as locators
from utils.Wrapit import Wrapit
from .Mobile_Base_Page import Mobile_Base_Page
import re


class Weather_Shopper(Mobile_Base_Page):
    "Page object for Weathershopper application."

    def get_temperature(self):
        "This method is to get the temperature in the Weather Shopper application."

        try:
            temperature = locators.temperature
            current_temperature = self.get_text(temperature)
        except Exception as e:
            self.write("Exception while trying to get temperature ")
            self.write(str(e))

        return int(current_temperature)

    def view_moisturizers(self):
        "This method is to click on Moisturizer tab in the Weather Shopper application."

        try:
            moisturizers = locators.moisturizers
            result_flag = self.click_element(moisturizers)
        except Exception as e:
            self.write("Exception while trying to click on Moisturizer tab")
            self.write(str(e))

        self.conditional_write(result_flag,
            positive='Successfully clicked on Moisturizer tab',
            negative='Failed to click on Moisturizer tab',
            level='debug')

        return result_flag

    def view_sunscreens(self):
        "This method is to click on Sunscreen tab in the Weather Shopper application."

        try:
            sunscreens = locators.sunscreens
            result_flag = self.click_element(sunscreens)
        except Exception as e:
            self.write("Exception while trying to click on Sunscreen tab")
            self.write(str(e))

        self.conditional_write(result_flag,
            positive='Successfully clicked on Sunscreen tab',
            negative='Failed to click on Sunscreen tab',
            level='debug')

        return result_flag

    def zoom_in_product_image(self, product_type):
        "This method is to zoom in the product image in the Weather Shopper application."

        try:
            if product_type == "Moisturizers":
                product_image = locators.image_of_moisturizer
                result_flag = self.click_element(product_image)
            else:
                product_image = locators.image_of_sunscreen
                result_flag = self.click_element(product_image)
        except Exception as e:
            self.write("Exception while trying to zoom in product image")
            self.write(str(e))

        self.conditional_write(result_flag,
            positive='Successfully zoomed in product image',
            negative='Failed to zoom in product image',
            level='debug')

        return result_flag  


    def get_all_products(self):
        "This method is to get all items from product page."

        try:
            all_products = []
            for _ in range(50):
                #Get product names and prices
                product_names = self.get_elements(locators.product_name)
                product_prices = self.get_elements(locators.product_price)

                #Loop through the products and store the product names and prices in a list
                for name,price in zip(product_names, product_prices):
                    product_name = self.get_text(name, dom_element_flag=True)
                    product_price = self.get_text(price, dom_element_flag=True)

                    #Append the product name and price to the list if it is not already in the list
                    if {"name":product_name.decode(),"price":float(product_price)} not in all_products:
                        all_products.append({"name":product_name.decode(),"price":float(product_price)})

                #Scroll forward
                self.scroll_forward()

                #If product are the same as the previous scroll, break the loop
                products_after_scroll = self.get_elements(locators.product_name)

                if products_after_scroll == product_names:
                    break
            return all_products
        
        except Exception as e:
            self.write("Exception while trying to get items")
            self.write(str(e))

    def get_least_expensive_item(self, all_items):
        "This method is to get the least expensive item from the given list of items"

        try:
            least_expensive_item = min(all_items, key=lambda x: x['price'])
            self.write("Least expensive item is %s" % least_expensive_item)
            return least_expensive_item
        
        except Exception as e:
            self.write("Exception while trying to get least expensive item")
            self.write(str(e))

    def get_most_expensive_item(self, all_items):
        "This method is to get the most expensive item from the given list of items"

        try:
            most_expensive_item = max(all_items, key=lambda x: x['price'])
            self.write("Most expensive item is %s" % most_expensive_item)
            return most_expensive_item

        except Exception as e:
            self.write("Exception while trying to get most expensive item")
            self.write(str(e))
    
    def add_to_cart(self,least_expensive_item, most_expensive_item):
        "This method is to click on Add to cart button in the Weather Shopper application."
        try:
            self.swipe_to_element(locators.recycler_view, locators.add_to_cart.format(least_expensive_item['name']), direction="down")
            result_flag = self.click_element(locators.add_to_cart.format(least_expensive_item['name']))
            self.scroll_to_top()
            self.swipe_to_element(locators.recycler_view, locators.add_to_cart.format(most_expensive_item['name']), direction="up")
            result_flag = self.click_element(locators.add_to_cart.format(most_expensive_item['name']))
            return result_flag
        
        except Exception as e:
            self.write("Exception while trying to click on Add to cart button")
            self.write(str(e))

    def view_cart(self):
        "This method is to click on Cart button in the Weather Shopper application."

        try:
            cart = locators.cart
            result_flag = self.click_element(cart)
            return result_flag
        except Exception as e:
            self.write("Exception while trying view Cart")
            self.write(str(e))

    def get_cart_total(self):
        "This method is to get the total price in the cart."
        try:
            cart_total = self.get_text(locators.total_amount)
            # Extracting the numeric part using regular expression
            match = re.search(r'\d+\.\d+', cart_total.decode())
            total_amount = float(match.group()) if match else None

            print("Total amount is ",total_amount)
            return total_amount
        
        except Exception as e:
            self.write("Exception while trying to get cart total")
            self.write(str(e))

    def verify_total(self, cart_total, cart_item_1, cart_item_2=0):
        "This method is to verify the total price in the cart."
        try:
            if cart_total == cart_item_1 + cart_item_2:
                return True
            else:
                return False
        
        except Exception as e:
            self.write("Exception while trying to verify total")
            self.write(str(e))

    def change_quantity(self, item_to_change, quantity=2):
        "This method is to change the quantity of an item in the cart"
        try:
            result_flag = self.set_text(locators.edit_quantity.format(item_to_change), quantity)
            return result_flag
        
        except Exception as e:
            self.write("Exception while trying to change quantity")
            self.write(str(e))

    def refresh_total_amount(self):
        "This method is to refresh the total amount in the cart."
        try:
            result_flag = self.click_element(locators.refresh_button)
            return result_flag
        
        except Exception as e:
            self.write("Exception while trying to refresh total amount")
            self.write(str(e))

    def delete_from_cart(self, item_to_delete):
        "This method is to delete an item from the cart"

        try:
            result_flag = self.click_element(locators.checkbox.format(item_to_delete))
            result_flag &= self.click_element(locators.delete_from_cart_button)
            return result_flag
        
        except Exception as e:
            self.write("Exception while trying to delete from cart")
            self.write(str(e))

    def checkout(self):
        "This method is to go to the Checkout page"

        try:
            result_flag = self.click_element(locators.checkout_button)
            return result_flag
        
        except Exception as e:
            self.write("Exception while trying to checkout")
            self.write(str(e))

    def enter_valid_payment_details(self, payment_details):
        "This method is to enter valid payment details"
        try:
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

        except Exception as e:
            self.write("Exception while trying to enter valid payment details")
            self.write(str(e))


    















