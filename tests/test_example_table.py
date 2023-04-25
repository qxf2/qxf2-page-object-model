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
        test_obj = PageFactory.get_page_object("Main Page", base_url=test_obj.base_url)

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
