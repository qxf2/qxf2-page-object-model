"""
This is an example automated test to help you learn Qxf2's framework
Our automated test will do the following action repeatedly to fill number of forms:
    #Open Qxf2 selenium-tutorial-main page.
    #Fill the example form
    #Click on Click me! button and check if its working fine
"""
#The import statements import: standard Python modules,conf,credential files
import os,sys,time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from page_objects.PageFactory import PageFactory
from utils.Option_Parser import Option_Parser
import conf.successive_form_creation_conf as conf

def test_succesive_form_creation(base_url,browser,browser_version,os_version,os_name,remote_flag,testrail_flag,tesults_flag,test_run_id,remote_project_name,remote_build_name):
    "Run the test"
    try:
	#Initalize flags for tests summary
        expected_pass = 0
        actual_pass = -1

        #1. Create a test object and fill the example form.
        test_obj = PageFactory.get_page_object("Main Page",base_url=base_url)

        #2. Setup and register a driver
        start_time = int(time.time())	#Set start_time with current time
        test_obj.register_driver(remote_flag,os_name,os_version,browser,browser_version,remote_project_name,remote_build_name)

        #3. Setup TestRail reporting
        if testrail_flag.lower()=='y':
            if test_run_id is None:
                test_obj.write('\033[91m'+"\n\nTestRail Integration Exception: It looks like you are trying to use TestRail Integration without providing test run id. \nPlease provide a valid test run id along with test run command using -R flag and try again. for eg: pytest -X Y -R 100\n"+'\033[0m')
                testrail_flag = 'N'   
            if test_run_id is not None:
                test_obj.register_testrail()
        
        if tesults_flag.lower()=='y':
            test_obj.register_tesults()
        
        #4. Get the test details from the conf file and fill the forms
        form_list = conf.form_list
        form_number = 1		#Initalize form counter
    
        # Collect form data
        for form in form_list:      
            name = form['NAME']
            email = form['EMAIL']
            phone = form['PHONE_NO']
            gender = form['GENDER']
    
            msg ="\nReady to fill form number %d"%form_number
            test_obj.write(msg)

            #a. Set and submit the form in one go
            result_flag = test_obj.submit_form(name,email,phone,gender)
            test_obj.log_result(result_flag,
                                positive="Successfully submitted the form number %d\n"%form_number,
                                negative="Failed to submit the form number %d \nOn url: %s"%(form_number,test_obj.get_current_url()),
                                level="critical")
            test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
            test_obj.add_tesults_case("Set and submit form " + str(form_number), "Sets and submits the form in one go", "test_successive_form_creation", result_flag, "Failed to submit the form number %d \nOn url: %s"%(form_number,test_obj.get_current_url()), [test_obj.log_obj.log_file_dir + os.sep + test_obj.log_obj.log_file_name])

            #b. Check the heading on the redirect page
            #Notice you don't need to create a new page object!
            if result_flag is True:
                result_flag = test_obj.check_heading()
            test_obj.log_result(result_flag,
                                positive="Heading on the redirect page checks out!\n",
                                negative="Fail: Heading on the redirect page is incorrect!")
            test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
            test_obj.add_tesults_case("Check redirect heading "  + str(form_number), "Check the heading on the redirect page", "test_successive_form_creation", result_flag, "Fail: Heading on the redirect page is incorrect!", [])

            #c. Check the copyright
            result_flag = test_obj.check_copyright() 
            test_obj.log_result(result_flag,
                                positive="Copyright check was successful\n",
                                negative="Copyright looks wrong.\nObtained the copyright: %s\n"%test_obj.get_copyright())
            test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
            test_obj.add_tesults_case("Check copyright "  + str(form_number), "Check the copyright", "test_successive_form_creation", result_flag, "Copyright looks wrong.\nObtained the copyright: %s\n"%test_obj.get_copyright(), [])

            #d. Visit main page again
            test_obj = PageFactory.get_page_object("Main Page",base_url=base_url)
            form_number = form_number + 1
            
        #5. Print out the results
        test_obj.write_test_summary()

        #Teardown
        test_obj.wait(3)
        expected_pass = test_obj.result_counter
        actual_pass = test_obj.pass_counter
        test_obj.teardown()

    except Exception as e:
        print("Exception when trying to run test :%s"%__file__)
        print("Python says:%s"%str(e))
     
    assert expected_pass == actual_pass ,"Test failed: %s"%__file__

    
#---START OF SCRIPT

if __name__=='__main__':
    print("Start of %s"%__file__)
    #Creating an instance of the class
    options_obj = Option_Parser()
    options=options_obj.get_options()

    #Run the test only if the options provided are valid
    if options_obj.check_options(options): 
        test_succesive_form_creation(base_url=options.url,
                                    browser=options.browser,
                                    browser_version=options.browser_version,
                                    os_version=options.os_version,
                                    os_name=options.os_name,
                                    remote_flag=options.remote_flag,
                                    testrail_flag=options.testrail_flag,
                                    tesults_flag=options.tesults_flag,
                                    test_run_id=options.test_run_id,
                                    remote_project_name=options.remote_project_name,
                                    remote_build_name=options.remote_build_name)                                    
    else:
        print('ERROR: Received incorrect comand line input arguments')
        print(options_obj.print_usage())
