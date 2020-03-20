"""
This is an example automated test to help you learn Qxf2's framework
Our automated test will do the following:
    #Open Qxf2 selenium-tutorial-main page.
    #Print out the entire table 
    #Verify if a certain name is present in the table
"""

#The import statements import: standard Python modules,conf,credential files
import os,sys,time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from page_objects.PageFactory import PageFactory
from utils.Option_Parser import Option_Parser
import conf.example_table_conf as conf
import conf.testrail_caseid_conf as testrail_file
import pytest


@pytest.mark.GUI
def test_example_table(test_obj):

    "Run the test"
    try:
        #Initalize flags for tests summary
        expected_pass = 0
        actual_pass = -1
        
        #1. Create a example table page object
        test_obj = PageFactory.get_page_object("Main Page")    

        #Set start_time with current time
        start_time = int(time.time())	

        #2. Get the test details from the conf file
        name = conf.name

        #3. Print out table text neatly
        result_flag = test_obj.print_table_text()
        test_obj.log_result(result_flag,
                            positive="Completed printing table text",
                            negative="Unable to print the table text")
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
        
        #4. Check if a name is present in the table
        result_flag = test_obj.check_name_present(name)
        test_obj.log_result(result_flag,
                            positive="Located the name %s in the table"%name,
                            negative="The name %s is not present under name column on the Page with url: %s"%(name,test_obj.get_current_url()))
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
        #Update TestRail
        case_id = testrail_file.test_example_table
        test_obj.report_to_testrail(case_id,test_obj.test_run_id,result_flag)
        test_obj.add_tesults_case("Example table", "Verify if a certain name is present in the table", "test_example_table", result_flag,"\nFailed to Verify if a certain name is present in the table\n")
     
        #5. Print out the result
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
    options=options_obj.get_options()
                        
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
        
        test_example_table(test_obj) 
        
        #teardowm
        test_obj.wait(3)
        test_obj.teardown()

    else:
        print('ERROR: Received incorrect input arguments')
        print(options_obj.print_usage())
