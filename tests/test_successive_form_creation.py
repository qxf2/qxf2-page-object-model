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
import conf.successive_form_creation_conf as conf
import conf.testrail_caseid_conf as testrail_file
import pytest
@pytest.mark.GUI

def test_succesive_form_creation(test_obj):
    "Run the test"
    try:
	#Initalize flags for tests summary
        expected_pass = 0
        actual_pass = -1

        #1. Create a test object and fill the example form.
        test_obj = PageFactory.get_page_object("Main Page", base_url=test_obj.base_url)

        #Set start_time with current time
        start_time = int(time.time())

        #2. Get the test details from the conf file and fill the forms
        form_list = conf.form_list
        form_number = 1		#Initalize form counter

        #3.Collect form data
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
            #Update TestRail
            case_id = testrail_file.test_successive_form_creation
            test_obj.report_to_testrail(case_id,test_obj.test_run_id,result_flag)
            test_obj.add_tesults_case("Set and submit form " + str(form_number), "Sets and submits the form in one go", "test_successive_form_creation", result_flag, "Failed to submit the form number %d \nOn url: %s"%(form_number,test_obj.get_current_url()), [test_obj.log_obj.log_file_dir + os.sep + test_obj.log_obj.log_file_name])

            #b. Check the heading on the redirect page
            #Notice you don't need to create a new page object!
            if result_flag is True:
                result_flag = test_obj.check_heading()
            test_obj.log_result(result_flag,
                                positive="Heading on the redirect page checks out!\n",
                                negative="Fail: Heading on the redirect page is incorrect!")
            test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
            case_id = testrail_file.test_successive_form_creation
            test_obj.report_to_testrail(case_id,test_obj.test_run_id,result_flag)
            test_obj.add_tesults_case("Check redirect heading "  + str(form_number), "Check the heading on the redirect page", "test_successive_form_creation", result_flag, "Fail: Heading on the redirect page is incorrect!", [])

            #c. Check the copyright
            result_flag = test_obj.check_copyright()
            test_obj.log_result(result_flag,
                                positive="Copyright check was successful\n",
                                negative="Copyright looks wrong.\nObtained the copyright: %s\n"%test_obj.get_copyright())
            test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
            case_id = testrail_file.test_successive_form_creation
            test_obj.report_to_testrail(case_id,test_obj.test_run_id,result_flag)
            test_obj.add_tesults_case("Check copyright "  + str(form_number), "Check the copyright", "test_successive_form_creation", result_flag, "Copyright looks wrong.\nObtained the copyright: %s\n"%test_obj.get_copyright(), [])

            #d. Visit main page again
            test_obj = PageFactory.get_page_object("Main Page", base_url=test_obj.base_url)
            form_number = form_number + 1

        #4.Print out the results
        test_obj.write_test_summary()
        expected_pass = test_obj.result_counter
        actual_pass = test_obj.pass_counter

    except Exception as e:
        print("Exception when trying to run test :%s"%__file__)
        print("Python says:%s"%str(e))

    assert expected_pass == actual_pass ,"Test failed: %s"%__file__
