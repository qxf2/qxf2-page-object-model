"""
This class models the page objects for the products in Weathershopper application.
"""
import conf.locators_conf as locators
from utils import Wrapit

class ProductPageObjects:
    "Page objects for the products in Weathershopper application."
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
    def get_all_products(self):
        "This method is to get all items from product page."
        all_products = []
        max_scrolls = 50
        for attempt in range(max_scrolls):
            # Get product names and prices
            product_names = self.get_elements(locators.product_name)
            product_prices = self.get_elements(locators.product_price)

            # Store the product names and prices in a list
            all_products = self.store_products_in_list(all_products, product_names, product_prices)

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

    def store_products_in_list(self, all_products, product_names, product_prices):
        "This method is to store the products in view to a list."
        for name, price in zip(product_names, product_prices):
            product_name = self.get_text(name, dom_element_flag=True)
            product_price = self.get_text(price, dom_element_flag=True)

            # Append the product name and price to the list if it is not already in the list
            if {"name": product_name.decode(),
                "price": float(product_price)} not in all_products:
                all_products.append({"name": product_name.decode(),
                "price": float(product_price)})
        return all_products

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
