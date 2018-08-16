"""
One off utility script to setup TestRail for an automated run
This script can:
a) Add a milestone if it does not exist
b) Add a test run (even without a milestone if needed)
c) Add select test cases to the test run using the setup_testrail.conf file
d) Write out the latest run id to a 'latest_test_run.txt' file

This script will NOT:
a) Add a project if it does not exist
"""

import os,ConfigParser,time
from .Test_Rail import Test_Rail
from optparse import OptionParser


def check_file_exists(file_path):
    #Check if the config file exists and is a file
    conf_flag = True
    if os.path.exists(file_path):
        if not os.path.isfile(file_path):
            print('\n****')
            print('Config file provided is not a file: ')
            print(file_path)
            print('****')
            conf_flag = False
    else:
        print('\n****')
        print('Unable to locate the provided config file: ')
        print(file_path)
        print('****')
        conf_flag = False

    return conf_flag


def check_options(options):
    "Check if the command line options are valid"
    result_flag = True
    if options.test_cases_conf is not None:
        result_flag = check_file_exists(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','conf',options.test_cases_conf)))

    return result_flag


def save_new_test_run_details(filename,test_run_name,test_run_id):
    "Write out latest test run name and id"
    fp = open(filename,'w')
    fp.write('TEST_RUN_NAME=%s\n'%test_run_name)
    fp.write('TEST_RUN_ID=%s\n'%str(test_run_id))
    fp.close()


def setup_testrail(project_name='POM DEMO',milestone_name=None,test_run_name=None,test_cases_conf=None,description=None,name_override_flag='N',case_ids_list=None):
    "Setup TestRail for an automated run"
    #1. Get project id
    #2. if milestone_name is not None 
    #   create the milestone if it does not already exist
    #3. if test_run_name is not None
    #   create the test run if it does not already exist
    #      TO DO: if test_cases_conf is not None -> pass ids as parameters
    #4. write out test runid to latest_test_run.txt
    conf_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','conf'))
    config = ConfigParser.ConfigParser()
    tr_obj = Test_Rail()
    #1. Get project id
    project_id = tr_obj.get_project_id(project_name)

    if project_id is not None: #i.e., the project exists
        #2. if milestone_name is not None:
        #   create the milestone if it does not already exist
        if milestone_name is not None:
            tr_obj.create_milestone(project_name,milestone_name)

        #3. if test_run_name is not None
        #   create the test run if it does not already exist
        #      if test_cases_conf is not None -> pass ids as parameters
        if test_run_name is not None:
            case_ids = []
            #Set the case ids
            if case_ids_list is not None:
                #Getting case ids from command line
                case_ids = case_ids_list.split(',')
            else:
                #Getting case ids based on given description(test name)
                if description is not None:
                    if check_file_exists(os.path.join(conf_dir,test_cases_conf)):
                        config.read(os.path.join(conf_dir,test_cases_conf))
                        case_ids = config.get(description,'case_ids')
                        case_ids = case_ids.split(',')
            #Set test_run_name
            if name_override_flag.lower() == 'y':
                test_run_name =  test_run_name + "-" + time.strftime("%d/%m/%Y/%H:%M:%S") + "_for_"
                #Use description as test_run_name
                if description is None:
                    test_run_name =  test_run_name +  "All"
                else:
                    test_run_name = test_run_name + str(description)
            tr_obj.create_test_run(project_name,test_run_name,milestone_name=milestone_name,case_ids=case_ids,description=description)
            run_id = tr_obj.get_run_id(project_name,test_run_name)
            save_new_test_run_details(os.path.join(conf_dir,'latest_test_run.txt'),test_run_name,run_id)
    else:
        print('Project does not exist: ',project_name)
        print('Stopping the script without doing anything.')



#---START OF SCRIPT
if __name__=='__main__':
    #This script takes an optional command line argument for the TestRail run id
    usage = '\n----\n%prog -p <OPTIONAL: Project name> -m <OPTIONAL: milestone_name> -r <OPTIONAL: Test run name> -t <OPTIONAL: test cases conf file> -d <OPTIONAL: Test run description>\n----\nE.g.: %prog -p "Secure Code Warrior - Test" -m "Pilot NetCetera" -r commit_id -t setup_testrail.conf -d Registration\n---'
    parser = OptionParser(usage=usage)

    parser.add_option("-p","--project",
                      dest="project_name",
                      default="POM DEMO",
                      help="Project name")
    parser.add_option("-m","--milestone",
                      dest="milestone_name",
                      default=None,
                      help="Milestone name")
    parser.add_option("-r","--test_run_name",
                      dest="test_run_name",
                      default=None,
                      help="Test run name")
    parser.add_option("-t","--test_cases_conf",
                      dest="test_cases_conf",
                      default="setup_testrail.conf",
                      help="Test cases conf listing test names and ids you want added")
    parser.add_option("-d","--test_run_description",
                      dest="test_run_description",
                      default=None,
                      help="The name of the test Registration_Tests/Intro_Run_Tests/Sales_Demo_Tests")
    parser.add_option("-n","--name_override_flag",
                      dest="name_override_flag",
                      default="Y",
                      help="Y or N. 'N' if you don't want to override the default test_run_name")
    parser.add_option("-c","--case_ids_list",
                      dest="case_ids_list",
                      default=None,
                      help="Pass all case ids with comma separated you want to add in test run")
    
    (options,args) = parser.parse_args()

    #Run the script only if the options are valid
    if check_options(options):
        setup_testrail(project_name=options.project_name,
                       milestone_name=options.milestone_name,
                       test_run_name=options.test_run_name,
                       test_cases_conf=options.test_cases_conf,
                       description=options.test_run_description,
                       name_override_flag=options.name_override_flag,
                       case_ids_list=options.case_ids_list)
    else:
        print('ERROR: Received incorrect input arguments')
        print(parser.print_usage())
        
