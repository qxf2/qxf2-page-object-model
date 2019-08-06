"""
PageFactory uses the factory design pattern. 
get_page_object() returns the appropriate page object.
Add elif clauses as and when you implement new pages.
"""

#import the pages 
from page_objects.<name_of_page> import <name_of_page>

class PageFactory():
    "PageFactory uses the factory design pattern."
    def get_page_object(page_name,base_url='',trailing_slash_flag=True):
        "Return the appropriate page object based on page_name"
        test_obj = None
        page_name = page_name.lower()
        if page_name == "main page":
            test_obj = <name_of_page>(base_url=base_url,trailing_slash_flag=trailing_slash_flag)
        return test_obj

    get_page_object = staticmethod(get_page_object)