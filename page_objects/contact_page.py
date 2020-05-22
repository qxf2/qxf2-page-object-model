"""
This class models the Contact page.
URL: contact
The page consists of a header, footer and form object.
"""
from .Base_Page import Base_Page
from .contact_form_object import Contact_Form_Object
from .header_object import Header_Object
from .footer_object import Footer_Object
from utils.Wrapit import Wrapit

class Contact_Page(Base_Page,Contact_Form_Object,Header_Object,Footer_Object):
    "Page Object for the contact page"

    def start(self):
        "Use this method to go to specific URL -- if needed"
        url = 'contact'
        self.open(url)
