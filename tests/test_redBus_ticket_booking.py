"""
This is an automated test to verify the following features under bus ticket booking facility of redBus
    #Open redBus.in/bus-tickets/
    #Set source,destination, onward date, return date on Search Buses form 
    #Click on Search Buses and submit the search information 
    #check if redirected correctly to Search results page
    #Verify source and destination fields are present in the search results page
    #Click on view seats under the first available bus
    #Verify if the seat selection message appears
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
        
        #1. Create a test object and fill the Search Buses form.
        test_obj = PageFactory.get_page_object("redBus Main Page")
        #Set start_time with current time
        start_time = int(time.time())	

        # Turn on the highlighting feature
        test_obj.turn_on_highlight()
                
        #2. Get the test details from the conf file
        source = booking_conf.source
        destination = booking_conf.destination
        onward_date = booking_conf.onward_date
        return_date = booking_conf.return_date
        
        #3. Set search data fields and submit the search buses form
        result_flag = test_obj.submit_form(source,destination,onward_date,return_date)
        test_obj.log_result(result_flag,
                            positive="Successfully submitted the form\n",
                            negative="Failed to submit the form \nOn url: %s"%test_obj.get_current_url(),
                            level="critical")

        #4. Verify if re-directed to the correct page i.e search results page
        if result_flag is True:
            result_flag = test_obj.check_redirect(source,destination)
        test_obj.log_result(result_flag,
                            positive="Redirected correctly to the Search Results page!!\n",
                            negative="Fail: Redirection to the Search Results page failed!")
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
        
        #5. Check if the source and destination elements are present on the redirect page i.e search results page
        if result_flag is True:
            result_flag = test_obj.check_source_and_destination()
        test_obj.log_result(result_flag,
                            positive="Source and destination elements found on the redirect page!!\n",
                            negative="Fail: Source and destination elements NOT found on the redirect page!")
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))

        #6. Click on view seats under the first available bus
        if result_flag is True:
            result_flag = test_obj.click_on_view_seats_button()
        test_obj.log_result(result_flag,
                            positive="Clicked on the View Seats button\n",
                            negative="Failed to click on View Seats button")
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
        
        #7. Verify if the seat selection message appears
        if result_flag is True:
            result_flag = test_obj.check_seat_selection_msg()
        test_obj.log_result(result_flag,
                            positive="Seat selection message appears on click of view seats!\n",
                            negative="Fail: Seat selection message does not appear on click of view seats!")
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
    
        #8. Print out the result
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
        
        test_redBus_ticket_booking(test_obj)
                
        #teardowm
        test_obj.wait(3)
        test_obj.teardown() 
    else:
        print('ERROR: Received incorrect comand line input arguments')
        print(option_obj.print_usage())
