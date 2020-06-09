"""
This class models the hamburger menu object as a Page Object
The hamburger menu has a bunch of options that can be:
a) Clicked
b) Hovered over
"""
import conf.locators_conf as locators
from utils.Wrapit import Wrapit


class Hamburger_Menu_Object:
    "Page Object for the hamburger menu"

    #locators
    menu_icon = locators.menu_icon
    menu_link = locators.menu_link
    menu_item = locators.menu_item

    @Wrapit._exceptionHandler
    def goto_menu_link(self,my_link,expected_url_string=None):
        "Navigate to a link: Hover + Click or just Click"
        #Format for link: string separated by '>'
        #E.g.: 'Approach > Where we start'
        split_link = my_link.split('>')
        hover_list = split_link[:-1]
        self.click_hamburger_menu()
        for element in hover_list:
            self.hover(self.menu_item%element.strip())
        result_flag = self.click_element(self.menu_link%split_link[-1].strip())

        #Additional check to see if we went to the right page
        if expected_url_string is not None:
            result_flag &= True if expected_url_string in self.get_current_url() else False

        #If the action failed, close the Hamburger menu
        if result_flag is False:
            self.click_hamburger_menu()

        return result_flag


    def click_hamburger_menu(self):
        "Click on the hamburger menu icon"
        return self.click_element(self.menu_icon)
