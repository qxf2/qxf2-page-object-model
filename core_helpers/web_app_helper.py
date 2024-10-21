"""
Page class that all page models can inherit from
There are useful wrappers for common Selenium operations
"""
import inspect
from selenium.webdriver.common.by import By
from core_helpers.drivers.driverfactory import DriverFactory
from .selenium_action_objects import Selenium_Action_Objects
from .remote_objects import Remote_Objects
from .logging_objects import Logging_Objects
from .screenshot_objects import Screenshot_Objects
from page_objects import PageFactory
import conf.base_url_conf
from utils import accessibility_util
from utils import snapshot_util

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

class Web_App_Helper(Borg, Selenium_Action_Objects, Logging_Objects, Remote_Objects, Screenshot_Objects):
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
            self.gif_import_flag = False
            self.images = []
            self.highlight_flag = False
            self.test_run_id = None
            self.reset()
        self.base_url = base_url
        self.driver_obj = DriverFactory()
        if self.driver is not None:
            self.start() #Visit and initialize xpaths for the appropriate page
            self.axe_util = accessibility_util.Accessibilityutil(self.driver)
            self.snapshot_util = snapshot_util.Snapshotutil()

    def reset(self):
        "Reset the base page object"
        self.driver = None
        self.calling_module = None
        self.result_counter = 0 #Increment whenever success or failure are called
        self.pass_counter = 0 #Increment everytime success is called
        self.mini_check_counter = 0 #Increment when conditional_write is called
        self.mini_check_pass_counter = 0 #Increment when conditional_write is called with True
        self.failure_message_list = []
        self.failed_scenarios = [] # <- Collect the failed scenarios for prettytable summary
        self.screenshot_counter = 1
        self.exceptions = []
        self.gif_file_name = None
        self.rp_logger = None
        self.highlight_flag = False

    def switch_page(self,page_name):
        "Switch the underlying class to the required Page"
        self.__class__ = PageFactory.PageFactory.get_page_object(page_name,base_url=self.base_url).__class__

    def register_driver(self,remote_flag,os_name,os_version,browser,browser_version,remote_project_name,remote_build_name,testname):
        "Register the driver with Page."
        self.set_screenshot_dir(os_name,os_version,browser,browser_version) # Create screenshot directory
        self.set_log_file()
        self.driver,self.session_url = self.driver_obj.get_web_driver(remote_flag,os_name,os_version,browser,browser_version,
                                                                          remote_project_name,remote_build_name,testname)
        if self.session_url:
            self.write( "Cloud Session URL for test: " + self.calling_module + '\n' + str(self.session_url))
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()

        self.start()

    def turn_on_highlight(self):
        "Highlight the elements being operated upon"
        self.highlight_flag = True

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

    def set_screenshot_dir(self,os_name,os_version,browser,browser_version):
        "Set the screenshot directory"
        self.screenshot_dir = self.get_screenshot_dir(os_name,os_version,browser,browser_version)
        self.create_dir_screenshot = self.create_screenshot_dir(self.screenshot_dir)

    def get_screenshot_dir(self,os_name,os_version,browser,browser_version):
        "Get the name of the test"
        if os_name == 'OS X':
            os_name = 'OS_X'
        if isinstance(os_name,list):
            windows_browser_combination = browser.lower()
        else:
            windows_browser_combination = os_name.lower() + '_' + str(os_version).lower() + '_' + browser.lower()+ '_' + str(browser_version)
        self.testname = self.get_test_name()
        self.testname = self.testname + '[' + str(windows_browser_combination)+ ']'
        self.screenshot_dir = self.screenshot_directory(self.testname)
        return self.screenshot_dir

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

    def get_current_window_handle(self):
        "Return the latest window handle"
        return self.driver.current_window_handle

    def set_window_name(self,name):
        "Set the name of the current window name"
        try:
            window_handle = self.get_current_window_handle()
            self.window_structure[window_handle] = name
        except Exception as e:
            self.write("Exception when trying to set windows name",'critical')
            self.write(str(e),'critical')
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
                self.driver.switch_to.window(window_handle_id)
                result_flag = True

            self.conditional_write(result_flag,
                                'Automation switched to the browser window: %s'%name,
                                'Unable to locate and switch to the window with name: %s'%name,
                                level='debug')
        except Exception as e:
            self.write("Exception when trying to switch window",'critical')
            self.write(str(e),'critical')
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
            self.write('Could not close the current window','critical')
            self.write(str(e),'critical')
            self.exceptions.append("Error when trying to close the current window")

        return result_flag

    def get_window_handles(self):
        "Get the window handles"
        return self.driver.window_handles

    def switch_frame(self,name=None,index=None,wait_time=2):
        "Make the driver switch to the frame"
        result_flag = False
        self.wait(wait_time)
        self.driver.switch_to.default_content()
        try:
            if name is not None:
                self.driver.switch_to.frame(name)
            elif index is not None:
                self.driver.switch_to.frame(self.driver.find_elements(By.TAG_NAME,("iframe")[index]))
            result_flag = True

        except Exception as e:
            self.write("Exception when trying to switch frame",'critical')
            self.write(str(e),'critical')
            self.exceptions.append("Error when switching to frame")

        return result_flag

    def get_element_attribute_value(self,element,attribute_name):
        "Return the elements attribute value if present"
        attribute_value = None
        if hasattr(element,attribute_name):
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

    def accessibility_inject_axe(self):
        "Inject Axe into the Page"
        try:
            return self.axe_util.inject()
        except Exception as e:
            self.write(str(e),'critical')

    def accessibility_run_axe(self):
        "Run Axe into the Page"
        try:
            return self.axe_util.run()
        except Exception as e:
            self.write(str(e),'critical')

    def snapshot_assert_match(self, value, snapshot_name):
        "Asserts the current value of the snapshot with the given snapshot_name"
        result_flag = False
        try:
            self.snapshot_util.assert_match(value, snapshot_name)
            result_flag = True
        except Exception as e:
            self.write(str(e),'critical')

        return result_flag

    def read_browser_console_log(self):
        "Read Browser Console log"
        log = None
        try:
            log = self.driver.get_log('browser')
            return log
        except Exception as e:
            self.write("Exception when reading Browser Console log",'critical')
            self.write(str(e),'critical')
            return log

    def conditional_write(self,flag,positive,negative,level='info'):
        "Write out either the positive or the negative message based on flag"
        self.mini_check_counter += 1
        if level.lower() == "inverse":
            if flag is True:
                self.write(positive,level='error')
            else:
                self.write(negative,level='success')
                self.mini_check_pass_counter += 1
        else:
            if flag is True:
                self.write(positive,level='success')
                self.mini_check_pass_counter += 1
            else:
                self.write(negative,level='error')

    def start(self):
        "Overwrite this method in your Page module if you want to visit a specific URL"
        pass
