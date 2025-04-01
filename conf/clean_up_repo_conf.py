"""
The file will have relative paths for dir and respective files which clean_up_repo.py will delete.
"""
import os

# Declaring directories as directory list
# dir_list : list
REPO_DIR = os.path.dirname(os.path.dirname(__file__))
CONF_DIR = os.path.join(REPO_DIR, 'conf')
ENDPOINTS_DIR = os.path.join(REPO_DIR, 'endpoints')
PAGE_OBJECTS_EXAMPLES_DIR = os.path.join(REPO_DIR, 'page_objects','examples')
TEST_DIR = os.path.join(REPO_DIR, 'tests')
dir_list = [CONF_DIR, ENDPOINTS_DIR, TEST_DIR]

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

file_list = [CONF_FILES_DELETE, ENDPOINTS_FILES_DELETE, TEST_FILES_DELETE]
