"""
This class models the main newsletter generator page.
"""
from .Base_Page import Base_Page
import conf.locators_conf as locators
import random
import string


class Main_Page(Base_Page):
    "Page Object for the newsletter's main page"

    opener = "From the simplest to the most complex application, automation is present in many forms in our everyday life. Common examples include household thermostats controlling boilers, the earliest automatic telephone switchboards, electronic navigation systems, or the most advanced algorithms behind self-driving cars."

    #locators
    PAGE_TITLE = locators.PAGE_TITLE
    HAMBURGER_MENU = locators.HAMBURGER
    ADD_ARTICLE = locators.ADD_ARTICLE


    def start(self):
        "Use this method to go to specific URL -- if needed"
        url = '/'
        self.open(url)

    def verify_page_title(self):

        result_title = self.get_text(self.PAGE_TITLE).decode('utf-8')

        if result_title is not None:
            self.write("The title found is: %s"%result_title,level="debug")
        else:
            self.write("Unable to find the title",level="")
        
        return result_title

    def hover_menu(self):

        result_menu = self.hover(self.HAMBURGER_MENU)

    def click_menu_content(self,options):

        if options in ['Add Article', 'Create Newsletter']:
            result_add_menu_content = self.click_element(self.ADD_ARTICLE%options)
            self.conditional_write(result_add_menu_content,
            positive="Clicked the %s"%options,
            negative="Could not click %s"%options)

        return result_add_menu_content











               

        



    

    


