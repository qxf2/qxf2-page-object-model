"""
The Qxf2 automation repository ships with example tests.
Run this file to delete all the example files and start fresh with your example.
Usage: python clean_up_repo.py
"""
import os
from .Base_Logging import Base_Logging

# Declaring directories as directory list
# dir_list : list
REPO_DIR = os.path.dirname(os.path.dirname(__file__))
CONF_DIR = os.path.join(REPO_DIR, 'conf')
ENDPOINTS_DIR = os.path.join(REPO_DIR, 'endpoints')
PAGE_OBJECTS_EXAMPLES_DIR = os.path.join(REPO_DIR, 'page_objects','examples')
TEST_DIR = os.path.join(REPO_DIR, 'tests')
DIR_LIST = [CONF_DIR, ENDPOINTS_DIR, TEST_DIR]

# Declaring files as file_list
# file_list : list
CONF_FILES_DELETE = ['api_example_conf.py',
    'cars_api_openapi_spec.json',
    'env_remote_enc',
    'example_form_conf.py',
    'example_table_conf.py',
    'mobile_bitcoin_conf.py',
    'mobile_weather_shopper_conf.py',
    'successive_form_creation_conf.py',
    'weather_shopper_mobile_conf.py']
ENDPOINTS_FILES_DELETE = ['cars_api_endpoints.py',
    'registration_api_endpoints.py',
    'user_api_endpoints.py']
TEST_FILES_DELETE = ['test_accessibility.py',
    'test_api_async_example.py',
    'test_api_endpoint_auto_generation.py',
    'test_example_table.py',
    'test_api_example.py',
    'test_mobile_bitcoin_price.py',
    'test_successive_form_creation.py',
    'test_example_form.py',
    'test_weather_shopper_app_menu_options.py',
    'test_weather_shopper_app.py',
    'test_weather_shopper_payment_app.py']

FILE_LIST = [CONF_FILES_DELETE, ENDPOINTS_FILES_DELETE, TEST_FILES_DELETE]

class CleanUpRepo:
    """Utility for cleaning up example files."""
    def __init__(self):
        """Initializes the CleanUpRepo class with a logger"""
        self.logger = Base_Logging(log_file_name="clean_up_repo.log", level="INFO")

    def delete_file(self, file_name):
        """The method will delete a particular file"""
        if os.path.exists(file_name):
            os.remove(file_name)
            self.logger.write(f'{file_name} deleted')

    def delete_directory(self, dir_name):
        """The method will delete a particular directory along with its content"""
        import shutil # pylint: disable=import-error,import-outside-toplevel
        if os.path.exists(dir_name) and os.path.isdir(dir_name):
            shutil.rmtree(dir_name)
            self.logger.write(f'{dir_name} deleted')

    def delete_files_in_dir(self, directory, files):
        """The method will delete files in a particular directory"""
        for file_name in files:
            self.delete_file(os.path.join(directory, file_name))

    def delete_files_used_in_example(self):
        """The method will delete a set of files"""
        for every_dir_list, every_file_list in zip(DIR_LIST, FILE_LIST):
            self.delete_files_in_dir(every_dir_list, every_file_list)

    def run_cleanup(self):
        """Runs the utility to delete example files and logs the operation."""
        self.logger.write("Running utility to delete the files")
        self.delete_directory(PAGE_OBJECTS_EXAMPLES_DIR)
        self.delete_files_used_in_example()
        self.logger.write(
            f'All the files related to the sample example from Page Object Model have been removed from {DIR_LIST} folders.\n'
            'For next steps, please refer to the edit files section of this blog post: '
            'https://qxf2.com/blog/how-to-start-using-the-qxf2-framework-with-a-new-project/'
        )

if __name__ == "__main__":
    cleanup = CleanUpRepo()
    cleanup.run_cleanup()
