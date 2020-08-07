"""
This conf file would have the relative paths of the files & folders.
"""
import os

#dst_folder will be Myntra
#Files from src:
src_file1 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','__init__.py'))
src_file2 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','conftest.py'))
src_file3 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','Readme.md'))
src_file4 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','Requirements.txt'))
src_file5 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','setup.cfg'))

#src file list:
src_files_list = [src_file1,src_file2,src_file3,src_file4,src_file5]

#destination folder for which user has to mention. This folder should be created by user.
#dst_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..','clients','Myntra'))

#CONF
#files from src conf:
src_conf_file1 = os.path.abspath(os.path.join(os.path.dirname(__file__),'testrailenv_conf.py'))
src_conf_file2 = os.path.abspath(os.path.join(os.path.dirname(__file__),'remote_credentials.py'))
src_conf_file3 = os.path.abspath(os.path.join(os.path.dirname(__file__),'browser_os_name_conf.py'))
src_conf_file4 = os.path.abspath(os.path.join(os.path.dirname(__file__),'__init__.py'))

#src Conf file list:
src_conf_files_list = [src_conf_file1,src_conf_file2,src_conf_file3,src_conf_file4]

#destination folder for conf:
dst_folder_conf = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..','clients','Myntra','conf'))

#Page_Objects
#files from src page_objects:
src_page_objects_file1 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','page_objects','Base_Page.py'))
src_page_objects_file2 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','page_objects','DriverFactory.py'))
src_page_objects_file3 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','page_objects','PageFactory.py'))
src_page_objects_file4 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','page_objects','__init__.py'))

#src page_objects file list:
src_page_objects_files_list = [src_page_objects_file1,src_page_objects_file2,src_page_objects_file3,src_page_objects_file4]

#destination folder for page_objects:
dst_folder_page_objects = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..','clients','Myntra','page_objects'))

#Utils

src_folder_utils = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','utils'))
dst_folder_utils = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..','clients','Myntra','utils'))

#files from src Utils:
src_utils_file1 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','utils','Base_Logging.py'))
src_utils_file2 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','utils','BrowserStack_Library.py'))
src_utils_file3 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','utils','Option_Parser.py'))
src_utils_file4 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','utils','setup_testrail.py'))
src_utils_file5 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','utils','Test_Rail.py'))
src_utils_file6 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','utils','testrail.py'))
src_utils_file7 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','utils','Wrapit.py'))

#files for dst Utils:
#dst_utils_file1 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..','clients','Myntra','utils','Base_Logging.py'))
#dst_utils_file2 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..','clients','Myntra','utils','BrowserStack_Library.py'))
#dst_utils_file3 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..','clients','Myntra','utils','Option_Parser.py'))
#dst_utils_file4 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..','clients','Myntra','utils','setup_testrail.py'))
#dst_utils_file5 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..','clients','Myntra','utils','Test_Rail.py'))
#dst_utils_file6 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..','clients','Myntra','utils','Test_Runner_Class.py'))
#dst_utils_file7 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..','clients','Myntra','utils','testrail.py'))
#dst_utils_file8 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..','clients','Myntra','utils','Wrapit.py'))

#src utils file list:
src_utils_files_list = [src_utils_file1,src_utils_file2,src_utils_file3,src_utils_file4,src_utils_file5,src_utils_file6,src_utils_file7]

#dst utils file list:
#dst_utils_files_list = [dst_utils_file1,dst_utils_file2,dst_utils_file3,dst_utils_file4,dst_utils_file5,dst_utils_file6,dst_utils_file7,dst_utils_file8]


