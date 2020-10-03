import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from page_objects.PageFactory import PageFactory

def before_all(context):
    "Let there be light!"
    context.test_obj = PageFactory.get_page_object("main page")


