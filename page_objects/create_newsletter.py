"""
This class models the create newsletter page.
"""
from .Base_Page import Base_Page
import conf.locators_conf as locators
import random
import string


class Create_Newsletter(Base_Page):
    "Page Object for the newsletter's main page"

    #locators for create newsletter page
    CREATE_NEWSLETTER_URL = locators.CATEGORY_URL
    CREATE_NEWSLETTER_ADD_MORE_ARTICLE = locators.ADD_MORE_ARTICLE
    CREATE_NEWSLETTER_CLEAR_FIELDS = locators.CLEAR_FIELDS
    CREATE_NEWSLETTER_ADDED_ARTICLE = locators.ADDED_ARTICLE
    CREATE_NEWSLETTER_SELECT_URL = locators.SELECT_URL
    CREATE_NEWSLETTER_SUBJECT = locators.SUBJECT
    CREATE_NEWSLETTER_OPENER = locators.OPENER
    CREATE_NEWSLETTER_PREVIEW_TEXT = locators.PREVIEW_TEXT
    CREATE_NEWSLETTER_PREVIEW_NEWSLETTER = locators.PREVIEW_NEWSLETTER
    CREATE_NEWSLETTER_PREVIEW_CONTENT = locators.PREVIEW_CONTENT
    CREATE_NEWSLETTER_CREATE_CAMPAIGN = locators.CREATE_CAMPAIGN

    def create_newsletter(self,article_category,subject,opener,preview,url_option):

        result_click_category = self.click_element(self.ADD_ARTICLE_SELECT_CATEGORY%article_category)

        if result_click_category is True:
            self.write("The category %s is selected"%article_category)
        else:
            self.write("The category %s is not selected"%article_category)

        result_click_url = self.click_element(self.CREATE_NEWSLETTER_URL)

        result_select_url = self.click_element(self.CREATE_NEWSLETTER_SELECT_URL%url_option)

        if result_select_url is not None:
            self.write("The URL %s is present"%url_option)
        else:
            self.write("The URL %s is not present"%url_option)

        result_add_more_article = self.click_element(self.CREATE_NEWSLETTER_ADD_MORE_ARTICLE)
        
        self.scroll_down(self.CREATE_NEWSLETTER_CLEAR_FIELDS)

        check_added_article = self.get_text(self.CREATE_NEWSLETTER_ADDED_ARTICLE%url_option)

        if check_added_article is not None:
            self.write("The URL %s is added"%url_option)
        else:
            self.write("The URL %s is not added"%url_option)   

        result_add_subject = self.set_text(self.CREATE_NEWSLETTER_SUBJECT,subject)
        result_add_opener = self.set_text(self.CREATE_NEWSLETTER_OPENER,opener)
        result_add_preview = self.set_text(self.CREATE_NEWSLETTER_PREVIEW_TEXT,preview)

        result_preview_newsletter = self.click_element(self.CREATE_NEWSLETTER_PREVIEW_NEWSLETTER)

        return result_preview_newsletter

    def check_preview_content(self,opener):

        check_preview_newsletter_content_opener = self.get_text(self.CREATE_NEWSLETTER_PREVIEW_CONTENT%opener)

        if check_preview_newsletter_content_opener is not None:
            self.write("The preview newsletter content is visible with opener as: %s"%opener)
        else:
            self.write("The preview newsletter content is not visible")
        
        self.scroll_down(self.CREATE_NEWSLETTER_CREATE_CAMPAIGN)

        return check_preview_newsletter_content_opener

    def create_campaign(self):

        result_create_campaign = self.click_element(self.CREATE_NEWSLETTER_CREATE_CAMPAIGN)

        if result_create_campaign is True:
            self.write("The create campaign is clicked")
        else:
            self.write("create campaign is not clicked")            

        return result_create_campaign



