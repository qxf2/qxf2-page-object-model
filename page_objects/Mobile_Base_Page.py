"""
Page class that all page models can inherit from
There are useful wrappers for common Selenium operations
"""
import unittest,os,inspect
from .driverfactory import DriverFactory
from .core_helpers.selenium_action_objects import Selenium_Action_Objects
from .core_helpers.logging_objects import Logging_Objects
from .core_helpers.remote_objects import Remote_Objects
from .core_helpers.screenshot_objects import Screenshot_Objects
from page_objects import PageFactory
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton

class Borg:
    #The borg design pattern is to share state
    #Src: http://code.activestate.com/recipes/66531/
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state


    def is_first_time(self):
        "Has the child class been invoked before?"
        result_flag = False
        if len(self.__dict__)==0:
            result_flag = True

        return result_flag


class Mobile_Base_Page(Borg,unittest.TestCase, Selenium_Action_Objects, Logging_Objects, Remote_Objects, Screenshot_Objects):
    "Page class that all page models can inherit from"

    def __init__(self):
        "Constructor"
        Borg.__init__(self)
        if self.is_first_time():
            #Do these actions if this the first time this class is initialized
            self.set_directory_structure()
            self.image_url_list = []
            self.msg_list = []
            self.window_structure = {}
            self.testrail_flag = False
            self.browserstack_flag = False
            self.test_run_id = None
            self.tesults_flag = False
            self.highlight_flag = False
            self.reset()

        self.driver_obj = DriverFactory()
        if self.driver is not None:
            self.start() #Visit and initialize xpaths for the appropriate page


    def reset(self):
        "Reset the base page object"
        self.driver = None
        self.result_counter = 0 #Increment whenever success or failure are called
        self.pass_counter = 0 #Increment everytime success is called
        self.mini_check_counter = 0 #Increment when conditional_write is called
        self.mini_check_pass_counter = 0 #Increment when conditional_write is called with True
        self.failure_message_list = []
        self.rp_logger = None
        self.exceptions = []
        self.screenshot_counter = 1
        self.calling_module = None


    def switch_page(self,page_name):
        "Switch the underlying class to the required Page"
        self.__class__ = PageFactory.PageFactory.get_page_object(page_name).__class__


    def register_driver(self,mobile_os_name,mobile_os_version,device_name,app_package,app_activity,remote_flag,device_flag,app_name,app_path,ud_id,org_id,signing_id,no_reset_flag,appium_version,remote_project_name,remote_build_name,orientation):
        "Register the mobile driver"
        self.driver = self.driver_obj.run_mobile(mobile_os_name,mobile_os_version,device_name,app_package,app_activity,remote_flag,device_flag,app_name,app_path,ud_id,org_id,signing_id,no_reset_flag,appium_version,remote_project_name,remote_build_name,orientation)
        self.set_screenshot_dir() # Create screenshot directory
        self.set_log_file()
        self.start()


    def get_driver_title(self):
        "Return the title of the current page"
        return self.driver.title


    def get_calling_module(self):
        "Get the name of the calling module"
        calling_file = inspect.stack()[-1][1]
        if 'runpy' in calling_file:
            calling_file = inspect.stack()[5][3]

        calling_filename = calling_file.split(os.sep)

        #This logic bought to you by windows + cygwin + git bash
        if len(calling_filename) == 1: #Needed for
            calling_filename = calling_file.split('/')
        self.calling_module = calling_filename[-1].split('.')[0]
        return self.calling_module


    def set_screenshot_dir(self):
        "Set the screenshot directory"
        self.screenshot_dir = self.get_screenshot_dir()
        self.create_dir_screenshot = self.create_screenshot_dir(self.screenshot_dir)


    def get_screenshot_dir(self):
        "Get the name of the test"
        self.testname = self.get_test_name()
        self.screenshot_dir = self.screenshot_directory(self.testname)
        return self.screenshot_dir


    def open(self,wait_time=2):
        "Visit the page base_url + url"
        self.wait(wait_time)


    def conditional_write(self,flag,positive,negative,level='debug',pre_format="  - "):
        "Write out either the positive or the negative message based on flag"
        if flag is True:
            self.write(pre_format + positive,level)
            self.mini_check_pass_counter += 1
        if flag is False:
            self.write(pre_format + negative,level)
        self.mini_check_counter += 1

    def swipe_to_element(self,scroll_group_locator, search_element_locator, max_swipes=20, direction="up"):
        result_flag = False
        try:
           #Get the scroll group
           scroll_group = self.get_element(scroll_group_locator)

           #Get the initial element location
           scroll_group_location = scroll_group.location

           #Get the initial element size
           scroll_group_size = scroll_group.size

           #Get the center of the initial element
           center_x = scroll_group_location['x'] + scroll_group_size['width'] / 2
           center_y = scroll_group_location['y'] + scroll_group_size['height'] / 2

           # 40% from the top of the element
           start_x = scroll_group_location['x'] + scroll_group_size['width'] * 0.4
           start_y = scroll_group_location['y'] + scroll_group_size['height'] * 0.4

           # 20% from the top of the element
           end_x = scroll_group_location['x'] + scroll_group_size['width'] * 0.2  
           end_y = scroll_group_location['y'] + scroll_group_size['height'] * 0.2

           #Get the search element locator
           path = self.split_locator(search_element_locator)

           #Perform swipes in a loop until the searchelement is found
           for _ in range(max_swipes):
                #Return when search element is located
                try:
                    element = self.driver.find_element(*path)
                    if element.is_displayed():
                        result_flag = True
                        return result_flag
                except:
                    pass

                # Perform swipe based on direction
                if direction == "up":
                    self.driver.swipe(start_x=center_x, start_y=start_y, end_x=center_x, end_y=end_y, duration=200)
                elif direction == "down":
                    self.driver.swipe(start_x=center_x, start_y=end_y, end_x=center_x, end_y=start_y, duration=200)
                elif direction == "left":
                    self.driver.swipe(start_x=start_x, start_y=center_y, end_x=end_x, end_y=center_y, duration=200)
                elif direction == "right":
                    self.driver.swipe(start_x=end_x, start_y=center_y, end_x=start_x, end_y=center_y, duration=200)

           self.conditional_write(result_flag,
                            positive='Located the element: %s' % search_element_locator,
                            negative='Could not locate the element %s after swiping.' % search_element_locator)

           return result_flag

        except Exception as e:
            self.write(str(e), 'debug')
            self.exceptions.append("Error while swiping to element - '%s' " % search_element_locator)

    def zoom_in(self, element_locator):
        """
        Perform zoom in gesture.
        """
        try:
            #Get the element to be zoomed
            zoom_element = self.get_element(element_locator)

            #Get the zoom element location
            zoom_element_location = zoom_element.location
            zoom_x = zoom_element_location['x']
            zoom_y = zoom_element_location['y']

            #Get the zoom element size and center
            zoom_element_size = zoom_element.size
            center_x = zoom_x + zoom_element_size['width'] / 2
            center_y = zoom_y + zoom_element_size['height'] / 2

            #Perform zoom
            actions = ActionChains(self.driver)
            finger1 = actions.w3c_actions.add_pointer_input('touch', 'finger1')
            finger2 = actions.w3c_actions.add_pointer_input('touch', 'finger2')

            finger1.create_pointer_move(x=center_x - 100, y=center_y)
            finger1.create_pointer_down(button=MouseButton.LEFT)
            finger1.create_pause(0.5)
            finger1.create_pointer_move(x=center_x - 500, y=center_y, duration=50)
            finger1.create_pointer_up(button=MouseButton.LEFT)

            finger2.create_pointer_move(x=center_x + 100, y=center_y)
            finger2.create_pointer_down(button=MouseButton.LEFT)
            finger2.create_pause(0.5)
            finger2.create_pointer_move(x=center_x + 500, y=center_y, duration=50)
            finger2.create_pointer_up(button=MouseButton.LEFT)

            actions.perform()

            size_after_zoom = zoom_element.size
            if size_after_zoom != zoom_element_size:
                return True
            else:
                return False

        except Exception as e:
            self.write(str(e), 'debug')
            self.exceptions.append("An exception occured when zooming in")

    def zoom_out(self, zoom_element_locator):
        """
        Perform zoom out gesture.
        """
        try:
            #Get the element to be zoomed
            zoom_element = self.get_element(zoom_element_locator)

            #Get the zoom element location
            zoom_element_location = zoom_element.location
            zoom_x = zoom_element_location['x']
            zoom_y = zoom_element_location['y']

            #Get the zoom element size and center
            zoom_element_size = zoom_element.size
            center_x = zoom_x + zoom_element_size['width'] / 2
            center_y = zoom_y + zoom_element_size['height'] / 2

            #Perform zoom
            actions = ActionChains(self.driver)
            finger1 = actions.w3c_actions.add_pointer_input('touch', 'finger1')
            finger2 = actions.w3c_actions.add_pointer_input('touch', 'finger2')

            finger1.create_pointer_move(x=center_x-400, y=center_y)
            finger1.create_pointer_down(button=MouseButton.LEFT)
            finger1.create_pause(0.5)
            finger1.create_pointer_move(x=center_x-100, y=center_y, duration=500)
            finger1.create_pointer_up(button=MouseButton.LEFT)

            finger2.create_pointer_move(x=center_x+400, y=center_y)
            finger2.create_pointer_down(button=MouseButton.LEFT)
            finger2.create_pause(0.5)
            finger2.create_pointer_move(x=center_x+100, y=center_y, duration=500)
            finger2.create_pointer_up(button=MouseButton.LEFT)

            actions.perform()

            size_after_zoom = zoom_element.size
            if size_after_zoom != zoom_element_size:
                return True
            else:
                return False

        except Exception as e:
            self.write(str(e), 'debug')
            self.exceptions.append("An exception occured when zooming out")

    def long_press(self, element, duration=5):
        """
        Perform a long press gesture on the specified element.
        """
        ressult_flag = False
        try:
            # Convert element locator to WebDriver element
            web_element = self.get_element(element)
            # Perform long press gesture
            action = ActionChains(self.driver)
            action.click_and_hold(web_element).pause(duration).release().perform()
            ressult_flag = True

        except Exception as e:
            # Log error if any exception occurs
            self.write(str(e), 'debug')
            self.exceptions.append("Error while performing long press gesture.")      
        return ressult_flag

    def drag_and_drop(self, source_locator, destination_locator):
        """
        Perform drag and drop gesture.
        """
        try:
            source_element = self.get_element(source_locator)
            source_element_location = source_element.location

            source_x = source_element_location['x']
            source_y = source_element_location['y']

            source_element_size = source_element.size
            source_center_x = source_x + source_element_size['width'] / 2
            source_center_y = source_y + source_element_size['height'] / 2

            destination_element = self.get_element(destination_locator)
            destination_element_location = destination_element.location

            destination_x = destination_element_location['x']
            destination_y = destination_element_location['y']

            destination_element_size = destination_element.size
            destination_center_x = destination_x + destination_element_size['width'] / 2
            destination_center_y = destination_y + destination_element_size['height'] / 2

            actions = ActionChains(self.driver)
            finger1 = actions.w3c_actions.add_pointer_input('touch', 'finger1')

            finger1.create_pointer_move(x=source_center_x, y=source_center_y)
            finger1.create_pointer_down(button=MouseButton.LEFT)
            finger1.create_pause(1)
            finger1.create_pointer_move(x=destination_center_x, y=destination_center_y, duration=500)
            finger1.create_pointer_up(button=MouseButton.LEFT)

            actions.perform()

            element_post_drop = self.get_element(source_locator)
            element_post_drop_location = element_post_drop.location
            if element_post_drop_location != source_element_location:
                return True
            else:
                self.write("Element did not move after drag and drop", 'debug')
                return False
        except Exception as e:
            self.write(str(e), 'debug')
            self.exceptions.append("An exception occured when performing drag and drop")

    def switch_screen_orientation(self, orientation='LANDSCAPE'):
        """
        Switch screen orientation.
        """
        try:
            print("Driver orientation",self.driver.orientation)
            # Capture the current orientation before switching
            initial_orientation = self.driver.orientation

            if initial_orientation == orientation:
                self.write("Screen orientation is already " + orientation, 'debug')
                return False
            # Switch orientation
            self.driver.orientation = orientation

            # Capture the orientation after switching
            new_orientation = self.driver.orientation

            # Verify if orientation has changed
            if new_orientation != initial_orientation:
                return True
            else:
                return False
        except Exception as e:
            self.write(str(e), 'debug')
            self.exceptions.append("An exception occured when switching screen orientation")

    def scroll_to_bottom(self):
        """
        Scroll to the bottom of the page.
        """
        result_flag = False
        try:
            self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR,value='new UiScrollable(new UiSelector().scrollable(true).instance(0)).flingToEnd(10)')
            result_flag = True
        except Exception as e:
            self.write(str(e),'debug')
            self.exceptions.append("An exception occured when scrolling to bottom of page")
        return result_flag

    def scroll_to_top(self):
        """
        Scroll to the top of the page.
        """
        result_flag = False
        try:
            self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiScrollable(new UiSelector().scrollable(true).instance(0)).flingToBeginning(10)')
            result_flag = True
        except Exception as e:
            self.write(str(e),'debug')
            self.exceptions.append("An exception occured when scrolling to top of page")
        return result_flag

    def start(self):
        "Dummy method to be over-written by child classes"
        pass

    def scroll_backward(self):
        "Scroll backward"

        result_flag = False
        try:
            self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,value='new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollBackward(150)')
            result_flag = True
        except Exception as e:
            self.write(str(e),'debug')
            self.exceptions.append("An exception occured when scrolling backward")
        return result_flag

    def scroll_forward(self):
        "Scroll backward"

        result_flag = False
        try:
            self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,value='new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollForward()')
            result_flag = True
        except Exception as e:
            self.write(str(e),'debug')
            self.exceptions.append("An exception occured when scrolling forward")
        return result_flag

    def scroll_into_view(self, search_text):
        "Scroll backward"

        result_flag = False
        try:
            ui_automator_expression = f'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollTextIntoView("{search_text}")'
            self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, value=ui_automator_expression)
            result_flag = True
        except Exception as e:
            self.write(str(e),'debug')
            self.exceptions.append("An exception occured when scrolling forward")
        return result_flag
