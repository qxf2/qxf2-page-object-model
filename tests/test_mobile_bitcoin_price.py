"""
Automated test will do the following:
    # Open Bitcoin Info application in emulator.
    # Click on the real time prices page.
    # Compare expected bitcoin real time price page heading and actual page heading.
    # Verify that the real time price of bitcoin is displayed in the usd.
    # Display the result.
"""

import os, sys, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from page_objects.PageFactory import PageFactory
from utils.Option_Parser import Option_Parser
import conf.mobile_bitcoin_conf as conf
import conf.testrail_caseid_conf as testrail_file


def test_price_page(mobile_os_name, mobile_os_version, device_name, app_package, app_activity, mobile_sauce_flag, device_flag):
    "This method is to verify real time price is displayed on the page."
    try:
        # Initalize flags for tests summary.
        expected_pass = 0
        actual_pass = -1

        #1. Create a test object.
        test_obj = PageFactory.get_page_object("bitcoin price page")
        
        #2. Setup and register a driver
        start_time = int(time.time())
        test_obj.register_mobile_driver(mobile_os_name,mobile_os_version,device_name,app_package,app_activity,mobile_sauce_flag,device_flag)

        #3. Get values of real time price of bitcoin.
        expected_bitcoin_price_page_heading = conf.expected_bitcoin_price_page_heading
        
        #4. Click on real time price page link.
        result_flag = test_obj.visit_bitcoin_real_time_price_page(expected_bitcoin_price_page_heading)
        test_obj.log_result(result_flag,
                    positive="Successfully visited bitcoin real time price page.",
                    negative="Failed to visit bitcoin real time price page.")
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
        
        #5. Check the heading on the bitcoin price page
        #Notice you don't need to create a new page object!
        if result_flag is True:
            result_flag = test_obj.get_bitcoin_real_time_price()
        test_obj.log_result(result_flag,
                            positive="Successfully got the bitcoin real time price in usd.",
                            negative="Failed to get the bitcoin real time price in usd.")
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))

        #6. Print out the results.
        test_obj.write_test_summary()

        #7. Teardown and Assertion.
        test_obj.wait(3)
        expected_pass = test_obj.result_counter
        actual_pass = test_obj.pass_counter
        test_obj.teardown()

    except Exception, e:
        print "Exception when trying to run test:%s" % __file__
        print "Python says:%s" % str(e)

    assert expected_pass == actual_pass


# ---START OF SCRIPT

if __name__ == '__main__':
    print "Start of %s" % __file__
    # Creating an instance of the class
    options_obj = Option_Parser()
    options = options_obj.get_options()

    # Run  the test only if the options provided are valid
    if options_obj.check_options(options):
        test_price_page(mobile_os_name = options.mobile_os_name,
                          mobile_os_version = options.mobile_os_version,
                          device_name = options.device_name,
                          app_package = options.app_package,
                          app_activity = options.app_activity,
                          mobile_sauce_flag = options.mobile_sauce_flag,
                          device_flag = options.device_flag,
                          )
    else:
        print 'ERROR: Received incorrect comand line input arguments'
        print options_obj.print_usage()
