"""
PageFactory uses the factory design pattern.
get_page_object() returns the appropriate page object.
Add elif clauses as and when you implement new pages.
Pages implemented so far:
1. Tutorial main page
2. Tutorial redirect page
3. Contact Page
4. Bitcoin main page
5. Bitcoin price page
"""
# pylint: disable=import-outside-toplevel, E0401
from conf import base_url_conf as url_conf

class PageFactory():
    "PageFactory uses the factory design pattern."
    @staticmethod
    def get_page_object(page_name,base_url=url_conf.ui_base_url):
        "Return the appropriate page object based on page_name"
        test_obj = None
        page_name = page_name.lower()
        if page_name in ["zero","zero page","agent zero"]:
            from page_objects.zero_page import Zero_Page
            test_obj = Zero_Page(base_url=base_url)
        elif page_name in ["zero mobile","zero mobile page"]:
            from page_objects.zero_mobile_page import Zero_Mobile_Page
            test_obj = Zero_Mobile_Page()
        elif page_name == "main page":
            from page_objects.examples.selenium_tutorial_webpage.tutorial_main_page import Tutorial_Main_Page
            test_obj = Tutorial_Main_Page(base_url=base_url)
        elif page_name == "redirect":
            from page_objects.examples.selenium_tutorial_webpage.tutorial_redirect_page import Tutorial_Redirect_Page
            test_obj = Tutorial_Redirect_Page(base_url=base_url)
        elif page_name == "contact page":
            from page_objects.examples.selenium_tutorial_webpage.contact_page import Contact_Page
            test_obj = Contact_Page(base_url=base_url)
        elif page_name == "bitcoin main page":
            from page_objects.examples.bitcoin_mobile_app.bitcoin_main_page import Bitcoin_Main_Page
            test_obj = Bitcoin_Main_Page()
        elif page_name == "bitcoin price page":
            from page_objects.examples.bitcoin_mobile_app.bitcoin_price_page import Bitcoin_Price_Page
            test_obj = Bitcoin_Price_Page()
            #"New pages added needs to be updated in the get_all_page_names method too"
        elif page_name == "weathershopper home page":
            from page_objects.examples.weather_shopper_mobile_app.weather_shopper_home_page import WeatherShopperHomePage
            test_obj = WeatherShopperHomePage()
        elif page_name == "weathershopper products page":
            from page_objects.examples.weather_shopper_mobile_app.weather_shopper_product_page import WeatherShopperProductPage
            test_obj = WeatherShopperProductPage()
        elif page_name == "weathershopper payment page":
            from page_objects.examples.weather_shopper_mobile_app.weather_shopper_payment_page import WeatherShopperPaymentPage
            test_obj = WeatherShopperPaymentPage()
        elif page_name == "weathershopper cart page":
            from page_objects.examples.weather_shopper_mobile_app.weather_shopper_cart_page import WeatherShopperCartPage
            test_obj = WeatherShopperCartPage()
        elif page_name == "webview":
            from page_objects.examples.weather_shopper_mobile_app.webview_chrome import WebviewChrome
            test_obj = WebviewChrome()
        return test_obj


    @staticmethod
    def get_all_page_names():
        "Return the page names"
        return ["main page",
                "redirect",
                "contact page"]
