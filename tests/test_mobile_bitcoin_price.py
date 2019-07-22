"""
Automated test will do the following:
    # Open Bitcoin Info application in emulator.
    # Click on the bitcoin real time price page button.
    # Compare expected bitcoin real time price page heading with current page heading.
    # Verify that the bitcoin real time price is displayed on the page.
    # Display the results.
"""
import os, sys, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from page_objects.PageFactory import PageFactory
from utils.Option_Parser import Option_Parser
import conf.mobile_bitcoin_conf as conf
import conf.testrail_caseid_conf as testrail_file


def test_mobile_bitcoin_price(mobile_os_name, mobile_os_version, device_name, app_package, app_activity, remote_flag, device_flag, testrail_flag, tesults_flag, test_run_id,app_name,app_path):
    "Run the test."
    try:
        # Initalize flags for tests summary.
        expected_pass = 0
        actual_pass = -1

        #1. Create a test object.
        test_obj = PageFactory.get_page_object("bitcoin main page")      
        
        #2. Setup and register a driver
        start_time = int(time.time())
        test_obj.register_driver(mobile_os_name,mobile_os_version,device_name,app_package,app_activity,remote_flag,device_flag,app_name,app_path)

        #3. Setup TestRail reporting
        if testrail_flag.lower()=='y':
            if test_run_id is None:
                test_obj.write('\033[91m'+"\n\nTestRail Integration Exception: It looks like you are trying to use TestRail Integration without providing test run id. \nPlease provide a valid test run id along with test run command using -R flag and try again. for eg: pytest -X Y -R 100\n"+'\033[0m')
                testrail_flag = 'N'   
            if test_run_id is not None:
                test_obj.register_testrail()

        if tesults_flag.lower()=='y':
            test_obj.register_tesults()

        #4. Get expected bitcoin price page header name
        expected_bitcoin_price_page_heading = conf.expected_bitcoin_price_page_heading
        
        #5. Click on real time price page button and verify the price page header name.
        result_flag = test_obj.click_on_real_time_price_button(expected_bitcoin_price_page_heading)
        test_obj.log_result(result_flag,
                    positive="Successfully visited the bitcoin real time price page.",
                    negative="Failed to visit the bitcoin real time price page.")
        #Update TestRail
        case_id = testrail_file.test_bitcoin_price_page_header
        test_obj.report_to_testrail(case_id,test_run_id,result_flag)
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
        
        #6. Verify bitcoin real time price is displayed.
        if result_flag is True:
            result_flag = test_obj.get_bitcoin_real_time_price()
        test_obj.log_result(result_flag,
                            positive="Successfully got the bitcoin real time price in usd.",
                            negative="Failed to get the bitcoin real time price in usd.")
        #Update TestRail
        case_id = testrail_file.test_bitcoin_real_time_price
        test_obj.report_to_testrail(case_id,test_run_id,result_flag)
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))

        #7. Print out the results.
        test_obj.write_test_summary()

        #8. Teardown and Assertion.
        test_obj.wait(3)
        expected_pass = test_obj.result_counter
        actual_pass = test_obj.pass_counter
        test_obj.teardown()

    except Exception as e:
        print("Exception when trying to run test:%s" % __file__)
        print("Python says:%s" % str(e))

    assert expected_pass == actual_pass,"Test failed: %s"%__file__


# ---START OF SCRIPT

if __name__ == '__main__':
    print("Start of %s" % __file__)
    # Creating an instance of the class.
    options_obj = Option_Parser()
    options = options_obj.get_options()
    
    # Run  the test only if the options provided are valid.
    if options_obj.check_options(options):
        test_mobile_bitcoin_price(mobile_os_name = options.mobile_os_name,
                          mobile_os_version = options.mobile_os_version,
                          device_name = options.device_name,
                          app_package = options.app_package,
                          app_activity = options.app_activity,
                          remote_flag = options.remote_flag,
                          device_flag = options.device_flag,
                          testrail_flag = options.testrail_flag,
                          test_run_id = options.test_run_id,
                          app_name = options.app_name)
    else:
        print('ERROR: Received incorrect comand line input arguments')
        print(options_obj.print_usage())
