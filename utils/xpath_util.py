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
        xpath = f"//{tag}[@{attr}='{element[attr]}']"
        return xpath

    def guess_xpath_button(self, tag, attr, element):
        """Guess the xpath for the button tag"""
        button_xpath = f"//{tag}[{attr}='{element}']"
        return button_xpath

    def guess_xpath_using_contains(self, tag, attr, element):
        """Guess the xpath using contains function"""
        button_contains_xpath = f"//{tag}[contains({attr},'{element}')]"
        return button_contains_xpath

    def generate_xpath(self, soup, driver):
        """Generate the xpath and assign the variable names"""
        result_flag = False
        for guessable_element in self.guessable_elements:
            self.elements = soup.find_all(guessable_element)
            for element in self.elements:
                if (not element.has_attr("type")) or \
                        (element.has_attr("type") and element['type'] != "hidden"):
                    for attr in self.known_attribute_list:
                        if element.has_attr(attr):
                            locator = self.guess_xpath(guessable_element, attr, element)
                            if len(driver.find_elements(by=By.XPATH, value=locator)) == 1:
                                result_flag = True
                                variable_name = self.get_variable_names(element)
                                # checking for the unique variable names
                                if variable_name != '' and variable_name not in self.variable_names:
                                    self.variable_names.append(variable_name)
                                    print(f"{guessable_element}_{variable_name.encode('utf-8').decode('latin-1')} = {locator.encode('utf-8').decode('latin-1')}")
                                    break
                                else:
                                    print(
                                        f"{locator.encode('utf-8').decode('latin-1')} ----> Couldn't generate an appropriate variable name for this xpath")
                        elif guessable_element == 'button' and element.get_text():
                            button_text = element.get_text()
                            if element.get_text() == button_text.strip():
                                locator = self.guess_xpath_button(guessable_element, "text()", element.get_text())
                            else:
                                locator = self.guess_xpath_using_contains(guessable_element, "text()",
                                                                          button_text.strip())
                            if len(driver.find_elements(by=By.XPATH, value=locator)) == 1:
                                result_flag = True
                                # Check for utf-8 characters in the button_text
                                matches = re.search(r"[^\x00-\x7F]", button_text)
                                if button_text.lower() not in self.button_text_lists:
                                    self.button_text_lists.append(button_text.lower())
                                    if not matches:
                                        # Stripping and replacing characters before printing the variable name
                                        print(f"{guessable_element}_{button_text.strip().strip('!?.').encode('utf-8').decode('latin-1').lower().replace(' + ', '_').replace(' & ', '_').replace(' ', '_')} = {locator.encode('utf-8').decode('latin-1')}")
                                    else:
                                        # printing the variable name with utf-8 characters along with the language counter
                                        print(f"{guessable_element}_foreign_language_{self.language_counter} = {locator.encode('utf-8').decode('latin-1')} ---> Foreign language found, please change the variable name appropriately")
                                        self.language_counter += 1
                                else:
                                    # if the variable name is already taken
                                    print(
                                        f"{locator.encode('utf-8').decode('latin-1')} ----> Couldn't generate an appropriate variable name for this xpath")
                                break

                        elif not guessable_element in self.guessable_elements:
                            print("We are not supporting this guessable element")

        return result_flag

    def get_variable_names(self, element):
        """Generate the variable names for the xpath"""
        # condition to check the length of the 'id' attribute and ignore if there are numerics in the 'id' attribute.
        # Also ignoring id values having "input" and "button" strings.
        if (element.has_attr('id') and len(element['id']) > 2) and not bool(
                re.search(r'\d', element['id'])) and (
                "input" not in element['id'].lower() and "button" not in element['id'].lower()):
            variable_name = element['id'].strip("_")
        # condition to check if the 'value' attribute exists and not having date and time values in it.
        elif element.has_attr('value') and element['value'] != '' and not bool(
                re.search(r'([\d]{1,}([/-]|\s|[.])?)+(\D+)?([/-]|\s|[.])?[[\d]{1,}', element['value'])) and not bool(
                re.search(r'\d{1,2}[:]\d{1,2}\s+((am|AM|pm|PM)?)', element['value'])):
            # condition to check if the 'type' attribute exists
            # getting the text() value if the 'type' attribute value is in 'radio','submit','checkbox','search'
            # if the text() is not '', getting the get_text() value else getting the 'value' attribute
            # for the rest of the type attributes printing the 'type'+'value' attribute values.
            # Doing a check to see if 'value' and 'type' attributes values are matching.
            if (element.has_attr('type')) and (element['type'] in ('radio', 'submit', 'checkbox', 'search')):
                if element.get_text() != '':
                    variable_name = f"{element['type']}_{element.get_text().strip().strip('_.')}"
                else:
                    variable_name = f"{element['type']}_{element['value'].strip('_.')}"
            else:
                if element['type'].lower() == element['value'].lower():
                    variable_name = element['value'].strip('_.')
                else:
                    variable_name = f"{element['type']}_{element['value'].strip('_.')}"
        # condition to check if the "name" attribute exists and if the length of "name" attribute is more than 2
        # printing variable name
        elif element.has_attr('name') and len(element['name']) > 2:
            variable_name = element['name'].strip("_")
        # condition to check if the "placeholder" attribute exists and is not having any numerics in it.
        elif element.has_attr('placeholder') and not bool(re.search(r'\d', element['placeholder'])):
            variable_name = element['placeholder']
        # condition to check if the "type" attribute exists and not in text','radio','button','checkbox','search'
        # and printing the variable name
        elif (element.has_attr('type')) and (element['type'] not in ('text', 'button', 'radio', 'checkbox', 'search')):
            variable_name = element['type']
        # condition to check if the "title" attribute exists
        elif element.has_attr('title'):
            variable_name = element['title']
        # condition to check if the "role" attribute exists
        elif element.has_attr('role') and element['role'] != "button":
            variable_name = element['role']
        else:
            variable_name = ''

        return variable_name.lower().replace("+/- ", "").replace("| ", "").replace(" / ", "_"). \
            replace("/", "_").replace(" - ", "_").replace(" ", "_").replace("&", "").replace("-", "_"). \
            replace("[", "_").replace("]", "").replace(",", "").replace("__", "_").replace(".com", "").strip("_")


# -------START OF SCRIPT--------
if __name__ == "__main__":
    print(f"Start of {__file__}")

    # Initialize the xpath object
    xpath_obj = XpathUtil()

    # Get the URL and parse
    url = input("Enter URL: ")

    # Create a chrome session
    driver = webdriver.Chrome()
    driver.get(url)

    # Parsing the HTML page with BeautifulSoup
    page = driver.execute_script("return document.body.innerHTML").encode('utf-8').decode('latin-1')
    soup = BeautifulSoup(page, 'html.parser')

    # execute generate_xpath
    if xpath_obj.generate_xpath(soup, driver) is False:
        print(f"No XPaths generated for the URL:{url}")

    driver.quit()
