"""
This conf file would have the relative paths of the files & folders.
"""
import os,sys

#Files from src:
src_file1 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','__init__.py'))
src_file2 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','conftest.py'))
src_file3 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','Readme.md'))
src_file4 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','Requirements.txt'))

#src file list:
src_files_list = [src_file1,src_file2,src_file3,src_file4]

#conf
#files from src conf:
src_conf_file1 = os.path.abspath(os.path.join(os.path.dirname(__file__),'testrailenv_conf.py'))
src_conf_file2 = os.path.abspath(os.path.join(os.path.dirname(__file__),'remote_credentials.py'))
src_conf_file3 = os.path.abspath(os.path.join(os.path.dirname(__file__),'browser_os_name_conf.py'))
src_conf_file4 = os.path.abspath(os.path.join(os.path.dirname(__file__),'__init__.py'))
src_conf_file5 = os.path.abspath(os.path.join(os.path.dirname(__file__),'locators_conf_template.py'))
src_conf_file6 = os.path.abspath(os.path.join(os.path.dirname(__file__),'opera_browser_conf.py'))

#src conf file list:
src_conf_files_list = [src_conf_file1,src_conf_file2,src_conf_file3,src_conf_file4,src_conf_file5,src_conf_file6]

#files from src page_objects:
src_page_objects_file1 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','page_objects','Base_Page.py'))
src_page_objects_file2 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','page_objects','DriverFactory.py'))
src_page_objects_file3 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','page_objects','PageFactory_template.py'))
src_page_objects_file4 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','page_objects','__init__.py'))
src_page_objects_file5 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','page_objects','main_page_template.py'))
src_page_objects_file6 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','page_objects','page_object_template.py'))


#src page_objects file list:
src_page_objects_files_list = [src_page_objects_file1,src_page_objects_file2,src_page_objects_file4,src_page_objects_file5,src_page_objects_file6]

#Utils
src_folder_utils = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','utils'))

#files from src Utils:
src_utils_file1 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','utils','Base_Logging.py'))
src_utils_file2 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','utils','BrowserStack_Library.py'))
src_utils_file3 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','utils','Option_Parser.py'))
src_utils_file4 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','utils','setup_testrail.py'))
src_utils_file5 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','utils','Test_Rail.py'))
src_utils_file6 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','utils','Test_Runner_Class.py'))
src_utils_file7 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','utils','testrail.py'))
src_utils_file8 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','utils','Wrapit.py'))
src_utils_file9 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','utils','__init__.py'))
src_utils_file10 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','utils','Tesults.py'))

#src utils file list:
src_utils_files_list = [src_utils_file1,src_utils_file2,src_utils_file3,src_utils_file4,src_utils_file5,src_utils_file6,src_utils_file7,src_utils_file8,src_utils_file9,src_utils_file10]

#files from src tests:
src_tests_file1 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','tests','test_boilerplate.py'))
src_tests_file2 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','utils','__init__.py'))

#src tests file list:
src_tests_files_list = [src_tests_file1,src_tests_file2]