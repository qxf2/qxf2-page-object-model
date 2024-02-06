"""
Qxf2 Services: Utility script to generate XPaths for the given URL
* Take the input URL from the user
* Parse the HTML content using BeautifulSoup
* Find all Input and Button tags
* Guess the XPaths
* Generate Variable names for the xpaths
* To run the script in Gitbash use command 'python -u utils/xpath_util.py'
"""

import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

class XpathUtil:
    """Class to generate the xpaths"""

    def __init__(self):
        """Initialize the required variables"""
        self.elements = None
        self.guessable_elements = ['input', 'button']
        self.known_attribute_list = ['id', 'name', 'placeholder', 'value', 'title', 'type', 'class']
        self.variable_names = []
        self.button_text_lists = []
        self.language_counter = 1

    def guess_xpath(self, tag, attr, element):
        """Guess the xpath based on the tag, attr, element[attr]"""
        # Class attribute returned as a unicodeded list, so removing 'u from the list
        if isinstance(element[attr], list):
            element[attr] = [i.encode('utf-8').decode('latin-1') for i in element[attr]]
            element[attr] = ' '.join(element[attr])
        xpath = f'//{tag}[@{attr}="{element[attr]}"]'
        return xpath

    def guess_xpath_button(self, tag, attr, element):
        """Guess the xpath for the button tag"""
        button_xpath = f"//{tag}[{attr}='{element}']"
        return button_xpath

    def guess_xpath_using_contains(self, tag, attr, element):
        """Guess the xpath using contains function"""
        button_contains_xpath = f"//{tag}[contains({attr},'{element}')]"
        return button_contains_xpath

    def generate_xpath_for_element(self, guessable_element, element, driver):
        """Generate xpath for a specific element and assign the variable names"""
        result_flag = False

        for attr in self.known_attribute_list:
            if self.process_attribute(guessable_element, attr, element, driver):
                result_flag = True
                break

        return result_flag

    def process_attribute(self, guessable_element, attr, element, driver):
        """Process a specific attribute and generate xpath"""
        if element.has_attr(attr):
            locator = self.guess_xpath(guessable_element, attr, element)
            if len(driver.find_elements(by=By.XPATH, value=locator)) == 1:
                variable_name = self.get_variable_names(element)
                if variable_name != '' and variable_name not in self.variable_names:
                    self.variable_names.append(variable_name)
                    print(f"{guessable_element}_{variable_name.encode('utf-8').decode('latin-1')} ="
                          f" {locator.encode('utf-8').decode('latin-1')}")
                    return True
                print(f"{locator.encode('utf-8').decode('latin-1')} ----> "
                      "Couldn't generate an appropriate variable name for this xpath")
        elif guessable_element == 'button' and element.get_text():
            return self.process_button_text(guessable_element, element, driver)

        return False

    def process_button_text(self, guessable_element, element, driver):
        """Process button text and generate xpath"""
        button_text = element.get_text()
        if element.get_text() == button_text.strip():
            locator = self.guess_xpath_button(guessable_element, "text()", element.get_text())
        else:
            locator = self.guess_xpath_using_contains(guessable_element,\
                      "text()", button_text.strip())
        if len(driver.find_elements(by=By.XPATH, value=locator)) == 1:
            matches = re.search(r"[^\x00-\x7F]", button_text)
            if button_text.lower() not in self.button_text_lists:
                self.button_text_lists.append(button_text.lower())
                if not matches:
                    print(f"""{guessable_element}_{button_text.strip()
                        .strip('!?.').encode('utf-8').decode('latin-1')
                        .lower().replace(' + ', '_').replace(' & ', '_')
                        .replace(' ', '_')} = {locator.encode('utf-8').decode('latin-1')}""")
                else:
                    print(f"""{guessable_element}_foreign_language_{self.language_counter} =
                        {locator.encode('utf-8').decode('latin-1')} ---> 
                        Foreign language found, please change the variable name appropriately""")
                    self.language_counter += 1
            else:
                print(f"""{locator.encode('utf-8').decode('latin-1')} ---->
                    Couldn't generate an appropriate variable name for this xpath""")
            return True

        return False

    def generate_xpath_for_elements(self, guessable_element, driver):
        """Generate xpath for a list of elements and assign the variable names"""
        result_flag = False

        for element in self.elements:
            if (not element.has_attr("type")) or \
            (element.has_attr("type") and element['type'] != "hidden"):
                result_flag |= self.generate_xpath_for_element(guessable_element, element, driver)

        return result_flag

    def generate_xpath(self, soup, driver):
        """Generate the xpath and assign the variable names"""
        result_flag = False

        for guessable_element in self.guessable_elements:
            self.elements = soup.find_all(guessable_element)
            result_flag |= self.generate_xpath_for_elements(guessable_element, driver)

        return result_flag

    def get_variable_names(self, element):
        """Generate the variable names for the xpath"""
        variable_name = ''

        if element.has_attr('id') and self.is_valid_id(element['id']):
            variable_name = self.extract_id(element)
        elif element.has_attr('value') and self.is_valid_value(element['value']):
            variable_name = self.extract_value(element)
        elif element.has_attr('name') and len(element['name']) > 2:
            variable_name = self.extract_name(element)
        elif element.has_attr('placeholder') and self.is_valid_placeholder(element['placeholder']):
            variable_name = self.extract_placeholder(element)
        elif element.has_attr('type') and self.is_valid_type(element['type']):
            variable_name = self.extract_type(element)
        elif element.has_attr('title'):
            variable_name = self.extract_title(element)
        elif element.has_attr('role') and element['role'] != "button":
            variable_name = self.extract_role(element)

        return variable_name

    # Helper functions for specific conditions
    def is_valid_id(self, id_value):
        """Check if the 'id' attribute is valid for generating a variable name."""
        return len(id_value) > 2 and not bool(re.search(r'\d', id_value)) and \
               ("input" not in id_value.lower() and "button" not in id_value.lower())

    def extract_id(self, element):
        """Extract variable name from the 'id' attribute."""
        return element['id'].strip("_")

    def is_valid_value(self, value):
        """Check if the 'value' attribute is valid for generating a variable name."""
        return value != '' and not \
                bool(re.search(r'([\d]{1,}([/-]|\s|[.])?)+(\D+)?([/-]|\s|[.])?[[\d]{1,}', value))\
                and not bool(re.search(r'\d{1,2}[:]\d{1,2}\s+((am|AM|pm|PM)?)', value))

    def extract_value(self, element):
        """Extract variable name from the 'value' attribute."""
        if element.has_attr('type') and \
        element['type'] in ('radio', 'submit', 'checkbox', 'search'):
            return f"{element['type']}_{element.get_text().strip().strip('_.')}"
        return element['value'].strip('_.')

    def extract_name(self, element):
        """Extract variable name from the 'name' attribute."""
        return element['name'].strip("_")

    def is_valid_placeholder(self, placeholder):
        """Check if the 'placeholder' attribute is valid for generating a variable name."""
        return not bool(re.search(r'\d', placeholder))

    def extract_placeholder(self, element):
        """Extract variable name from the 'placeholder' attribute."""
        return element['placeholder']

    def is_valid_type(self, element_type):
        """Check if the 'type' attribute is valid for generating a variable name."""
        return element_type not in ('text', 'button', 'radio', 'checkbox', 'search')

    def extract_type(self, element):
        """Extract variable name from the 'type' attribute."""
        return element['type']

    def extract_title(self, element):
        """Extract variable name from the 'title' attribute."""
        return element['title']

    def extract_role(self, element):
        """Extract variable name from the 'role' attribute."""
        return element['role']

# -------START OF SCRIPT--------
if __name__ == "__main__":
    print(f"Start of {__file__}")

    # Initialize the xpath object
    xpath_obj = XpathUtil()

    # Get the URL and parse
    url = input("Enter URL: ")

    # Create a chrome session
    web_driver = webdriver.Chrome()
    web_driver.get(url)

    # Parsing the HTML page with BeautifulSoup
    page = web_driver.execute_script("return document.body.innerHTML")\
           .encode('utf-8').decode('latin-1')
    soup_parsed = BeautifulSoup(page, 'html.parser')

    # execute generate_xpath
    if xpath_obj.generate_xpath(soup_parsed, web_driver) is False:
        print(f"No XPaths generated for the URL:{url}")

    web_driver.quit()
