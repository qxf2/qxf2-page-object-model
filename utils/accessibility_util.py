"""
This is a class object that contains the following methods
#Inject accessibility
#Run accessibility
"""

import os
from axe_selenium_python import Axe

def inject_accessibility_test(driver):
    "Inject Axe in the test"
    script_url=os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "utils", "axe.min.js"))
    axe = Axe(driver)
    axe.inject()

def run_accessibility_test(driver):
    "Run Axe in the test"
    axe = Axe(driver)
    return axe.run()
   