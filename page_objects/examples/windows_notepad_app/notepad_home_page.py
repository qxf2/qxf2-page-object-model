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
    def clear_text_if_any(self):
        "Send Ctrl + A and Delete to clean all text if any"
        result_flag = self.send_keys_to_element(locators.notepad_textarea, ('CONTROL', 'a'))
        result_flag = self.send_keys_to_element(locators.notepad_textarea, ('DELETE'))

        self.conditional_write(result_flag,
            positive='Send keys to clear text',
            negative='Failed to send keys',
            level='debug')

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def verify_text_cleared(self):
        "Verify the text cleared"
        text = self.get_text(locators.notepad_textarea)
        if text == b'':
            result_flag = True
        else:
            result_flag = False

        self.conditional_write(result_flag,
            positive='Verified text cleaned successfully',
            negative='Failed to clean text',
            level='debug')

        return result_flag

    def clear_text_and_verify(self):
        "Clear text and verify it"
        result_flag = self.clear_text_if_any()
        result_flag &= self.verify_text_cleared()

        return result_flag

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
    def verify_text_added(self, expected_text):
        "Enter the text in notepad"
        import unicodedata
        result_flag = False
        raw_text = self.get_text(locators.notepad_textarea)
        # Decode bytes safely
        if isinstance(raw_text, bytes):
            decoded_text = raw_text.decode("utf-8", errors="ignore")
        else:
            decoded_text = str(raw_text)

        # Normalize unicode (fix curly quotes, accented characters, etc.)
        normalized_text = unicodedata.normalize("NFKC", decoded_text)

        # Check substring
        if expected_text in normalized_text:
            result_flag = True

        self.conditional_write(result_flag,
            positive=f'verified text set correctly to: {expected_text} ',
            negative=f'Verify text: {expected_text} not set correctly',
            level='debug')

        return result_flag

    def enter_text_and_verify(self,text):
        "Enter text and verify it"
        result_flag = self.enter_text(text)
        result_flag &= self.verify_text_added(text)

        return result_flag

    @Wrapit._exceptionHandler
    @Wrapit._screenshot
    def click_on_file_menu(self):
        "Click on File menu option"
        result_flag = self.click_element(locators.file_menu)
        self.conditional_write(result_flag,
            positive='Successfully clicked on file menu',
            negative='Failed to click on file menu',
            level='debug')

        return result_flag
