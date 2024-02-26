"""
Page class that all page models can inherit from
There are useful wrappers for common Selenium operations
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest,time,logging,os,inspect
from utils.Base_Logging import Base_Logging
from utils.stop_test_exception_util import Stop_Test_Exception
from .driverfactory import DriverFactory
from .core_helpers.selenium_objects import Selenium_Objects
from .core_helpers.logging_objects import Logging_Objects
from .core_helpers.test_reporting_objects import Test_Reporting_Objects
from .core_helpers.screenshot_objects import Screenshot_Objects
from page_objects import PageFactory
from utils import Gif_Maker

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

class Mobile_Base_Page(Borg,unittest.TestCase, Selenium_Objects, Logging_Objects, Test_Reporting_Objects, Screenshot_Objects):
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
        self.screenshot_counter = 1

    def switch_page(self,page_name):
        "Switch the underlying class to the required Page"
        self.__class__ = PageFactory.PageFactory.get_page_object(page_name).__class__

    def register_driver(self,mobile_os_name,mobile_os_version,device_name,app_package,app_activity,remote_flag,device_flag,app_name,app_path,ud_id,org_id,signing_id,no_reset_flag,appium_version):
        "Register the mobile driver"
        self.driver = self.driver_obj.run_mobile(mobile_os_name,mobile_os_version,device_name,app_package,app_activity,remote_flag,device_flag,app_name,app_path,ud_id,org_id,signing_id,no_reset_flag,appium_version)
        self.set_screenshot_dir() # Create screenshot directory
        self.set_log_file()
        self.start()

    def get_driver_title(self):
        "Return the title of the current page"
        return self.driver.title

    def get_calling_module(self):
        "Get the name of the calling module"
        calling_file = inspect.stack()[-1][1]
        if 'runpy' or 'string' in calling_file:
            calling_file = inspect.stack()[4][3]
        calling_filename = calling_file.split(os.sep)
        #This logic bought to you by windows + cygwin + git bash
        if len(calling_filename) == 1: #Needed for
            calling_filename = calling_file.split('/')

        self.calling_module = calling_filename[-1].split('.')[0]
        return self.calling_module

    def set_screenshot_dir(self):
        "Set the screenshot directory"
        try:
            self.screenshot_dir = self.get_screenshot_dir()
            if not os.path.exists(self.screenshot_dir):
                os.makedirs(self.screenshot_dir)
        except Exception as e:
            self.write("Exception when trying to set screenshot directory")
            self.write(str(e))
    def get_screenshot_dir(self):
        "Get the name of the test"
        self.testname = self.get_test_name()
        self.screenshot_dir = self.screenshot_directory(self.testname)
        return self.screenshot_dir
    def open(self,wait_time=2):
        "Visit the page base_url + url"
        self.wait(wait_time)

    def smart_wait(self,wait_seconds,locator):
        "Performs an explicit wait for a particular element"
        result_flag = False
        try:
            path = self.split_locator(locator)
            WebDriverWait(self.driver, wait_seconds).until(EC.presence_of_element_located(path))
            result_flag =True
        except Exception:
                    self.conditional_write(result_flag,
                    positive='Located the element: %s'%locator,
                    negative='Could not locate the element %s even after %.1f seconds'%(locator,wait_seconds))

        return result_flag

    def conditional_write(self,flag,positive,negative,level='debug',pre_format="  - "):
        "Write out either the positive or the negative message based on flag"
        if flag is True:
            self.write(pre_format + positive,level)
            self.mini_check_pass_counter += 1
        if flag is False:
            self.write(pre_format + negative,level)
        self.mini_check_counter += 1

    def start(self):
        "Dummy method to be over-written by child classes"
        pass

