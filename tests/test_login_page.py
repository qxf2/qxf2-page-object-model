"""
This is an example automated test to help you learn Qxf2's framework
Our automated test will do the following:
    #Open Qxf2 selenium-tutorial-main page.
    #Fill the example form.
    #Click on Click me! button and check if its working fine.
"""
import os,sys,time,pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from page_objects.PageFactory import PageFactory
from utils.Option_Parser import Option_Parser
import conf.login_conf as conf
import conf.testrail_caseid_conf as testrail_file
import pytest


@pytest.mark.GUI
def test_login_page(test_obj):

    "Run the test"
    try:
        #Initalize flags for tests summary
        expected_pass = 0
        actual_pass = -1

        #1. Create a test object and fill the example form.
        test_obj = PageFactory.get_page_object("login page")
        #Set start_time with current time
        start_time = int(time.time())

        # Turn on the highlighting feature
        test_obj.turn_on_highlight()

        #4. Get the test details from the conf file
        username = conf.user_name
        password = conf.password
        
        #5. Set name in form
        print(username)
        result_flag = test_obj.set_user(username)
        test_obj.log_result(result_flag,
                            positive="Name was successfully set to: %s\n" % username,
                            negative="Failed to set name: %s \nOn url: %s\n" % (username, test_obj.get_current_url()))
        test_obj.write('Script duration: %d seconds\n' %
                       (int(time.time()-start_time)))
        
        #6. Set Password in form
        result_flag = test_obj.set_password(password)
        test_obj.log_result(result_flag,
                            positive="Password was successfully set to: %s\n" % password,
                            negative="Failed to set password: %s \nOn url: %s\n" % (password, test_obj.get_current_url()))
        test_obj.write('Script duration: %d seconds\n' %
                       (int(time.time()-start_time)))
       
        
        #10. Set and submit the form in one go
        result_flag = test_obj.login()
        test_obj.log_result(result_flag,
                            positive="Successfully logged in the page\n",
                            negative="Failed to login the page \nOn url: %s" % test_obj.get_current_url(),
                            level="critical")


        #Turn off the highlighting feature
        #test_obj.turn_off_highlight()

        #Switching to Alert        
        Alert alert = driver.switchTo().alert();		
        		
        #Capturing alert message.    
        String alertMessage= driver.switchTo().alert().getText();		
        		
        # Displaying alert message		
        System.out.println(alertMessage);	
        Thread.sleep(5000);
        		
        # Accepting alert		
        alert.accept();		
     

        #13. Print out the result
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

        test_login_page(test_obj)
                
        #teardowm
        test_obj.wait(3)
        test_obj.teardown() 
    else:
        print('ERROR: Received incorrect comand line input arguments')
        print(option_obj.print_usage())
