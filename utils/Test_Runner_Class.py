"""
Test Runner class. Lets you setup testrail and run a bunch of tests one after the other
"""

import os,subprocess

class Test_Runner_Class:
    "Test Runner class"
    def __init__(self,base_url='http://qxf2.com',testrail_flag='N',browserstack_flag='N',os_name='Windows',os_version='7',browser='firefox',browser_version='33'):
        "Constructor"
        self.python_executable = "python"
        self.util_directory = os.path.abspath((os.path.dirname(__file__)))
        self.test_directory = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','tests'))
        self.setup_testrail_script = os.path.join(self.util_directory,"setup_testrail.py")
        self.reset(base_url=base_url,
                   testrail_flag=testrail_flag,
                   browserstack_flag=browserstack_flag,
                   os_name=os_name,
                   os_version=os_version,
                   browser=browser,
                   browser_version=browser_version)

    def check_file_exists(self,file_path):
        "Check if the config file exists and is a file"
        file_exist_flag = True
        if os.path.exists(file_path):
            if not os.path.isfile(file_path):
                print('\n****')
                print('Script file provided is not a file: ')
                print(file_path)
                print('****')
                file_exist_flag = False
        else:
            print('\n****')
            print('Unable to locate the provided script file: ')
            print(file_path)
            print('****')
            conf_flag = False

        return file_exist_flag


    def reset(self,base_url=None,testrail_flag=None,browserstack_flag=None,os_name=None,os_version=None,browser=None,browser_version=None):
        "Reset the private variables"
        if base_url is not None:
            self.base_url = base_url
        if testrail_flag is not None:
            self.testrail_flag = testrail_flag
        if browserstack_flag is not None:
            self.browserstack_flag = browserstack_flag
        if os_name is not None:
            self.os_name = os_name
        if os_version is not None:
            self.os_version = os_version
        if browser is not None:
            self.browser = browser
        if browser_version is not None:
            self.browser_version = browser_version



    def run_test(self,test_name):
        "Run the test script with the given command line options"
        testscript_args_list = self.setup_test_script_args_list(test_name)
        self.run_script(testscript_args_list)


    def run_setup_testrail(self,test_name=None,test_run_name='',case_ids_list=None,name_override_flag=True):
        "Run the setup_testrail with given command line options"
        if self.testrail_flag.lower() == 'y':
            testrail_args_list = self.setup_testrail_args_list(test_name,test_run_name,case_ids_list,name_override_flag)
            self.run_script(testrail_args_list)


    def run_script(self,args_list):
        "Run the script on command line with given args_list"
        print("\nWill be running the following script:")
        print(' '.join(args_list))
        print("Starting..")
        subprocess.call(args_list,shell=True)
        print("Done!")


    def setup_testrail_args_list(self,test_name=None,test_run_name='',case_ids_list=None,name_override_flag=True):
        "Convert the command line arguments into list for setup_testrail.py"
        args_list = []
        #python setup_testrail.py -r test_run_name -d test_run_description
        if self.check_file_exists(self.setup_testrail_script):
            args_list = [self.python_executable,self.setup_testrail_script]
            if test_run_name != '':
                args_list.append("-r")
                args_list.append(test_run_name)
            if test_name is not None:
                args_list.append("-d")
                args_list.append(test_name)
            if name_override_flag is False:
                args_list.append("-n")
                args_list.append("N")
            if case_ids_list is not None:
                args_list.append("-c")
                case_ids_list = ','.join(case_ids_list)
                args_list.append(case_ids_list)

        return args_list


    def setup_test_script_args_list(self,test_name):
        "convert the command line arguments into list for test script"
        args_list = []
        #python test_script.py -x Y
        test_script_name = test_name + ".py"
        test_script_name = os.path.join(self.test_directory,test_script_name)
        if self.check_file_exists(test_script_name):
            args_list = [self.python_executable,test_script_name,"-b",self.browser,"-u",self.base_url,"-x",self.testrail_flag,"-s",self.browserstack_flag,"-o",self.os_version,"-v",self.browser_version,"-p",self.os_name]

        return args_list





