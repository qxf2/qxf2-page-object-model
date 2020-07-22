"""
Page class that all page models can inherit from
There are useful wrappers for common Selenium operations
"""
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import unittest,time,logging,os,inspect,pytest
from utils.Base_Logging import Base_Logging
from utils.BrowserStack_Library import BrowserStack_Library
from .DriverFactory import DriverFactory
from page_objects import PageFactory
from utils.Test_Rail import Test_Rail
from utils import Tesults
from utils.stop_test_exception_util import Stop_Test_Exception
import conf.remote_credentials
import conf.base_url_conf
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

# Get the Base URL from the conf file
base_url = conf.base_url_conf

class Base_Page(Borg,unittest.TestCase):
    "Page class that all page models can inherit from"

    def __init__(self,base_url):
        "Constructor"
        Borg.__init__(self)
        if self.is_first_time():
            #Do these actions if this the first time this class is initialized
            self.set_directory_structure()
            self.image_url_list = []
            self.msg_list = []
            self.current_console_log_errors = []
            self.window_structure = {}
            self.testrail_flag = False
            self.tesults_flag = False
            self.images = []
            self.browserstack_flag = False
            self.highlight_flag = False
            self.test_run_id = None
            self.reset()
        self.base_url = base_url
        self.driver_obj = DriverFactory()
        if self.driver is not None:
            self.start() #Visit and initialize xpaths for the appropriate page


    def reset(self):
        "Reset the base page object"
        self.driver = None
        self.calling_module = None
        self.result_counter = 0 #Increment whenever success or failure are called
        self.pass_counter = 0 #Increment everytime success is called
        self.mini_check_counter = 0 #Increment when conditional_write is called
        self.mini_check_pass_counter = 0 #Increment when conditional_write is called with True
        self.failure_message_list = []
        self.screenshot_counter = 1
        self.exceptions = []
        self.gif_file_name = None


    def turn_on_highlight(self):
        "Highlight the elements being operated upon"
        self.highlight_flag = True

    def turn_off_highlight(self):
        "Turn off the highlighting feature"
        self.highlight_flag = False

    def get_failure_message_list(self):
        "Return the failure message list"
        return self.failure_message_list


    def switch_page(self,page_name):
        "Switch the underlying class to the required Page"
        self.__class__ = PageFactory.PageFactory.get_page_object(page_name,base_url=self.base_url).__class__


    def register_driver(self,remote_flag,os_name,os_version,browser,browser_version,remote_project_name,remote_build_name):
        "Register the driver with Page."
        self.set_screenshot_dir(os_name,os_version,browser,browser_version) # Create screenshot directory
        self.set_log_file()
        self.driver = self.driver_obj.get_web_driver(remote_flag,os_name,os_version,browser,browser_version,remote_project_name,remote_build_name)
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()

        if conf.remote_credentials.REMOTE_BROWSER_PLATFORM == 'BS' and remote_flag.lower() == 'y':
            self.register_browserstack()
            self.session_url = self.browserstack_obj.get_session_url()
            self.browserstack_msg = 'BrowserStack session URL:'
            self.write( self.browserstack_msg + '\n' + str(self.session_url))

        self.start()


    def get_current_driver(self):
        "Return current driver."
        return self.driver


    def register_testrail(self):
        "Register TestRail with Page"
        self.testrail_flag = True
        self.tr_obj = Test_Rail()

    def set_test_run_id(self,test_run_id):
        "Set TestRail's test run id"
        self.test_run_id = test_run_id

    def register_tesults(self):
        "Register Tesults with Page"
        self.tesults_flag = True

    def register_browserstack(self):
        "Register Browser Stack with Page"
        self.browserstack_flag = True
        self.browserstack_obj = BrowserStack_Library()

    def set_calling_module(self,name):
        "Set the test name"
        self.calling_module = name

    def get_calling_module(self):
        "Get the name of the calling module"
        if self.calling_module is None:
            #Try to intelligently figure out name of test when not using pytest
            full_stack = inspect.stack()
            index = -1
            for stack_frame in full_stack:
                print(stack_frame[1],stack_frame[3])
                #stack_frame[1] -> file name
                #stack_frame[3] -> method
                if 'test_' in stack_frame[1]:
                    index = full_stack.index(stack_frame)
                    break
            test_file = full_stack[index][1]
            test_file = test_file.split(os.sep)[-1]
            testname = test_file.split('.py')[0]
            self.set_calling_module(testname)

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
            self.exceptions.append("Error when setting up the directory structure")


    def set_screenshot_dir(self,os_name,os_version,browser,browser_version):
        "Set the screenshot directory"
        try:
            self.screenshot_dir = self.get_screenshot_dir(os_name,os_version,browser,browser_version,overwrite_flag=True)
            if not os.path.exists(self.screenshot_dir):
                os.makedirs(self.screenshot_dir)
        except Exception as e:
            self.write("Exception when trying to set screenshot directory")
            self.write(str(e))
            self.exceptions.append("Error when setting up the screenshot directory")


    def get_screenshot_dir(self,os_name,os_version,browser,browser_version,overwrite_flag=False):
        "Get the name of the test"
        if os_name == 'OS X':
            os_name = 'OS_X'
        if isinstance(os_name,list):
            windows_browser_combination = browser.lower()
        else:
            windows_browser_combination = os_name.lower() + '_' + str(os_version).lower() + '_' + browser.lower()+ '_' + str(browser_version)
        self.testname = self.get_calling_module()
        self.testname =self.testname.replace('<','')
        self.testname =self.testname.replace('>','')
        self.testname = self.testname + '[' + str(windows_browser_combination)+ ']'
        self.screenshot_dir = self.screenshots_parent_dir + os.sep + self.testname
        if os.path.exists(self.screenshot_dir) and overwrite_flag is True:
            for i in range(1,4096):
                if os.path.exists(self.screenshot_dir + '_'+str(i)):
                    continue
                else:
                    os.rename(self.screenshot_dir,self.screenshot_dir +'_'+str(i))
                    break

        return self.screenshot_dir


    def set_log_file(self):
        'set the log file'
        self.log_name = self.testname + '.log'
        self.log_obj = Base_Logging(log_file_name=self.log_name,level=logging.DEBUG)


    def append_latest_image(self,screenshot_name):
        "Get image url list from Browser Stack"
        screenshot_url = self.browserstack_obj.get_latest_screenshot_url()
        image_dict = {}
        image_dict['name'] = screenshot_name
        image_dict['url'] = screenshot_url
        self.image_url_list.append(image_dict)


    def save_screenshot_reportportal(self,image_name):
        "Method to save image to ReportPortal"
        try:
            rp_logger = self.log_obj.setup_rp_logging()
            with open(image_name, "rb") as fh:
                image = fh.read()

            rp_logger.info(
                image_name,
                attachment={
                    "data": image,
                    "mime": "application/octet-stream"
                },
            )
        except Exception as e:
            self.write("Exception when trying to get rplogger")
            self.write(str(e))
            self.exceptions.append("Error when trying to get reportportal logger")


    def save_screenshot(self,screenshot_name,pre_format="      #Debug screenshot: "):
        "Take a screenshot"
        if os.path.exists(self.screenshot_dir + os.sep + screenshot_name+'.png'):
            for i in range(1,100):
                if os.path.exists(self.screenshot_dir + os.sep +screenshot_name+'_'+str(i)+'.png'):
                    continue
                else:
                    os.rename(self.screenshot_dir + os.sep +screenshot_name+'.png',self.screenshot_dir + os.sep +screenshot_name+'_'+str(i)+'.png')
                    break
        screenshot_name = self.screenshot_dir + os.sep + screenshot_name+'.png'
        self.driver.get_screenshot_as_file(screenshot_name)
	    #self.conditional_write(flag=True,positive= screenshot_name + '.png',negative='', pre_format=pre_format)
        if hasattr(pytest,'config'):
            if pytest.config._config.getoption('--reportportal'):
                self.save_screenshot_reportportal(screenshot_name)
        if self.browserstack_flag is True:
            self.append_latest_image(screenshot_name)
        if self.tesults_flag is True:
            self.images.append(screenshot_name)


    def open(self,url,wait_time=2):
        "Visit the page base_url + url"
        if self.base_url[-1] != '/' and url[0] != '/':
            url = '/' + url
        if self.base_url[-1] == '/' and url[0] == '/':
            url = url[1:]
        url = self.base_url + url
        if self.driver.current_url != url:
            self.driver.get(url)
        self.wait(wait_time)


    def get_current_url(self):
        "Get the current URL"
        return self.driver.current_url


    def get_page_title(self):
        "Get the current page title"
        return self.driver.title


    def get_page_paths(self,section):
        "Open configurations file,go to right sections,return section obj"
        pass


    def get_current_window_handle(self):
        "Return the latest window handle"
        return self.driver.current_window_handle


    def set_window_name(self,name):
        "Set the name of the current window name"
        try:
            window_handle = self.get_current_window_handle()
            self.window_structure[window_handle] = name
        except Exception as e:
            self.write("Exception when trying to set windows name")
            self.write(str(e))
            self.exceptions.append("Error when setting up the name of the current window")


    def get_window_by_name(self,window_name):
        "Return window handle id based on name"
        window_handle_id = None
        for window_id,name in self.window_structure.iteritems():
            if name == window_name:
                window_handle_id = window_id
                break

        return window_handle_id


    def switch_window(self,name=None):
        "Make the driver switch to the last window or a window with a name"
        result_flag = False
        try:
            if name is not None:
                window_handle_id = self.get_window_by_name(name)
            else:
                window_handle_id = self.driver.window_handles[-1]

            if window_handle_id is not None:
                self.driver.switch_to_window(window_handle_id)
                result_flag = True

            self.conditional_write(result_flag,
                                'Automation switched to the browser window: %s'%name,
                                'Unable to locate and switch to the window with name: %s'%name,
                                level='debug')
        except Exception as e:
            self.write("Exception when trying to switch window")
            self.write(str(e))
            self.exceptions.append("Error when switching browser window")

        return result_flag


    def close_current_window(self):
        "Close the current window"
        result_flag = False
        try:
            before_window_count = len(self.get_window_handles())
            self.driver.close()
            after_window_count = len(self.get_window_handles())
            if (before_window_count - after_window_count) == 1:
                result_flag = True
        except Exception as e:
            self.write('Could not close the current window')
            self.write(str(e))
            self.exceptions.append("Error when trying to close the current window")

        return result_flag


    def get_window_handles(self):
        "Get the window handles"
        return self.driver.window_handles

    def switch_frame(self,name=None,index=None,wait_time=2):
        "switch to iframe"
        self.wait(wait_time)
        self.driver.switch_to.default_content()
        if name is not None:
            self.driver.switch_to.frame(name)
        elif index is not None:
            self.driver.switch_to.frame(self.driver.find_elements_by_tag_name("iframe")[index])

    def _get_locator(key):
        "fetches locator from the locator conf"
        value = None
        try:
            path_conf_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'conf', 'locators.conf'))
            if path_conf_file is not None:
                value = Conf_Reader.get_value(path_conf_file, key)
        except Exception as e:
            print (str(e))
            self.exceptions.append("Error when fetching locator from the locator.conf")

        return value

    def get_element_attribute_value(self,element,attribute_name):
        "Return the elements attribute value if present"
        attribute_value = None
        if (hasattr(element,attribute_name)):
            attribute_value = element.get_attribute(attribute_name)

        return attribute_value

    def highlight_element(self,element,wait_seconds=3):
        "Highlights a Selenium webdriver element"
        original_style = self.get_element_attribute_value(element,'style')
        self.apply_style_to_element(element,"border: 4px solid #F6F7AD;")
        self.wait(wait_seconds)
        self.apply_style_to_element(element,original_style)

    def highlight_elements(self,elements,wait_seconds=3):
        "Highlights a group of elements"
        original_styles = []
        for element in elements:
            original_styles.append(self.get_element_attribute_value(element,'style'))
            self.apply_style_to_element(element,"border: 4px solid #F6F7AD;")
        self.wait(wait_seconds)
        for style,element in zip(original_styles, elements) :
            self.apply_style_to_element(element,style)

    def apply_style_to_element(self,element,element_style):
        self.driver.execute_script("arguments[0].setAttribute('style', arguments[1])", element, element_style)

    def get_element(self,locator,verbose_flag=True):
        "Return the DOM element of the path or 'None' if the element is not found "
        dom_element = None
        try:
            locator = self.split_locator(locator)
            dom_element = self.driver.find_element(*locator)
            if self.highlight_flag is True:
                self.highlight_element(dom_element)
        except Exception as e:
            if verbose_flag is True:
                self.write(str(e),'debug')
                self.write("Check your locator-'%s,%s' in the conf/locators.conf file" %(locator[0],locator[1]))
            self.exceptions.append("Check your locator-'%s,%s' in the conf/locators.conf file" %(locator[0],locator[1]))

        return dom_element


    def split_locator(self,locator):
        "Split the locator type and locator"
        result = ()
        try:
            result = tuple(locator.split(',',1))
        except Exception as e:
            self.write(str(e),'debug')
            self.write("Error while parsing locator")
            self.exceptions.append("Unable to split the locator-'%s' in the conf/locators.conf file"%(locator[0],locator[1]))

        return result


    def get_elements(self,locator,msg_flag=True):
        "Return a list of DOM elements that match the locator"
        dom_elements = []
        try:
            locator = self.split_locator(locator)
            dom_elements = self.driver.find_elements(*locator)
            if self.highlight_flag is True:
                self.highlight_elements(dom_elements)
        except Exception as e:
            if msg_flag==True:
                self.write(str(e),'debug')
                self.write("Check your locator-'%s,%s' in the conf/locators.conf file" %(locator[0],locator[1]))
            self.exceptions.append("Unable to locate the element with the xpath -'%s,%s' in the conf/locators.conf file"%(locator[0],locator[1]))

        return dom_elements


    def click_element(self,locator,wait_time=3):
        "Click the button supplied"
        result_flag = False
        try:
            link = self.get_element(locator)
            if link is not None:
                link.click()
                result_flag=True
                self.wait(wait_time)
        except Exception as e:
            self.write(str(e),'debug')
            self.write('Exception when clicking link with path: %s'%locator)
            self.exceptions.append("Error when clicking the element with path,'%s' in the conf/locators.conf file"%locator)

        return result_flag


    def set_text(self,locator,value,clear_flag=True):
        "Set the value of the text field"
        text_field = None
        try:
            text_field = self.get_element(locator)
            if text_field is not None and clear_flag is True:
                try:
                    text_field.clear()
                except Exception as e:
                    self.write(str(e),'debug')
                    self.exceptions.append("Could not clear the text field- '%s' in the conf/locators.conf file"%locator)
        except Exception as e:
            self.write("Check your locator-'%s,%s' in the conf/locators.conf file" %(locator[0],locator[1]))

        result_flag = False
        if text_field is not None:
            try:
                text_field.send_keys(value)
                result_flag = True
            except Exception as e:
                self.write('Could not write to text field: %s'%locator,'debug')
                self.write(str(e),'debug')
                self.exceptions.append("Could not write to text field- '%s' in the conf/locators.conf file"%locator)

        return result_flag


    def get_text(self,locator):
        "Return the text for a given path or the 'None' object if the element is not found"
        text = ''
        try:
            text = self.get_element(locator).text
        except Exception as e:
            self.write(e)
            self.exceptions.append("Error when getting text from the path-'%s' in the conf/locators.conf file"%locator)
            return None
        else:
            return text.encode('utf-8')


    def get_dom_text(self,dom_element):
        "Return the text of a given DOM element or the 'None' object if the element has no attribute called text"
        text = None
        try:
            text = dom_element.text
            text = text.encode('utf-8')
        except Exception as e:
            self.write(e)
            self.exceptions.append("Error when getting text from the DOM element-'%s' in the conf/locators.conf file"%locator)

        return text


    def select_checkbox(self,locator):
        "Select a checkbox if not already selected"
        result_flag = False
        try:
            checkbox = self.get_element(locator)
            if checkbox.is_selected() is False:
                result_flag = self.toggle_checkbox(locator)
            else:
                result_flag = True
        except Exception as e:
            self.write(e)
            self.exceptions.append("Error when selecting checkbox-'%s' in the conf/locators.conf file"%locator)

        return result_flag


    def deselect_checkbox(self,locator):
        "Deselect a checkbox if it is not already deselected"
        result_flag = False
        try:
            checkbox =  self.get_element(locator)
            if checkbox.is_selected() is True:
                result_flag = self.toggle_checkbox(locator)
            else:
                result_flag = True
        except Exception as e:
            self.write(e)
            self.exceptions.append("Error when deselecting checkbox-'%s' in the conf/locators.conf file"%locator)

        return result_flag

    unselect_checkbox = deselect_checkbox #alias the method


    def toggle_checkbox(self,locator):
        "Toggle a checkbox"
        try:
            return self.click_element(locator)
        except Exception as e:
            self.write(e)
            self.exceptions.append("Error when toggling checkbox-'%s' in the conf/locators.conf file"%locator)


    def select_dropdown_option(self, locator, option_text):
        "Selects the option in the drop-down"
        result_flag= False
        try:
            dropdown = self.get_element(locator)
            for option in dropdown.find_elements_by_tag_name('option'):
                if option.text == option_text:
                    option.click()
                    result_flag = True
                    break
        except Exception as e:
            self.write(e)
            self.exceptions.append("Error when selecting option from the drop-down '%s' "%locator)

        return result_flag


    def check_element_present(self,locator):
        "This method checks if the web element is present in page or not and returns True or False accordingly"
        result_flag = False
        if self.get_element(locator,verbose_flag=False) is not None:
            result_flag = True

        return result_flag


    def check_element_displayed(self,locator):
        "This method checks if the web element is present in page or not and returns True or False accordingly"
        result_flag = False
        try:
            if self.get_element(locator) is not None:
                element = self.get_element(locator,verbose_flag=False)
                if element.is_displayed() is True:
                    result_flag = True
        except Exception as e:
            self.write(e)
            self.exceptions.append("Web element not present in the page, please check the locator is correct -'%s' in the conf/locators.conf file"%locator)

        return result_flag


    def hit_enter(self,locator,wait_time=2):
        "Hit enter"
        try:
            element = self.get_element(locator)
            element.send_keys(Keys.ENTER)
            self.wait(wait_time)
        except Exception as e:
            self.write(str(e),'debug')
            self.exceptions.append("An exception occurred when hitting enter")
            return None


    def scroll_down(self,locator,wait_time=2):
        "Scroll down"
        try:
            element = self.get_element(locator)
            element.send_keys(Keys.PAGE_DOWN)
            self.wait(wait_time)
        except Exception as e:
            self.write(str(e),'debug')
            self.exceptions.append("An exception occured when scrolling down")
            return None


    def hover(self,locator,wait_seconds=2):
        "Hover over the element"
        #Note: perform() of ActionChains does not return a bool
        #So we have no way of returning a bool when hover is called
        element = self.get_element(locator)
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
        msg = str(msg)
        self.msg_list.append('%-8s:  '%level.upper() + msg)
        if self.browserstack_flag is True:
            if self.browserstack_msg not in msg:
                self.msg_list.pop(-1) #Remove the redundant BrowserStack message
        self.log_obj.write(msg,level)


    def report_to_testrail(self,case_id,test_run_id,result_flag,msg=''):
        "Update Test Rail"
        if self.testrail_flag is True:
            msg += '\n'.join(self.msg_list)
            msg = msg + "\n"
            if self.browserstack_flag is True:
                for image in self.image_url_list:
                    msg += '\n' + '[' + image['name'] + ']('+ image['url']+')'
                msg += '\n\n' + '[' + 'Watch Replay On BrowserStack' + ']('+ self.session_url+')'
            self.tr_obj.update_testrail(case_id,test_run_id,result_flag,msg=msg)
        self.image_url_list = []
        self.msg_list = []

    def add_tesults_case(self, name, desc, suite, result_flag, msg='', files=[], params={}, custom={}):
        "Update Tesults with test results"
        if self.tesults_flag is True:
            result = "unknown"
            failReason = ""
            if result_flag == True:
                result = "pass"
            if result_flag == False:
                result = "fail"
                failReason = msg
            for image in self.images:
                files.append(self.screenshot_dir + os.sep + image + '.png')
            self.images = []
            caseObj = {'name': name, 'suite': suite, 'desc': desc, 'result': result, 'reason': failReason, 'files': files, 'params': params}
            for key, value in custom.items():
                caseObj[key] = str(value)
            Tesults.add_test_case(caseObj)

    def make_gif(self):
        "Create a gif of all the screenshots within the screenshots directory"
        self.gif_file_name = Gif_Maker.make_gif(self.screenshot_dir,name=self.calling_module)

        return self.gif_file_name


    def wait(self,wait_seconds=5,locator=None):
        "Performs wait for time provided"
        if locator is not None:
            self.smart_wait(locator,wait_seconds=wait_seconds)
        else:
            time.sleep(wait_seconds)


    def smart_wait(self,locator,wait_seconds=5):
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


    def success(self,msg,level='info',pre_format='PASS: '):
        "Write out a success message"
        if level.lower() == 'critical':
            level = 'info'
        self.log_obj.write(pre_format + msg,level)
        self.result_counter += 1
        self.pass_counter += 1


    def failure(self,msg,level='info',pre_format='FAIL: '):
        "Write out a failure message"
        self.log_obj.write(pre_format + msg,level)
        self.result_counter += 1
        self.failure_message_list.append(pre_format + msg)
        if level.lower() == 'critical':
            self.teardown()
            raise Stop_Test_Exception("Stopping test because: "+ msg)


    def log_result(self,flag,positive,negative,level='info'):
        "Write out the result of the test"
        if level.lower() == "inverse":
            if flag is True:
                self.failure(positive,level="error")
            else:
                self.success(negative,level="info")
        else:
            if flag is True:
                self.success(positive,level=level)
            else:
                self.failure(negative,level=level)


    def read_browser_console_log(self):
        "Read Browser Console log"
        log = None
        try:
            log = self.driver.get_log('browser')
            return log
        except Exception as e:
            self.write("Exception when reading Browser Console log")
            self.write(str(e))
            return log


    def conditional_write(self,flag,positive,negative,level='info'):
        "Write out either the positive or the negative message based on flag"
        self.mini_check_counter += 1
        if level.lower() == "inverse":
            if flag is True:
                self.write(positive,level='error')
            else:
                self.write(negative,level='info')
                self.mini_check_pass_counter += 1
        else:
            if flag is True:
                self.write(positive,level='info')
                self.mini_check_pass_counter += 1
            else:
                self.write(negative,level='error')


    def execute_javascript(self,js_script,*args):
        "Execute javascipt"
        try:
            self.driver.execute_script(js_script)
            result_flag = True
        except Exception as e:
            result_flag = False

        return result_flag


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
        if len(self.exceptions) > 0:
            self.exceptions = list(set(self.exceptions))
            self.write('\n--------USEFUL EXCEPTION--------\n')
            for (i,msg) in enumerate(self.exceptions,start=1):
                self.write(str(i)+"- " + msg)
        self.make_gif()
        if self.gif_file_name is not None:
            self.write("Screenshots & GIF created at %s"%self.screenshot_dir)
            self.write('************************')

    def start(self):
        "Overwrite this method in your Page module if you want to visit a specific URL"
        pass


    _get_locator = staticmethod(_get_locator)
