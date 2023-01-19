"""
This class models the add article page.
"""
from .Base_Page import Base_Page
import conf.locators_conf as locators
import random
import string


class Add_Article(Base_Page):
    "Page Object for the newsletter's main page"

    #locators for add article page
    ADD_ARTICLE_URL = locators.URL
    ADD_ARTICLE_TITLE = locators.TITLE
    ADD_ARTICLE_DESCRIPTION = locators.DESCRIPTION
    ADD_ARTICLE_TIME = locators.TIME
    ADD_ARTICLE_SELECT_CATEGORY = locators.SELECT_CATEGORY
    ADD_ARTICLE_BUTTON = locators.ADD_ARTICLE_BUTTON
    AAD_ARTICLE_ADDED_RECORD = locators.ADDED_RECORD

    def add_article(self):

        rand_text = "".join( [random.choice(string.ascii_letters) for i in range(15)] )
        text_val = "http://qxf2.com/"+rand_text

        result_add_article = self.set_text(self.ADD_ARTICLE_URL,text_val)
        

        if result_add_article is not None:
            self.write("The url field is found and entered text is: %s"%result_add_article,level="debug")
        else:
            self.write("Unable to find the url field",level="")
        
        return result_add_article 

    def add_title(self,title):

        result_title = self.set_text(self.ADD_ARTICLE_TITLE,title)   

        if result_title is not None:
            self.write("The title field is found: %s"%result_title,level="debug")
        else:
            self.write("Unable to find the title field",level="")
        
        return result_title

    def add_description(self,description):

        result_description = self.set_text(self.ADD_ARTICLE_DESCRIPTION,description)   

        if result_description is not None:
            self.write("The description field is found: %s"%result_description,level="debug")
        else:
            self.write("Unable to find the description field",level="")
        
        return result_description

    def add_time(self):

        rand_digit = random.randint(1,119)
        result_digit = self.set_text(self.ADD_ARTICLE_TIME,rand_digit)   

        if result_digit is not None:
            self.scroll_down(self.ADD_ARTICLE_SELECT_CATEGORY,wait_time=10)
            self.write("The time field is found: %s"%result_digit,level="debug")
        else:
            self.write("Unable to find the time field",level="")
        
        return result_digit

    def click_category(self,article_category):

        result_click_category = self.click_element(self.ADD_ARTICLE_SELECT_CATEGORY%article_category) 

        if result_click_category is True:
            self.write("The category is clicked")        
        else:
            self.write("The category is not clicked")

        return result_click_category

    def click_add_article_button(self):

        result_add_button = self.click_element(self.ADD_ARTICLE_BUTTON)
        result_added_record = self.get_text(self.AAD_ARTICLE_ADDED_RECORD)
        if result_added_record is not None:
            self.write("The add button is clicked and the %s is displayed"%result_added_record)
        else:
            self.write("The add button is not clicked and the %s is not displayed"%result_added_record)

        return result_add_button



