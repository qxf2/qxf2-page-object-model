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


def test_example_table(base_url,browser,browser_version,os_version,os_name,remote_flag,testrail_flag,test_run_id):
    "Run the test"
    try:
	#Initalize flags for tests summary
        expected_pass = 0
        actual_pass = -1

        #1. Create a example table page object
        test_obj = PageFactory.get_page_object("Main Page",base_url=base_url)    

        #2. Setup and register a driver
        start_time = int(time.time())	#Set start_time with current time
        test_obj.register_driver(remote_flag,os_name,os_version,browser,browser_version)

        #3. Setup TestRail reporting
        if testrail_flag.lower()=='y':
            if test_run_id is None:
                default_test_run_file = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','conf','latest_test_run.txt'))
                test_run_id = Conf_Reader.get_value(default_test_run_file,'TEST_RUN_ID')
            if test_run_id is not None:
                test_obj.register_testrail()

        #4. Get the test details from the conf file
        name = conf.name

        #5. Print out table text neatly
        test_obj.print_table_text()

        #6. Check if a name is present in the table
        result_flag = test_obj.check_name_present(name)
        test_obj.log_result(result_flag,
                            positive="Located the name %s in the table"%name,
                            negative="The name %s is not present under name column on the Page with url: %s"%(name,test_obj.get_current_url()))
        test_obj.write('Script duration: %d seconds\n'%(int(time.time()-start_time)))
        #Update TestRail
        case_id = testrail_file.test_example_table
        test_obj.report_to_testrail(case_id,test_run_id,result_flag)

        #7. Print out the result
        test_obj.write_test_summary()

        #Teardown
        test_obj.wait(3)
        expected_pass = test_obj.result_counter
        actual_pass = test_obj.pass_counter
        test_obj.teardown() 
    
    except Exception,e:
        print "Exception when trying to run test: %s"%__file__
        print "Python says:%s"%str(e)

    assert expected_pass == actual_pass   
    

#---START OF SCRIPT
if __name__=='__main__':
    print "Start of %s"%__file__
    #Creating an instance of the class
    options_obj = Option_Parser()
    options=options_obj.get_options()
                        
    if options_obj.check_options(options): 
        #Run the test only if the options provided are valid
        test_example_table(browser=options.browser,
                    base_url=options.url,
                    test_run_id=options.test_run_id,
                    testrail_flag=options.testrail_flag,
                    remote_flag=options.remote_flag,
                    os_version=options.os_version,
                    browser_version=options.browser_version,
                    os_name=options.os_name)
    else:
        print 'ERROR: Received incorrect input arguments'
        print options_obj.print_usage()
