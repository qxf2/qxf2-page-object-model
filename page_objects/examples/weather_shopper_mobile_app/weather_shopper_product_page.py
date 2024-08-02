"""
Page objects for the product page in Weathershopper application.
"""
# pylint: disable = W0212,E0401
import conf.locators_conf as locators
from utils.Wrapit import Wrapit
from core_helpers.mobile_app_helper import Mobile_App_Helper

class WeatherShopperProductPage(Mobile_App_Helper):
    "Page objects for product page in Weathershopper application."

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
        self.switch_page("weathershopper cart page")
        return result_flag
