"""
The file will have relative paths for dir and respective files which clean_up_repo.py will delete.
"""
import os

# Declaring directories as directory list
# dir_list : list
REPO_DIR = os.path.dirname(os.path.dirname(__file__))
CONF_DIR = os.path.join(REPO_DIR, 'conf')
ENDPOINTS_DIR = os.path.join(REPO_DIR, 'endpoints')
PAGE_OBJECTS_DIR = os.path.join(REPO_DIR, 'page_objects')
TEST_DIR = os.path.join(REPO_DIR, 'tests')
dir_list = [CONF_DIR, ENDPOINTS_DIR, PAGE_OBJECTS_DIR, TEST_DIR]

# Declaring files as file_list
# file_list : list
CONF_FILES_DELETE = ['api_example_conf.py',
    'example_form_conf.py',
    'example_table_conf.py',
    'mobile_bitcoin_conf.py',
    'successive_form_creation_conf.py']
ENDPOINTS_FILES_DELETE = ['Cars_API_Endpoints.py',
    'Registration_API_Endpoints.py',
    'User_API_Endpoints.py']
PAGE_OBJECTS_FILES_DELETE = ['bitcoin_main_page.py',
    'bitcoin_price_page.py',
    'contact_form_object.py',
    'contact_page.py',
    'footer_object.py',
    'form_object.py',
    'header_object.py',
    'table_object.py',
    'tutorial_main_page.py',
    'tutorial_redirect_page.py',
    'hamburger_menu_object.py']
TEST_FILES_DELETE = ['test_example_table.py',
    'test_api_example.py',
    'test_mobile_bitcoin_price.py',
    'test_successive_form_creation.py',
    'test_example_form.py']

file_list = [CONF_FILES_DELETE, ENDPOINTS_FILES_DELETE, PAGE_OBJECTS_FILES_DELETE, TEST_FILES_DELETE]