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

from page_objects.zero_mobile_page import Zero_Mobile_Page
from page_objects.zero_page import Zero_Page
from page_objects.tutorial_main_page import Tutorial_Main_Page
from page_objects.tutorial_redirect_page import Tutorial_Redirect_Page
from page_objects.contact_page import Contact_Page
from page_objects.bitcoin_price_page import Bitcoin_Price_Page
from page_objects.bitcoin_main_page import Bitcoin_Main_Page
import conf.base_url_conf


class PageFactory():
    "PageFactory uses the factory design pattern."
    def get_page_object(page_name,base_url=conf.base_url_conf.base_url):
        "Return the appropriate page object based on page_name"
        test_obj = None
        page_name = page_name.lower()
        if page_name in ["zero","zero page","agent zero"]:
            test_obj = Zero_Page(base_url=base_url)
        elif page_name in ["zero mobile","zero mobile page"]:
            test_obj = Zero_Mobile_Page()
        elif page_name == "main page":
            test_obj = Tutorial_Main_Page(base_url=base_url)
        elif page_name == "redirect":
            test_obj = Tutorial_Redirect_Page(base_url=base_url)
        elif page_name == "contact page":
            test_obj = Contact_Page(base_url=base_url)
        elif page_name == "bitcoin main page":
            test_obj = Bitcoin_Main_Page()
        elif page_name == "bitcoin price page":
            test_obj = Bitcoin_Price_Page()
        return test_obj

    get_page_object = staticmethod(get_page_object)