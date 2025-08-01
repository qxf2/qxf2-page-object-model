"""
This class models the home page in windows word application.
"""
# pylint: disable = W0212,E0401
from core_helpers.mobile_app_helper import Mobile_App_Helper
import conf.locators_conf as locators
from utils.Wrapit import Wrapit

class WordHomePage(Mobile_App_Helper):
    "Page objects for home page in windows word application."

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def enter_text_on_page(self, text):
        "Enter the text in word"
        result_flag = self.set_text(locators.word_textarea, text,clear_flag=True)
        self.conditional_write(result_flag,
            positive=f'Successfully set the text: {text}',
            negative=f'Failed to set the text: {text}',
            level='debug')
        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_on_blank_document(self):
        "Click on blank doc option"
        result_flag = self.click_element(locators.blank_document)
        self.conditional_write(result_flag,
            positive=f'Successfully clicked on blank doc option',
            negative=f'Failed to click on blank doc option',
            level='debug')
        return result_flag
    

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_on_insert_menu_tab(self):
        "Click on insert menu option"
        result_flag = self.click_element(locators.insert_tab)
        self.conditional_write(result_flag,
            positive=f'Successfully clicked on insert menu option',
            negative=f'Failed to click on insert menu option',
            level='debug')
        return result_flag
    

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_on_icons_button(self):
        "Click on icons button"
        result_flag = self.click_element(locators.icon_button)
        self.conditional_write(result_flag,
            positive=f'Successfully clicked on icons button',
            negative=f'Failed to click on icons button',
            level='debug')
        return result_flag
    

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def verify_stock_images_popup_windows(self):
        "Click on icons button"
        self.smart_wait(locators.stock_image_popup_window)
        result_flag = self.check_element_displayed(locators.stock_image_popup_window)
        self.conditional_write(result_flag,
            positive=f'Stock image popup window visible',
            negative=f'Stock image windows not visible',
            level='debug')
        return result_flag
    

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def select_angle_face_icon(self):
        "Select angle face icon"
        result_flag = self.click_element(locators.icon_angel_face)
        self.conditional_write(result_flag,
            positive=f'Successfully selected angle face icon',
            negative=f'Failed to select angle face icon',
            level='debug')
        return result_flag
    

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_on_insert_icons_button(self):
        "Click on insert icons button"
        result_flag = self.click_element(locators.insert_icons_button)
        self.conditional_write(result_flag,
            positive=f'Successfully clicked on insert icons button',
            negative=f'Failed to click on insert icons button',
            level='debug')
        return result_flag
    

    def insert_icon(self):
        "insert icon"
        result_flag = self.click_on_insert_menu_tab()
        result_flag &= self.click_on_icons_button()
        #self.wait(3)
        result_flag &= self.verify_stock_images_popup_windows()
        result_flag &= self.select_angle_face_icon()
        result_flag &= self.click_on_insert_icons_button()

        return result_flag
