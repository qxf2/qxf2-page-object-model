"""
This is an automated test to verify bus ticket booking facility of redBus
    #Open redBus.in and get navigated to bus-tickets main page
    #Set source,destination, onward date, return date on Search Buses form 
    #Click on Search Buses and check if redirected correctly
    #Verify source and destination fields in the view buses page  
"""
import os,sys,time,pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from page_objects.PageFactory import PageFactory
from utils.Option_Parser import Option_Parser
import conf.testrail_caseid_conf as testrail_file
import conf.ticket_booking_conf as booking_conf 
import pytest


def test_redBus_ticket_booking(test_obj):


    "Run the test"
    try:
        #Initalize flags for tests summary
        expected_pass = 0
        actual_pass = -1
        
        #1. Create a test object and fill the example form.
        test_obj = PageFactory.get_page_object("redBus Main Page")
        #Set start_time with current time
        start_time = int(time.time())	

        # Turn on the highlighting feature
        test_obj.turn_on_highlight()
                
        #4. Get the test details from the conf file
        source = booking_conf.source
        destination = booking_conf.destination
        onward_date = booking_conf.onward_date
        return_date = booking_conf.return_date
        
        #6. Set and submit the search buses form 
        result_flag = test_obj.submit_form(source,destination,onward_date,return_date)
        test_obj.log_result(result_flag,
                            positive="Successfully submitted the form\n",
                            negative="Failed to submit the form \nOn url: %s"%test_obj.get_current_url(),
                            level="critical")

        #7. Check the source and destination locations on the redirect page
        if result_flag is True:
            result_flag = test_obj.check_source_and_destination(source,destination)
        test_obj.log_result(result_flag,
                            positive="Source and destination locations found on the redirect page!!\n",
                            negative="Fail: Source and destination locations mismatch on the redirect page!")
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
        
        #<tbd>. Print out the result
        test_obj.write_test_summary()
        expected_pass = test_obj.result_counter
        actual_pass = test_obj.pass_counter        

    except Exception as e:
        print("Exception when trying to run test: %s"%__file__)
        print("Python says:%s"%str(e))
    
    assert expected_pass == actual_pass, "Test failed: %s"%__file__

    
#---START OF SCRIPT   
if __name__=='__main__':
    print("Start of %s"%__file__)
    
    #Creating an instance of the class
    options_obj = Option_Parser()
    options = options_obj.get_options()
                
    #Run the test only if the options provided are valid
    if options_obj.check_options(options): 
        test_obj = PageFactory.get_page_object("Zero",base_url=options.url)

        #Setup and register a driver
        test_obj.register_driver(options.remote_flag,options.os_name,options.os_version,options.browser,options.browser_version,options.remote_project_name,options.remote_build_name)

        #Setup TestRail reporting
        if options.testrail_flag.lower()=='y':
            if options.test_run_id is None:
                test_obj.write('\033[91m'+"\n\nTestRail Integration Exception: It looks like you are trying to use TestRail Integration without providing test run id. \nPlease provide a valid test run id along with test run command using -R flag and try again. for eg: pytest -X Y -R 100\n"+'\033[0m')
                options.testrail_flag = 'N'   
            if options.test_run_id is not None:
                test_obj.register_testrail()
                test_obj.set_test_run_id(options.test_run_id)

        if options.tesults_flag.lower()=='y':
            test_obj.register_tesults()

        test_redBus_ticket_booking(test_obj)
                
        #teardowm
        test_obj.wait(3)
        test_obj.teardown() 
    else:
        print('ERROR: Received incorrect comand line input arguments')
        print(option_obj.print_usage())
