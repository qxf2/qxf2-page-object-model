"""
This class models the home page in notepad application.
"""
# pylint: disable = W0212,E0401
from core_helpers.mobile_app_helper import Mobile_App_Helper
import conf.locators_conf as locators
from utils.Wrapit import Wrapit

class NotepadHomePage(Mobile_App_Helper):
    "Page objects for home page in Weathershopper application."

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def enter_text(self, text):
        "Enter the text in notepad"
        result_flag = self.set_text(locators.notepad_textarea, text)
        self.conditional_write(result_flag,
            positive=f'Successfully set the text: {text}',
            negative=f'Failed to set the text: {text}',
            level='debug')
        return result_flag
    

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_on_file_menu(self):
        "Click on File menu option"
        result_flag = self.click_element(locators.file_menu)
        self.conditional_write(result_flag,
            positive=f'Successfully clicked on file menu',
            negative=f'Failed to click on file menu',
            level='debug')
        return result_flag
