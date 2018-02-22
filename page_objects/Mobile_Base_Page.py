"""
Page class that all page models can inherit from
There are useful wrappers for common Selenium operations
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains 
import sys,unittest,time,logging,os,inspect
from utils.Base_Logging import Base_Logging
from inspect import getargspec
from utils.BrowserStack_Library import BrowserStack_Library
from DriverFactory import DriverFactory
from utils.Test_Rail import Test_Rail
import PageFactory


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


class Mobile_Base_Page(Borg,unittest.TestCase):
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

            self.reset()

        self.driver_obj = DriverFactory()
        self.log_obj = Base_Logging(level=logging.DEBUG)
        self.log_obj.set_stream_handler_level(self.log_obj.getStreamHandler(),level=logging.DEBUG)
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


    def register_driver(self,sauce_flag,os_name,os_version,browser,browser_version):
        "Register the driver with Page"
        self.driver = self.driver_obj.get_web_driver(sauce_flag,os_name,os_version,browser,browser_version)
        self.driver.implicitly_wait(5) 
        self.driver.maximize_window()
        self.start()


    def register_mobile_driver(self,mobile_os_name,mobile_os_version,device_name,app_package,app_activity,mobile_sauce_flag,device_flag):
        "Register the mobile driver"
        self.driver = self.driver_obj.run_mobile(mobile_os_name,mobile_os_version,device_name,app_package,app_activity,mobile_sauce_flag,device_flag)
        self.set_screenshot_dir() # Create screenshot directory
        self.start()


    def get_current_driver(self):
        "Return current driver"        
        return self.driver
        
    def get_console_log(self):
        "Return current browser's console logs from driver"
        return self.driver.get_log('browser')

    def get_driver_title(self):
        "Return the title of the current page"
        return self.driver.title


    def get_current_url(self):
        "Return the current url"
        return self.driver.current_url


    def register_testrail(self):
        "Register TestRail with Page"
        self.testrail_flag = True
        self.tr_obj = Test_Rail()
        self.write('Automation registered with TestRail',level='debug')

        
    def register_browserstack(self):
        "Register Browser Stack with Page"
        self.browserstack_flag = True
        self.browserstack_obj = BrowserStack_Library()


    def set_locator_conf(self,locator_path):
        "Set the path of the configuration file with locators"
        self.xpath_conf_file = locator_path
        

    def start(self):
        "Dummy method to be over-written by child classes"
        pass

        
    def _screenshot(func):
        "Decorator for taking screenshot"
        def wrapper(*args,**kwargs):
            result = func(*args, **kwargs)
            screenshot_name = '%003d'%args[0].screenshot_counter + '_' + func.__name__
            args[0].screenshot_counter += 1
            args[0].save_screenshot(screenshot_name)
            return result
        
        return wrapper


    def _exceptionHandler(f):
        "Decorator to handle exceptions"
        argspec = getargspec(f)
        def inner(*args,**kwargs):
            try:
                return f(*args,**kwargs)
            except Exception,e:
                args[0].write('You have this exception')
                args[0].write('Exception in method: %s'%str(f.__name__))
                args[0].write('PYTHON SAYS: %s'%str(e))
                
        return inner 


    def _get_xpath_string(key):
        "Get the value of the given key from the xpath_conf_file"
        xpath_conf_file = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','conf','locators.conf'))
        value = Conf_Reader.get_value(xpath_conf_file,key)

        return value


    def get_calling_module(self):
        "Get the name of the calling module"
        calling_file = inspect.stack()[-1][1]
        calling_filename = calling_file.split(os.sep)

        #This logic bought to you by windows + cygwin + git bash 
        if len(calling_filename) == 1: #Needed for 
            calling_filename = calling_file.split('/')
        
        self.calling_module = calling_filename[-1].split('.')[0]

        return self.calling_module
    

    @_exceptionHandler
    def set_directory_structure(self):
        "Setup the required directory structure if it is not already present"
        screenshots_parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','screenshots'))
        if not os.path.exists(screenshots_parent_dir):
            os.makedirs(screenshots_parent_dir)


    @_exceptionHandler
    def set_screenshot_dir(self):
        "Set the screenshot directory"
        self.screenshot_dir = self.get_screenshot_dir()
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)


    def get_screenshot_dir(self):
        "Get the name of the test"
        testname = self.get_calling_module()
        screenshot_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','screenshots')) + os.sep  + testname
        if os.path.exists(screenshot_dir):
            for i in range(1,4096):
                if os.path.exists(screenshot_dir + '_'+str(i)):
                    continue
                else:
                    os.rename(screenshot_dir,screenshot_dir +'_'+str(i))
                    break

        return screenshot_dir
            

    def append_latest_image(self,screenshot_name):
        "Get image url list from Browser Stack"
        screenshot_url = self.browserstack_obj.get_latest_screenshot_url()
        image_dict = {}
        image_dict['name'] = screenshot_name
        image_dict['url'] = screenshot_url
        self.image_url_list.append(image_dict)
        

    def save_screenshot(self,screenshot_name):
        "Take a screenshot"
        if os.path.exists(self.screenshot_dir + os.sep + screenshot_name+'.jpg'):
            for i in range(1,100): 
                if os.path.exists(self.screenshot_dir + os.sep +screenshot_name+'_'+str(i)+'.jpg'):
                    continue
                else:
                    os.rename(self.screenshot_dir + os.sep +screenshot_name+'.jpg',self.screenshot_dir + os.sep +screenshot_name+'_'+str(i)+'.jpg')
                    break
        self.driver.get_screenshot_as_file(self.screenshot_dir + os.sep+ screenshot_name+'.jpg')
        if self.browserstack_flag is True:
            self.append_latest_image(screenshot_name)
            

    def open(self,wait_time=2):
        "Visit the page base_url + url"
        self.wait(wait_time)


    def get_page_xpaths(self,section):
        "Open configurations file,go to right sections,return section obj"
        pass
        

    def get_xpath(self,xpath,verbose_flag=True):
        "Return the DOM element of the xpath OR the 'None' object if the element is not found"
        dom_element = None
        try:
            dom_element = self.driver.find_element_by_xpath(xpath)
        except Exception,e:
            if verbose_flag is True:
                self.write(str(e),'debug')
        
        return dom_element


    def get_current_window_handle(self):
        "Return the latest window handle"
        return self.driver.current_window_handle


    @_exceptionHandler
    def set_window_name(self,name):
        "Set the name of the current window name"
        window_handle = self.get_current_window_handle()
        self.window_structure[window_handle] = name


    def get_window_by_name(self,window_name):
        "Return window handle id based on name"
        window_handle_id = None
        for id,name in self.window_structure.iteritems():
            if name == window_name:
                window_handle_id = id
                break

        return window_handle_id


    @_exceptionHandler
    def switch_window(self,name=None):
        "Make the driver switch to the last window or a window with a name"
        result_flag = False
        if name is not None:
            window_handle_id = self.get_window_by_name(name)
        else:
            name = "Next"
            window_handle_id = self.driver.window_handles[-1]

        if window_handle_id is not None:
            self.driver.switch_to_window(window_handle_id)
            result_flag = True

        self.conditional_write(result_flag,
                               'Automation switched to the browser window: %s'%name,
                               'Unable to locate and switch to the window with name: %s'%name,
                               level='debug')

        return result_flag


    def close_current_window(self):
        "Close the current window"
        result_flag = False
        try:
            before_window_count = len(self.get_window_handles)
            self.driver.close()
            after_window_count = len(self.get_window_handles)
            if (before_window_count - after_window_count) == 1:
                result_flag = True
        except Exception,e:
            self.write('Could not close the current window')
            self.write(str(e))

        return result_flag


    def get_window_handles(self):
        "Get the window handles"
        return self.driver.window_handles


    def get_current_window_handle(self):
        "Get the current window handle"
        return self.driver.current_window_handle


    def get_xpaths(self,xpath,msg_flag=True):
        "Return a list of DOM elements that match the xpath"
        dom_elements = []
        try:
            dom_elements = self.driver.find_elements_by_xpath(xpath)
        except Exception,e:
            if msg_flag==True:
                self.write(e,'debug')
        
        return dom_elements


    def click_element(self,locator,wait_time=3):
        "Click the button supplied"
        link = self.get_element(locator)
        if link is not None:
            try:
                link.click()
                self.wait(wait_time)
            except Exception,e:
                self.write('Exception when clicking link with path: %s'%locator)
                self.write(e)
            else:
                return True

        return False


    def click_mobile_element(self,xpath=None,id=None,wait_seconds=3):
        "Click the mobile element"
        if xpath is not None:
            link = self.driver.find_element_by_xpath(xpath)
        if id is not None:
            link = self.driver.find_element_by_id(id)
        if link is not None:
            try:
                link.click()
                self.wait(wait_seconds)
            except Exception,e:
                self.write('Exception while clicking link with xpath:%s'%xpath)
                self.write(str(e))
            else:
                return True

        return False


    def set_mobile_text(self,text,xpath=None,id=None,wait_seconds=3):
        "Set a text in the mobile text field"
        if xpath is not None:
            link = self.driver.find_element_by_xpath(xpath)
        if id is not None:
            link = self.driver.find_element_by_id(id)
        if link is not None:
            try:
                link.clear()
                self.wait(wait_seconds)
                link.send_keys(text)
                try:
                    self.driver.hide_keyboard()
                except Exception,e:
                    pass
                else:
                    pass
            except Exception,e:
                self.write('Exception while trying to set text')
                self.write(str(e))
            else:
                return True

        return False
    

    def set_text(self,xpath,value,clear_flag=True):
        "Set the value of the text field"
        text_field = self.get_xpath(xpath)
        try:
            if clear_flag is True:
                text_field.clear()
        except Exception, e:
            self.write('ERROR: Could not clear the text field: %s'%xpath,'debug')

        result_flag = False
        try:
            text_field.send_keys(value)
            result_flag = True
        except Exception,e:
            self.write('Unable to write to text field: %s'%xpath,'debug')
            self.write(str(e),'debug')

        return result_flag
          
          
    def get_text(self,xpath):
        "Return the text for a given xpath or the 'None' object if the element is not found"
        text = ''
        try:
            text = self.get_xpath(xpath).text
        except Exception,e:
            self.write(e)
            return None
        else:
            return text.encode('utf-8')
        

    def get_dom_text(self,dom_element):
        "Return the text of a given DOM element or the 'None' object if the element has no attribute called text"
        text = None
        try:
            text = dom_element.text
            text = text.encode('utf-8')
        except Exception, e:
            self.write(e)
        
        return text


    def select_checkbox(self,xpath):
        "Select a checkbox if not already selected"
        checkbox = self.get_xpath(xpath)
        if checkbox.is_selected() is False:
            result_flag = self.toggle_checkbox(xpath)
        else:
            result_flag = True

        return result_flag


    def deselect_checkbox(self,xpath):
        "Deselect a checkbox if it is not already deselected"
        checkbox = self.get_xpath(xpath)
        if checkbox.is_selected() is True:
            result_flag = self.toggle_checkbox(xpath)
        else:
            result_flag = True

        return result_flag
    unselect_checkbox = deselect_checkbox #alias the method


    def toggle_checkbox(self,xpath):
        "Toggle a checkbox"
        return self.click_element(xpath)


    def select_dropdown_option(self, select_locator, option_text):
        "Selects the option in the drop-down"
        result_flag = False
        dropdown = self.driver.find_element_by_xpath(select_locator)
        for option in dropdown.find_elements_by_tag_name('option'):
            if option.text == option_text:
                option.click()
                result_flag = True
                break

        return result_flag


    def check_element_present(self,xpath):
        "This method checks if the web element is present in page or not and returns True or False accordingly"
        result_flag = False
        if self.get_xpath(xpath,verbose_flag=False) is not None:
            result_flag = True

        return result_flag


    def check_element_displayed(self,xpath):
        "This method checks if the web element is visible on the page or not and returns True or False accordingly"
        result_flag = False
        if self.get_xpath(xpath,verbose_flag=False) is not None:
            element = self.get_xpath(xpath)
            if element.is_displayed() is True:
                result_flag = True

        return result_flag
    

    def get_elements(self,xpath,wait_seconds=1):
        "Return elements list"
        elements = None
        try:
            elements = self.driver.find_elements_by_xpath(xpath)
            self.wait(wait_seconds)
        except Exception,e:
            self.write(e)

        return elements


    def hit_enter(self,xpath,wait_seconds=2):
        "Hit enter"
        element = self.get_xpath(xpath)
        try:
            element.send_keys(Keys.ENTER)
            self.wait(wait_seconds)
        except Exception,e:
            self.write(str(e),'debug')
            return None


    def scroll_down(self,xpath,wait_seconds=2):
        "Scroll down"
        element = self.get_xpath(xpath)
        try:
            element.send_keys(Keys.PAGE_DOWN)
            self.wait(wait_seconds)
        except Exception,e:
            self.write(str(e),'debug')
            return None


    def hover(self,xpath,wait_seconds=2):
        "Hover over the element"
        #Note: perform() of ActionChains does not return a bool 
        #So we have no way of returning a bool when hover is called
        element = self.get_xpath(xpath)
        action_obj = ActionChains(self.driver)
        action_obj.move_to_element(element)
        action_obj.perform()
        self.wait(wait_seconds)
        

    def teardown(self):
        "Tears down the driver"
        self.driver.quit()
        self.reset()


    def write(self,msg,level='info'):
        "Log the message"
        self.msg_list.append('%-8s:  '%level.upper() + msg)
        if self.browserstack_flag is True:
            if self.browserstack_msg not in msg:
                self.msg_list.pop(-1) #Remove the redundant BrowserStack message
        self.log_obj.write(msg,level)


    def get_failure_message_list(self):
        "Return the failure message list"
        return self.failure_message_list


    def success(self,msg,level='info',pre_format='PASS: '):
        "Write out a success message"
        self.log_obj.write(pre_format + msg,level)
        self.result_counter += 1
        self.pass_counter += 1


    def failure(self,msg,level='info',pre_format='FAIL: '):
        "Write out a failure message"
        self.log_obj.write(pre_format + msg,level)
        self.result_counter += 1
        self.failure_message_list.append(pre_format + msg)


    def log_result(self,flag,positive,negative,level='info'):
        "Write out the result of the test"
        if flag is True:
            self.success(positive,level=level)
        if flag is False:
            self.failure(negative,level=level)


    def conditional_write(self,flag,positive,negative,level='debug',pre_format="  - "):
        "Write out either the positive or the negative message based on flag"
        if flag is True:
            self.write(pre_format + positive,level)
            self.mini_check_pass_counter += 1
        if flag is False:
            self.write(pre_format + negative,level)
        self.mini_check_counter += 1


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
            self.tr_obj.update_testrail(case_id,test_run_id,result_flag,msg=msg)
        self.image_url_list = []
        self.msg_list = []
        

    def wait(self,wait_seconds=5,xpath=None):
        "Performs wait for time provided"
        if xpath is not None:
            result_flag = self.explicit_wait(xpath,wait_seconds)
        else:
            time.sleep(wait_seconds)
            result_flag = True

        return result_flag


    def explicit_wait(self,xpath,wait_seconds):
        "Performs an explicit wait for a particular element"
        result_flag = False
        try:
            WebDriverWait(self.driver, wait_seconds).until(EC.presence_of_element_located((By.XPATH, xpath)))
            result_flag =True
        except Exception,e:
            self.write("Unable to locate element with xpath: %s"%xpath,'debug')

        return result_flag


    _screenshot = staticmethod(_screenshot)
    _exceptionHandler = staticmethod(_exceptionHandler)
    _get_xpath_string = staticmethod(_get_xpath_string)


    def get_text_by_locator(self,locator):
        "Return the text for a given path or the 'None' object if the element is not found"
        text = ''
        try:
            text = self.get_element(locator).text
        except Exception,e:
            self.write(e)
            return None
        else:
            return text.encode('utf-8')


    def get_element(self,locator,verbose_flag=True):
        "Return the DOM element of the path or 'None' if the element is not found "
        dom_element = None
        try:
            locator = self.split_locator(locator)
            dom_element = self.driver.find_element(*locator)
        except Exception,e:
            if verbose_flag is True:
                self.write(str(e),'debug')
                self.write("Check your locator-'%s,%s' in the conf/locators.conf file"%(locator[0],locator[1]))
                self.get_session_details()

        return dom_element


    def split_locator(self,locator):
        "Split the locator type and locator"
        result = ()
        try:
            result = tuple(locator.split(',',1))
        except Exception,e:
            self.write("Error while parsing locator")

        return result


    def write_test_summary(self):
        "Print out a useful, human readable summary"
        self.write('\n\n************************\n--------RESULT--------\nTotal number of checks=%d'%self.result_counter)
        self.write('Total number of checks passed=%d\n----------------------\n************************\n\n'%self.pass_counter)
        self.write('Total number of mini-checks=%d'%self.mini_check_counter)
        self.write('Total number of mini-checks passed=%d'%self.mini_check_pass_counter)
        failure_message_list = self.get_failure_message_list()
        if len(failure_message_list) > 0:
            self.write('\n--------FAILURE SUMMARY--------\n')
            for msg in failure_message_list:
                self.write(msg)



