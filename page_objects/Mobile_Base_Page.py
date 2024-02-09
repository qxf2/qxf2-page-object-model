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
from .selenium_objects import Selenium_Objects
from .logging_objects import Logging_Objects
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

class Mobile_Base_Page(Borg,unittest.TestCase, Selenium_Objects, Logging_Objects):
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

    def make_gif(self):
        "Create a gif of all the screenshots within the screenshots directory"
        self.gif_file_name = Gif_Maker.make_gif(self.screenshot_dir,name=self.calling_module)

    def get_current_driver(self):
        "Return current driver"
        return self.driver

    def get_driver_title(self):
        "Return the title of the current page"
        return self.driver.title

    def register_testrail(self):
        "Register TestRail with Page"
        from utils.Test_Rail import Test_Rail  # pylint: disable=import-error,import-outside-toplevel
        self.testrail_flag = True
        self.testrail_object = Test_Rail()
        self.write('Automation registered with TestRail',level='debug')

    def set_test_run_id(self,test_run_id):
        "Set TestRail's test run id"
        self.test_run_id = test_run_id

    def register_tesults(self):
        "Register Tesults with Page"
        self.tesults_flag = True

    def register_browserstack(self):
        "Register Browser Stack with Page"
        from utils.BrowserStack_Library import BrowserStack_Library  # pylint: disable=import-error,import-outside-toplevel
        self.browserstack_flag = True
        self.browserstack_obj = BrowserStack_Library()

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

    def set_directory_structure(self):
        "Setup the required directory structure if it is not already present"
        try:
            self.screenshots_parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','screenshots'))
            if not os.path.exists(self.screenshots_parent_dir):
                os.makedirs(self.screenshots_parent_dir)
            self.logs_parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','log'))
            if not os.path.exists(self.logs_parent_dir):
                os.makedirs(self.logs_parent_dir)
        except Exception as e:
            self.write("Exception when trying to set directory structure")
            self.write(str(e))

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
        self.testname = self.get_calling_module()
        self.testname =self.testname.replace('<','')
        self.testname =self.testname.replace('>','')
        self.screenshot_dir = self.screenshots_parent_dir + os.sep  + self.testname
        if os.path.exists(self.screenshot_dir):
            for i in range(1,4096):
                if os.path.exists(self.screenshot_dir + '_'+str(i)):
                    continue
                else:
                    os.rename(self.screenshot_dir,self.screenshot_dir +'_'+str(i))
                    break

        return self.screenshot_dir

    def append_latest_image(self,screenshot_name):
        "Get image url list from Browser Stack"
        screenshot_url = self.browserstack_obj.get_latest_screenshot_url()
        image_dict = {}
        image_dict['name'] = screenshot_name
        image_dict['url'] = screenshot_url
        self.image_url_list.append(image_dict)

    def save_screenshot(self,screenshot_name):
        "Take a screenshot"
        if os.path.exists(self.screenshot_dir + os.sep + screenshot_name+'.png'):
            for i in range(1,100):
                if os.path.exists(self.screenshot_dir + os.sep +screenshot_name+'_'+str(i)+'.png'):
                    continue
                else:
                    os.rename(self.screenshot_dir + os.sep +screenshot_name+'.png',self.screenshot_dir + os.sep +screenshot_name+'_'+str(i)+'.png')
                    break
        self.driver.get_screenshot_as_file(self.screenshot_dir + os.sep+ screenshot_name+'.png')
        if self.browserstack_flag is True:
            self.append_latest_image(screenshot_name)

    def open(self,wait_time=2):
        "Visit the page base_url + url"
        self.wait(wait_time)

    def set_text(self,locator,value,clear_flag=True):
        "Set the value of the text field"
        text_field = self.get_element(locator)
        try:
            if clear_flag is True:
                text_field.clear()
        except Exception as e:
            self.write('ERROR: Could not clear the text field: %s'%locator,'debug')

        result_flag = False
        try:
            text_field.send_keys(value)
            result_flag = True
        except Exception as e:
            self.write('Unable to write to text field: %s'%locator,'debug')
            self.write(str(e),'debug')

        return result_flag

    def teardown(self):
        "Tears down the driver"
        self.driver.quit()
        self.reset()

    def report_to_testrail(self,case_id,test_run_id,result_flag,msg=''):
        "Update Test Rail"
        if self.testrail_flag is True:
            self.write('Automation is about to update TestRail for case id: %s'%str(case_id),level='debug')
            msg += '\n'.join(self.msg_list)
            msg = msg + "\n"
            if self.browserstack_flag is True:
                for image in self.image_url_list:
                    msg += '\n' + '[' + image['name'] + ']('+ image['url']+')'
                msg += '\n\n' + '[' + 'Watch Replay On BrowserStack' + ']('+ self.session_url+')'
            self.testrail_object.update_testrail(case_id,test_run_id,result_flag,msg=msg)
        self.image_url_list = []
        self.msg_list = []

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

