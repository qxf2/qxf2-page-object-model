"""
Utility script to verify Chrome and ChromeDriver are correctly set up.
Run this directly to confirm the browser launches before running the test suite.
Usage: python utils/check_chrome_setup.py
"""
import time
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def check_chrome_setup():
    chromedriver_path = shutil.which('chromedriver')
    if not chromedriver_path:
        print("ERROR: chromedriver not found in PATH. Add it to your PATH and retry.")
        return False

    print("chromedriver found at: %s" % chromedriver_path)

    try:
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service)
        driver.get('https://qxf2.com/')
        time.sleep(3)
        print("SUCCESS: Chrome launched and qxf2.com loaded correctly.")
        time.sleep(2)
        driver.quit()
        return True
    except Exception as e:
        print("ERROR: %s" % str(e))
        return False


if __name__ == '__main__':
    check_chrome_setup()
