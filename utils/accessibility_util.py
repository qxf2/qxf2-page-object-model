"""
Accessibility Integration
* This is a class which extends the methods of Axe parent class
"""

import os
from axe_selenium_python import Axe

script_url=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "axe.min.js"))

class Accessibilityutil(Axe):
    "Accessibility object to run accessibility test"
    def __init__(self, driver):
        super().__init__(driver, script_url)
