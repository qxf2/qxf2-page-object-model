"""
This class models the home page in Weathershopper application.
"""
# pylint: disable = W0212,E0401
import conf.locators_conf as locators
from utils.Wrapit import Wrapit
from core_helpers.mobile_app_helper import Mobile_App_Helper
from .weather_shopper_homepage_objects import HomepageObjects
from .navigation_menu_objects import NavigationMenuObjects

class WeatherShopperHomePage(Mobile_App_Helper, HomepageObjects, NavigationMenuObjects):
    "Page objects for home page in Weathershopper application."
