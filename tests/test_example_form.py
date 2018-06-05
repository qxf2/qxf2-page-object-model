"""
This is an example automated test to help you learn Qxf2's framework
Our automated test will do the following:
    #Open Qxf2 selenium-tutorial-main page.
    #Fill the example form.
    #Click on Click me! button and check if its working fine.
"""

#The import statements import: standard Python modules,conf,credential files
import os,sys,time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from page_objects.PageFactory import PageFactory
from utils.Option_Parser import Option_Parser
import conf.example_form_conf as conf
import conf.testrail_caseid_conf as testrail_file


def test_example_form(base_url,browser,browser_version,os_version,os_name,remote_flag,testrail_flag,test_run_id):
    "Run the test"
    try:
	#Initalize flags for tests summary
        expected_pass = 0
        actual_pass = -1

        #1. Create a test object and fill the example form.
        test_obj = PageFactory.get_page_object("Main Page",base_url=base_url)

        #2. Setup and register a driver
        start_time = int(time.time())	#Set start_time with current time
        test_obj.register_driver(remote_flag,os_name,os_version,browser,browser_version)
        
        #3. Setup TestRail reporting
        if testrail_flag.lower()=='y':
            if test_run_id is None:
                test_obj.write('\033[91m'+"\n\nTestRail Integration Exception: It looks like you are trying to use TestRail Integration without providing test run id. \nPlease provide a valid test run id along with test run command using -R flag and try again. for eg: pytest -X Y -R 100\n"+'\033[0m')
                testrail_flag = 'N'   
            if test_run_id is not None:
                test_obj.register_testrail()
        
        #4. Get the test details from the conf file
        name = conf.name
        email = conf.email
        phone = conf.phone_no
        gender = conf.gender
 
        #5. Set name in form
        result_flag = test_obj.set_name(name) 
        test_obj.log_result(result_flag,
                            positive="Name was successfully set to: %s\n"%name,
                            negative="Failed to set name: %s \nOn url: %s\n"%(name,test_obj.get_current_url()))
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
        #Update TestRail
        case_id = testrail_file.test_example_form_name
        test_obj.report_to_testrail(case_id,test_run_id,result_flag)
        
        #6. Set Email in form
        result_flag = test_obj.set_email(email) 
        test_obj.log_result(result_flag,
                            positive="Email was successfully set to: %s\n"%email,
                            negative="Failed to set Email: %s \nOn url: %s\n"%(email,test_obj.get_current_url()))
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
        #Update TestRail
        case_id = testrail_file.test_example_form_email
        test_obj.report_to_testrail(case_id,test_run_id,result_flag)
        
        #7. Set Phone number in form
        result_flag = test_obj.set_phone(phone)
        test_obj.log_result(result_flag,
                            positive="Phone number was successfully set for phone: %s\n"%phone,
                            negative="Failed to set phone number: %s \nOn url: %s\n"%(phone,test_obj.get_current_url()))
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
        #Update TestRail
        case_id = testrail_file.test_example_form_phone
        test_obj.report_to_testrail(case_id,test_run_id,result_flag)
        
        #8. Set Gender in form
        result_flag = test_obj.set_gender(gender)
        test_obj.log_result(result_flag,
                            positive= "Gender was successfully set to: %s\n"%gender,
                            negative="Failed to set gender: %s \nOn url: %s\n"%(gender,test_obj.get_current_url()))
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
        #Update TestRail
        case_id = testrail_file.test_example_form_gender
        test_obj.report_to_testrail(case_id,test_run_id,result_flag)
        
        #9. Check the copyright
        result_flag = test_obj.check_copyright()
        test_obj.log_result(result_flag,
                            positive="Copyright check was successful\n",
                            negative="Copyright looks wrong.\nObtained the copyright%s\n"%test_obj.get_copyright())
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
        
        #10. Set and submit the form in one go
        
        result_flag = test_obj.submit_form(name,email,phone,gender)
        test_obj.log_result(result_flag,
                            positive="Successfully submitted the form\n",
                            negative="Failed to submit the form \nOn url: %s"%test_obj.get_current_url())
                            
        #Update TestRail
        case_id = testrail_file.test_example_form
        test_obj.report_to_testrail(case_id,test_run_id,result_flag)
        
        #11. Check the heading on the redirect page
        #Notice you don't need to create a new page object!
        if result_flag is True:
            result_flag = test_obj.check_heading()
        test_obj.log_result(result_flag,
                            positive="Heading on the redirect page checks out!\n",
                            negative="Fail: Heading on the redirect page is incorrect!")
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))

        #12. Visit the contact page and verify the link
        result_flag = test_obj.goto_footer_link('Contact > Get in touch!','contact')    
        test_obj.log_result(result_flag,
                            positive="Successfully visited the Contact page\n",
                            negative="\nFailed to visit the Contact page\n")
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
        #Update TestRail
        case_id = testrail_file.test_example_form_footer_contact
        test_obj.report_to_testrail(case_id,test_run_id,result_flag)
        
        #13. Print out the results
        test_obj.write_test_summary()

        #Teardown
        test_obj.wait(3)
        expected_pass = test_obj.result_counter
        actual_pass = test_obj.pass_counter
        test_obj.teardown() 
        
    except Exception,e:
        print "Exception when trying to run test:%s"%__file__
        print "Python says:%s"%str(e)

    assert expected_pass == actual_pass, "Test failed: %s"%__file__
       
    
#---START OF SCRIPT   
if __name__=='__main__':
    print "Start of %s"%__file__
    #Creating an instance of the class
    options_obj = Option_Parser()
    options = options_obj.get_options()
                
    #Run the test only if the options provided are valid
    if options_obj.check_options(options): 
        test_example_form(base_url=options.url,
                        browser=options.browser,
                        browser_version=options.browser_version,
                        os_version=options.os_version,
                        os_name=options.os_name,
                        remote_flag=options.remote_flag,
                        testrail_flag=options.testrail_flag,
                        test_run_id=options.test_run_id) 
    else:
        print 'ERROR: Received incorrect comand line input arguments'
        print option_obj.print_usage()
