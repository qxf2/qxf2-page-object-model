"""
This class models the main page of the web application
"""
from .Base_Page import Base_Page
from utils.Wrapit import Wrapit
#import page objects created for other pages

#Update the class name and name of the file according to your test scenario
class <name_of_main_page>(Base_Page,<other_page_objects>):
    "Page Object for the main page"
    
    def start(self):
        "Use this method to go to specific URL -- if needed"
        url = ''
        self.open(url)
