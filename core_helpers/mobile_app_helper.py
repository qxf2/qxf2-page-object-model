"""
Page class that all page models can inherit from
There are useful wrappers for common Selenium operations
"""
import unittest,os,inspect
from core_helpers.drivers.driverfactory import DriverFactory
from .selenium_action_objects import Selenium_Action_Objects
from .logging_objects import Logging_Objects
from .remote_objects import Remote_Objects
from .screenshot_objects import Screenshot_Objects
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

class Mobile_App_Helper(Borg,unittest.TestCase, Selenium_Action_Objects, Logging_Objects, Remote_Objects, Screenshot_Objects):
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
        self.driver,self.session_url = self.driver_obj.get_mobile_driver(mobile_os_name,mobile_os_version,device_name,app_package,app_activity,remote_flag,device_flag,app_name,app_path,ud_id,org_id,signing_id,no_reset_flag,appium_version,remote_project_name,remote_build_name,orientation)
        self.set_screenshot_dir() # Create screenshot directory
        self.set_log_file()
        if self.session_url:
            self.write( "Cloud Session URL for test: " + self.calling_module + '\n' + str(self.session_url))
        self.start()

    def get_driver_title(self):
        "Return the title of the current page"
        return self.driver.title

    def get_calling_module(self):
        "Get the name of the calling module"
        return self.calling_module

    def set_calling_module(self,name):
        "Set the test name"
        self.calling_module = name

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
            self.write(pre_format + positive,level='success')
            self.mini_check_pass_counter += 1
        if flag is False:
            self.write(pre_format + negative,level='error')
        self.mini_check_counter += 1

    def swipe_to_element(self,scroll_group_locator, search_element_locator, max_swipes=20, direction="up"):
        result_flag = False
        try:
            #Get the scroll view group
            scroll_group = self.get_element(scroll_group_locator)

            #Get the swipe coordinates
            coordinates = self.swipe_coordinates(scroll_group)
            start_x, start_y, end_x, end_y, center_x, center_y = (coordinates[key] for key in ["start_x", "start_y",
                                                                "end_x", "end_y", "center_x", "center_y"])
            #Get the search element locator
            path = self.split_locator(search_element_locator)

            #Perform swipes in a loop until the searchelement is found
            for _ in range(max_swipes):
                    #Return when search element is located
                try:
                    element = self.driver.find_element(*path)
                    if element.is_displayed():
                        self.write('Element found', 'debug')
                        result_flag = True
                        return result_flag
                except Exception:
                    self.write('Element not found, swiping again', 'debug')
                    pass

                # Perform swipe based on direction
                self.perform_swipe(direction, start_x, start_y,
                    end_x, end_y, center_x, center_y, duration=200)

            self.conditional_write(
                result_flag,
                positive=f'Located the element: {search_element_locator}',
                negative=f'Could not locate the element {search_element_locator} after swiping.'
            )
            return result_flag

        except Exception as e:
            self.write(str(e), 'debug')
            self.exceptions.append(f'Error while swiping to element - {search_element_locator}')

    def swipe_coordinates(self, scroll_group):
        "Calculate the swipe coordinates from the element locator"

        try:
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

            coordinates = {"start_x": start_x, "start_y": start_y,
                            "end_x": end_x, "end_y": end_y, 
                            "center_x": center_x, "center_y": center_y}

            return coordinates

        except Exception as e:
            self.write(str(e), 'debug')
            self.exceptions.append("Error while calculating swipe coordinates")

    def perform_swipe(self, direction, start_x, start_y, end_x, end_y, center_x, center_y, duration):
        "Perform swipe based on the direction"
        try:
            if direction == "up":
                self.driver.swipe(start_x=center_x, start_y=start_y, end_x=center_x, end_y=end_y, duration=duration)
            elif direction == "down":
                self.driver.swipe(start_x=center_x, start_y=end_y, end_x=center_x, end_y=start_y, duration=duration)
            elif direction == "left":
                self.driver.swipe(start_x=start_x, start_y=center_y, end_x=end_x, end_y=center_y, duration=duration)
            elif direction == "right":
                self.driver.swipe(start_x=end_x, start_y=center_y, end_x=start_x, end_y=center_y, duration=duration)

        except Exception as e:
            self.write(str(e), 'debug')
            self.exceptions.append("Error while performing swipe")

    def zoom(self, element_locator, zoom_direction="in"):
        """
        Perform zoom gesture.
        """
        try:
            #Get the element to be zoomed
            zoom_element = self.get_element(element_locator)

            #Get the center of the element
            coordinates = self.get_element_center(zoom_element)
            center_x = coordinates['center_x']
            center_y = coordinates['center_y']
            zoom_element_size = zoom_element.size

            #Perform zoom
            self.perform_zoom(zoom_direction, center_x, center_y)

            size_after_zoom = zoom_element.size
            if size_after_zoom != zoom_element_size:
                return True
            else:
                return False

        except Exception as e:
            self.write(str(e), 'debug')
            self.exceptions.append("An exception occurred when zooming")

    def perform_zoom(self, zoom_direction, center_x, center_y):
        """
        Execute zoom based on the zoom direction.
        """
        try:
            start_offset = 400
            end_offset = 100
            actions = ActionChains(self.driver)
            finger1 = actions.w3c_actions.add_pointer_input('touch', 'finger1')
            finger2 = actions.w3c_actions.add_pointer_input('touch', 'finger2')

            if zoom_direction == "in":
                start_offset = 100
                end_offset = 400
            finger1.create_pointer_move(x=center_x - start_offset, y=center_y)
            finger1.create_pointer_down(button=MouseButton.LEFT)
            finger1.create_pause(0.5)
            finger1.create_pointer_move(x=center_x - end_offset, y=center_y, duration=500)
            finger1.create_pointer_up(button=MouseButton.LEFT)

            finger2.create_pointer_move(x=center_x + start_offset, y=center_y)
            finger2.create_pointer_down(button=MouseButton.LEFT)
            finger2.create_pause(0.5)
            finger2.create_pointer_move(x=center_x + end_offset, y=center_y, duration=500)
            finger2.create_pointer_up(button=MouseButton.LEFT)

            actions.perform()

        except Exception as e:
            self.write(str(e), 'debug')
            self.exceptions.append("An exception occured when performing the zooming")

    def get_element_center(self, element):
        """
        Get the coordinates of the element to be zoomed.
        """
        try:
            #Get the zoom element location
            element_location = element.location
            element_x = element_location['x']
            element_y = element_location['y']

            #Get the zoom element size and center
            element_size = element.size
            center_x = element_x + element_size['width'] / 2
            center_y = element_y + element_size['height'] / 2
            coordinates = {"center_x": center_x, "center_y": center_y}

            return coordinates

        except Exception as e:
            self.write(str(e), 'debug')
            self.exceptions.append("An exception occured when getting the element coordinates")

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
            # Get the center of the source element
            source_element = self.get_element(source_locator)
            source_coordinates = self.get_element_center(source_element)
            source_center_x = source_coordinates['center_x']
            source_center_y = source_coordinates['center_y']

            # Get the center of the destination element
            destination_element = self.get_element(destination_locator)
            destination_coordinates = self.get_element_center(destination_element)
            destination_center_x = destination_coordinates['center_x']
            destination_center_y = destination_coordinates['center_y']

            # Perform drag and drop gesture
            actions = ActionChains(self.driver)
            finger1 = actions.w3c_actions.add_pointer_input('touch', 'finger1')
            finger1.create_pointer_move(x=source_center_x, y=source_center_y)
            finger1.create_pointer_down(button=MouseButton.LEFT)
            finger1.create_pause(1)
            finger1.create_pointer_move(x=destination_center_x, y=destination_center_y, duration=500)
            finger1.create_pointer_up(button=MouseButton.LEFT)
            actions.perform()

        except Exception as e:
            self.write(str(e), 'debug')
            self.exceptions.append("An exception occured when performing drag and drop")

    def scroll_to_bottom(self, scroll_amount=10):
        """
        Scroll to the bottom of the page.
        """
        result_flag = False
        try:
            self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR,
            value=f'new UiScrollable(new UiSelector().scrollable(true).instance(0)).flingToEnd({scroll_amount})')
            result_flag = True
        except Exception as e:
            self.write(str(e), 'debug')
            self.exceptions.append("An exception occurred when scrolling to the bottom of the page")
        return result_flag

    def scroll_to_top(self, scroll_amount=10):
        """
        Scroll to the top of the page.
        """
        result_flag = False
        try:
            self.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
            value=f'new UiScrollable(new UiSelector().scrollable(true).instance(0)).flingToBeginning({scroll_amount})')
            result_flag = True
        except Exception as e:
            self.write(str(e),'debug')
            self.exceptions.append("An exception occured when scrolling to top of page")
        return result_flag

    def scroll_backward(self, distance=150):
        "Scroll backward"

        result_flag = False
        try:
            self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                value=f'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollBackward({distance})'
            )
            result_flag = True
        except Exception as e:
            self.write(str(e), 'debug')
            self.exceptions.append("An exception occurred when scrolling backward")
        return result_flag

    def scroll_forward(self, distance=150):
        "Scroll forward"

        result_flag = False
        try:
            self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                value=f'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollForward({distance})'
            )
            result_flag = True
        except Exception as e:
            self.write(str(e), 'debug')
            self.exceptions.append("An exception occurred when scrolling forward")
        return result_flag

    def start(self):
        "Dummy method to be over-written by child classes"
        pass

    def get_source_code(self):
        "To get the source code of the Mobile app page"
        try:
            source = self.driver.page_source
            return source
        except Exception as e:
            self.write(str(e), 'debug')
            self.exceptions.append("An exception occured when getting source")
