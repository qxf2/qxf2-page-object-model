"""
Get the webrivers for local browsers.
"""
from conf import opera_browser_conf
from selenium.webdriver.chrome.options import Options
import sys
from selenium import webdriver

class LocalBrowsers():
    """Class contains methods for getting webfrivers for various browsers."""

    @staticmethod
    def firefox_local():
        """Get webdriver for firefox."""
        local_driver = webdriver.Firefox()

        return local_driver

    @staticmethod
    def explorer_local():
        """Get webdriver for internet explorer."""
        local_driver = webdriver.Ie()

        return local_driver

    @staticmethod
    def chrome_local():
        """Get webdriver for chrome."""
        local_driver = webdriver.Chrome()

        return local_driver

    @staticmethod
    def opera_local():
        """Get webdriver for opera."""
        try:
            opera_browser_location = opera_browser_conf.location
            options = webdriver.ChromeOptions()
            options.binary_location = opera_browser_location # path to opera executable
            local_driver = webdriver.Opera(options=options)

        except Exception as exception:
            print("\nException when trying to get remote webdriver:%s"%sys.modules[__name__])
            print("Python says:%s"%str(exception))
            if  'no Opera binary' in str(exception):
                print("SOLUTION: It looks like you are trying to use Opera Browser. Please update Opera Browser location under conf/opera_browser_conf.\n")

        return local_driver

    @staticmethod
    def safari_local():
        """Get webdriver for safari."""
        local_driver = webdriver.Safari()

        return local_driver

    @staticmethod
    def headless_chrome():
        """Set up headless chrome driver options and get webdriver for headless chrome."""
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-certificate-errors')
        local_driver = webdriver.Chrome(options=options)

        return local_driver
