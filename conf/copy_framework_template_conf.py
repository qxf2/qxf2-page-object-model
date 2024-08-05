"""
This conf file would have the relative paths of the files & folders.
"""
import os

#Files from src:
src_file1 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','__init__.py'))
src_file2 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','conftest.py'))
src_file3 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','Readme.md'))
src_file4 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','requirements.txt'))
src_file5 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','.gitignore'))
src_file6 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','env_conf'))
src_file7 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','env_remote'))
src_file8 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','env_ssh_conf'))
src_file9 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','pytest.ini'))

#src file list:
src_files_list = [src_file1,src_file2,src_file3,src_file4,src_file5,src_file6,src_file7,src_file8,
                  src_file9]

#CONF
#files from src conf:
src_conf_file1 = os.path.abspath(os.path.join(os.path.dirname(__file__),'testrail_caseid_conf.py'))
src_conf_file2 = os.path.abspath(os.path.join(os.path.dirname(__file__),'base_url_conf.py'))
src_conf_file3 = os.path.abspath(os.path.join(os.path.dirname(__file__),'browser_os_name_conf.py'))
src_conf_file4 = os.path.abspath(os.path.join(os.path.dirname(__file__),'clean_up_repo_conf.py'))
src_conf_file5 = os.path.abspath(os.path.join(os.path.dirname(__file__),'gpt_summarization_prompt.py'))
src_conf_file6 = os.path.abspath(os.path.join(os.path.dirname(__file__),'locators_conf.py'))
src_conf_file7 = os.path.abspath(os.path.join(os.path.dirname(__file__),'ports_conf.py'))
src_conf_file8 = os.path.abspath(os.path.join(os.path.dirname(__file__),'remote_url_conf.py'))
src_conf_file9 = os.path.abspath(os.path.join(os.path.dirname(__file__),'screenshot_conf.py'))
src_conf_file10 = os.path.abspath(os.path.join(os.path.dirname(__file__),'snapshot_dir_conf.py'))
src_conf_file11 = os.path.abspath(os.path.join(os.path.dirname(__file__),'__init__.py'))

#src Conf file list:
src_conf_files_list = [src_conf_file1,src_conf_file2,src_conf_file3,src_conf_file4,src_conf_file5,
                       src_conf_file6,src_conf_file7,src_conf_file8,src_conf_file9,src_conf_file10,
                       src_conf_file11]

#Page_Objects
#files from src page_objects:
src_page_objects_file1 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','page_objects','zero_page.py'))
src_page_objects_file2 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','page_objects','zero_mobile_page.py'))
src_page_objects_file3 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','page_objects','PageFactory.py'))
src_page_objects_file4 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','page_objects','__init__.py'))

#src page_objects file list:
src_page_objects_files_list = [src_page_objects_file1,src_page_objects_file2,src_page_objects_file3,src_page_objects_file4]

#tests
#files from tests:
src_tests_file1 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','tests','__init__.py'))
src_tests_file2 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','tests','test_boilerplate.py'))

#src tests file list:
src_tests_files_list = [src_tests_file1, src_tests_file2]
