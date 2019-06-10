"""
Simple iOS tests on a sample app, showing accessing elements, setting text and clicking them.
"""
"""
Automated test will do the following:
    # Open the application in iOS device.
    # Enter a value for name field.
    # Enter a value for phone field.
    # Click on submit button.
"""

import os, sys, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from page_objects.PageFactory import PageFactory
from utils.Option_Parser import Option_Parser
import conf.mobile_avinash_conf as conf
import conf.testrail_caseid_conf as testrail_file

def test_mobile_iOS(mobile_os_name, mobile_os_version, device_name, app_package, app_activity, remote_flag, device_flag, testrail_flag, tesults_flag, test_run_id,app_name,app_path,ud_id,org_id,signing_id,no_reset_flag):
#def test_mobile_iOS(mobile_os_name, mobile_os_version, device_name, app_package, app_activity, remote_flag, device_flag, testrail_flag, tesults_flag, test_run_id, app_name,app_path, ud_id, org_id, signing_id, no_reset_flag):
    "Run the test."
    #try:
    # Initalize flags for tests summary.
    expected_pass = 0
    actual_pass = -1

    #1. Create a test object.
    test_obj = PageFactory.get_page_object("avinash demo main page")
    
    #Get the path of the .apk file
    app_path = input('\nEnter the path of .app file:')
    
    #2. Setup and register a driver
    start_time = int(time.time())
    #test_obj.register_driver(mobile_os_name,mobile_os_version,device_name,app_package,app_activity,remote_flag,device_flag,app_name,app_path,ud_id,org_id,signing_id,no_reset_flag)
    test_obj.register_driver(mobile_os_name,mobile_os_version,device_name,app_package,app_activity,remote_flag,device_flag,app_name,app_path,ud_id,org_id,signing_id,no_reset_flag)
    #3. Get the test details from the conf file
    name = conf.name
    phone = conf.phone_no
    
    #4. Set the name in the demo app.
    result_flag = test_obj.set_name_input(name)
    test_obj.log_result(result_flag,
                positive="Successfully set name.",
                negative="Failed to set name.") 

    #5. Set the phone no in the demo app.
    result_flag = test_obj.set_phone_input(phone)
    test_obj.log_result(result_flag,
                positive="Successfully set phone no.",
                negative="Failed to set phone no.")    
    
    #6. Click on submit button.
    result_flag = test_obj.click_submit()
    test_obj.log_result(result_flag,
                positive="Successfully clicked on Submit Button.",
                negative="Failed to click on Submit Button")       

    #7. Print out the results.
    test_obj.write_test_summary()

    #8. Teardown and Assertion.
    test_obj.wait(3)
    expected_pass = test_obj.result_counter
    actual_pass = test_obj.pass_counter
    test_obj.teardown()

    #except Exception as e:
    print ("Exception when trying to run test:%s" % __file__)
    print ("Python says:%s" % str(e))

    assert expected_pass == actual_pass,"Test failed: %s"%__file__


# ---START OF SCRIPT

if __name__ == '__main__':
    print ("Start of %s" % __file__)
    # Creating an instance of the class.
    options_obj = Option_Parser()
    options = options_obj.get_options()
    
    # Run  the test only if the options provided are valid.
    if options_obj.check_options(options):
        test_mobile_iOS(mobile_os_name = options.mobile_os_name,
                          mobile_os_version = options.mobile_os_version,
                          device_name = options.device_name,
                          app_package = options.app_package,
                          app_activity = options.app_activity,
                          remote_flag = options.remote_flag,
                          device_flag = options.device_flag,
                          testrail_flag = options.testrail_flag,
                          test_run_id = options.test_run_id,
                          app_name = options.app_name,
                          ud_id = options.aud_id,
                          org_id = options.org_id,
                          signing_id = options.signing_id,
                          no_reset_flag = options.no_reset_flag)
    else:
        print ('ERROR: Received incorrect comand line input arguments')
        print (options_obj.print_usage())
