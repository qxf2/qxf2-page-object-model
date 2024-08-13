"""
Automated test for Weather Shopper mobile application to validate:
1. Menu labels
2. Menu link redirects

The test clicks the links in Menu options and validates the URL in the Webview
"""

# pylint: disable=E0401, C0413
import time
import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from page_objects.PageFactory import PageFactory
from conf.mobile_weather_shopper_conf import menu_option as conf

@pytest.mark.MOBILE
def test_weather_shopper_menu_options(test_mobile_obj):
    "Run the test."
    try:
        # Initialize flags for tests summary.
        expected_pass = 0
        actual_pass = -1

        # Create a test object.
        test_mobile_obj = PageFactory.get_page_object("weathershopper home page")
        test_mobile_obj.switch_to_app_context()
        start_time = int(time.time())

        # Click on Menu option
        result_flag = test_mobile_obj.click_on_menu_option()
        test_mobile_obj.log_result(result_flag,
                                   positive="Successfully clicked on the Menu option",
                                   negative="Failed to click on the menu option",
                                   level="critical")

        close_chrome_tabs_message = "try closing all Chrome tabs and running the test again"
        # Verify Developed by label
        developed_by_label = test_mobile_obj.get_developed_by_label()
        result_flag = True if developed_by_label == conf['developed_by_label'] else False
        test_mobile_obj.log_result(result_flag,
                                   positive="Successfully validated Developed by label",
                                   negative=f"Failed to validate Developed by label, actual label {developed_by_label} does not match expected {conf['developed_by_label']}",
                                   level="critical")

        # Verify About APP label
        about_app_label = test_mobile_obj.get_about_app_label()
        result_flag = True if about_app_label == conf['about_app_label'] else False
        test_mobile_obj.log_result(result_flag,
                                   positive="Successfully validated about the app label",
                                   negative=f"Failed to validate about the app label, actual label {about_app_label} does not match expected {conf['about_app_label']}",
                                   level="critical")

        # Verify Automation framework label
        automation_framework_label = test_mobile_obj.get_automation_framework_label()
        result_flag = True if automation_framework_label == conf['framework_label'] else False
        test_mobile_obj.log_result(result_flag,
                                   positive="Successfully validated Qxf2 automation framework label",
                                   negative=f"Failed to validate Qxf2 Automation Framework label, actual label {automation_framework_label} does not match {conf['framework_label']}",
                                   level="critical")

        # Verify Privacy Policy label
        privacy_policy_label = test_mobile_obj.get_privacy_policy_label()
        result_flag = True if privacy_policy_label == conf['privacy_policy_label'] else False
        test_mobile_obj.log_result(result_flag,
                                   positive="Successfully validated Privacy Policy label",
                                   negative=f"Failed to validate Qxf2 Automation Framework label, actual label {privacy_policy_label} does not match {conf['privacy_policy_label']}",
                                   level="critical")

        # Verify Contact us label
        contact_us_label = test_mobile_obj.get_contact_us_label()
        result_flag = True if contact_us_label == conf['contact_us_label'] else False
        test_mobile_obj.log_result(result_flag,
                                   positive="Successfully validated Contact Us label",
                                   negative=f"Failed to validate Contact Us label, actual label {contact_us_label} does not match {conf['contact_us_label']}",
                                   level="critical")

        # Verify Developed by URL redirect
        result_flag = test_mobile_obj.click_get_developed_by_option()
        test_mobile_obj.log_result(result_flag,
                                   positive="Succesfully clicked on get Developed by option",
                                   negative="Failed to click on get Developed by option",
                                   level="critical")
        test_mobile_obj.dismiss_chrome_welcome() # Dismiss Chrome Welcome screen
        test_mobile_obj = PageFactory.get_page_object("webview")
        test_mobile_obj.switch_to_chrome_context()
        developed_by_url = test_mobile_obj.get_current_url()
        result_flag = True if developed_by_url == conf['developed_by_url'] else False
        test_mobile_obj.log_result(result_flag,
                                   positive="Successfully validated that Developed by URL redirect",
                                   negative=f"Failed to validate the Developed by redirect URL, the actual {developed_by_url} does not match {conf['developed_by_url']} url, {close_chrome_tabs_message}",
                                   level="critical")

        # Go back to the app
        test_mobile_obj = PageFactory.get_page_object("weathershopper home page")
        test_mobile_obj.switch_to_app_context()
        test_mobile_obj.navigate_back_to_app()

        # Click on Menu option
        result_flag = test_mobile_obj.click_on_menu_option()
        test_mobile_obj.log_result(result_flag,
                                    positive="Successfully clicked on the Menu option",
                                    negative="Failed to click on the menu option",
                                    level="critical")

        # Verify About the app URL redirect
        result_flag = test_mobile_obj.click_about_app_option()
        test_mobile_obj.log_result(result_flag,
                                    positive="Successfully clicked on the About app option",
                                    negative="Failed to click on the About app option",
                                    level="critical")
        test_mobile_obj = PageFactory.get_page_object("webview")
        test_mobile_obj.switch_to_chrome_context()
        about_app_url = test_mobile_obj.get_current_url()
        result_flag = True if about_app_url == conf['about_app_url'] else False
        test_mobile_obj.log_result(result_flag,
                                   positive="Successfully validated About app URL redirect",
                                   negative=f"Failed to validte About app URL redirect, actual {about_app_url} does not match {conf['about_app_url']} url, {close_chrome_tabs_message}",
                                   level="critical")

        # Go back to the app
        test_mobile_obj = PageFactory.get_page_object("weathershopper home page")
        test_mobile_obj.switch_to_app_context()
        test_mobile_obj.navigate_back_to_app()

        # Click on Menu option
        result_flag = test_mobile_obj.click_on_menu_option()
        test_mobile_obj.log_result(result_flag,
                                    positive="Successfully clicked on the Menu option",
                                    negative="Failed to click on the Menu option",
                                    level="critical")


        # Verify Automation Framework URL redirect
        result_flag = test_mobile_obj.click_automation_framework_option()
        test_mobile_obj.log_result(result_flag,
                                    positive="Successfully clicked on the Automation framework option",
                                    negative="Failed to click on the Automation framework option",
                                    level="critical")
        test_mobile_obj = PageFactory.get_page_object("webview")
        test_mobile_obj.switch_to_chrome_context()
        automation_framework_url = test_mobile_obj.get_current_url()
        result_flag = True if automation_framework_url == conf['framework_url'] else False
        test_mobile_obj.log_result(result_flag,
                                   positive="Successfully validated Automation framework URL redirect",
                                   negative=f"Failed to validate the Automation framework URL redirect, actual {automation_framework_url} does not match {conf['framework_url']} URL, {close_chrome_tabs_message}",
                                   level="critical")

        # Go back to the app
        test_mobile_obj = PageFactory.get_page_object("weathershopper home page")
        test_mobile_obj.switch_to_app_context()
        test_mobile_obj.navigate_back_to_app()

        # Click on Menu option
        result_flag = test_mobile_obj.click_on_menu_option()
        test_mobile_obj.log_result(result_flag,
                                    positive="Successfully clicked on the Menu option",
                                    negative="Failed to click on the menu option",
                                    level="critical")

        # Click Contact us option
        result_flag = test_mobile_obj.click_contact_us_option()
        test_mobile_obj.log_result(result_flag,
                                    positive="Successfully clicked on the Contact us option",
                                    negative="Failed to click on the Contact us option",
                                    level="critical")
        test_mobile_obj = PageFactory.get_page_object("webview")
        test_mobile_obj.switch_to_chrome_context()
        contact_us_url = test_mobile_obj.get_current_url()
        result_flag = True if contact_us_url == conf['contact_us_url'] else False
        test_mobile_obj.log_result(result_flag,
                                   positive="Successfully validated Contact us URL redirect",
                                   negative=f"Failed to validate Contact us URL redirect,actual {contact_us_url} does not match {conf['contact_us_url']} URL, {close_chrome_tabs_message}",
                                   level="critical")

        # Go back to the app
        test_mobile_obj = PageFactory.get_page_object("weathershopper home page")
        test_mobile_obj.switch_to_app_context()
        test_mobile_obj.navigate_back_to_app()

        # Print out the results.
        test_mobile_obj.write(f'Script duration: {int(time.time() - start_time)} seconds\n')
        test_mobile_obj.write_test_summary()

        # Teardown and Assertion.
        expected_pass = test_mobile_obj.result_counter
        actual_pass = test_mobile_obj.pass_counter

    except Exception as e:
        print(f"Exception when trying to run test: {__file__}")
        print(f"Python says: {str(e)}")

    if expected_pass != actual_pass:
        raise AssertionError(f"Test failed: {__file__}")