"""The Qxf2 automation repository ships with example tests.
Run this file to delete all the example files and start fresh with your example.
After this script runs, you will need to edit a few files to configure them to suit your own repository
Usage: python clean_up_repo.py
"""
import os
REPO_DIR = os.path.dirname(os.path.dirname(__file__))
CONF_DIR = os.path.join(REPO_DIR, 'conf')
ENDPOINTS_DIR = os.path.join(REPO_DIR, 'endpoints')
PAGE_OBJECTS_DIR = os.path.join(REPO_DIR, 'page_objects')
TEST_DIR = os.path.join(REPO_DIR, 'tests')
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

def delete_file(filename):
    "Delete a file if it exists."
    if os.path.exists(filename):
        os.remove(filename)
        print("File deleted")
    else:
        print("File does not exist")

def delete_files_in_dir(directory, files):
    "Delete specific files in the directory."
    for filename in files:
        delete_file(os.path.join(directory,filename))

def delete_files_used_in_example():
    "Delete files used in example from the template."
    delete_files_in_dir(CONF_DIR, CONF_FILES_DELETE)
    delete_files_in_dir(ENDPOINTS_DIR, ENDPOINTS_FILES_DELETE)
    delete_files_in_dir(PAGE_OBJECTS_DIR, PAGE_OBJECTS_FILES_DELETE)
    delete_files_in_dir(TEST_DIR, TEST_FILES_DELETE)

#----START OF SCRIPT
if __name__ == "__main__":
    print("Running utility to delete the files")
    delete_files_used_in_example()   