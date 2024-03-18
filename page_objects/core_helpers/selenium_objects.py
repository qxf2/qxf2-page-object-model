"""
Helper class for Selenium Objects
"""
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Selenium_Objects:

    def get_current_driver(self):
        "Return current driver."
        return self.driver

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

    def check_element_present(self,locator):
        "This method checks if the web element is present in page or not and returns True or False accordingly"
        result_flag = False
        if self.get_element(locator,verbose_flag=False) is not None:
            result_flag = True

        return result_flag

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

    def select_dropdown_option(self, locator, option_text):
        "Selects the option in the drop-down"
        result_flag= False
        try:
            dropdown = self.get_element(locator)
            for option in dropdown.find_elements(By.TAG_NAME,'option'):
                if option.text == option_text:
                    option.click()
                    result_flag = True
                    break
        except Exception as e:
            self.write(e)
            self.exceptions.append("Error when selecting option from the drop-down '%s' "%locator)

        return result_flag

    def get_page_paths(self,section):
        "Open configurations file,go to right sections,return section obj"
        pass

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
    get_text_by_locator = get_text #alias the method



    def split_locator(self,locator):
        "Split the locator type and locator"
        result = ()
        try:
            result = tuple(locator.split(',',1))
        except Exception as e:
            self.write(str(e),'debug')
            self.write("Error while parsing locator")
            self.exceptions.append("Unable to split the locator-'%s,%s' in the conf/locators.conf file"%(locator[0],locator[1]))

        return result

    def toggle_checkbox(self,locator):
        "Toggle a checkbox"
        try:
            return self.click_element(locator)
        except Exception as e:
            self.write(e)
            self.exceptions.append("Error when toggling checkbox-'%s' in the conf/locators.conf file"%locator)

    def wait(self,wait_seconds=5,locator=None):
        "Performs wait for time provided"
        if locator is not None:
            self.smart_wait(locator,wait_seconds=wait_seconds)
        else:
            time.sleep(wait_seconds)

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

    def teardown(self):
        "Tears down the driver"
        self.driver.quit()
        self.reset()

            