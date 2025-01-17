import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_auto_generator.endpoint_name_generator import NameGenerator
from api_auto_generator.openapi_spec_parser import OpenAPISpecParser
from loguru import logger

@pytest.fixture
def name_generator():
	return NameGenerator(endpoint_url="/cars/{name}",
					  	if_query_param=False,
						path_params=[('name', 'str')],
						requestbody_type=None)

@pytest.fixture
def openapi_spec_parser():
	return OpenAPISpecParser("conf/cars_api_openapi_spec.json", logger)

@pytest.mark.API_AUTO_GEN_UNIT
def test_module_name_generation(name_generator):
	assert name_generator.module_name == "cars_endpoint"

@pytest.mark.API_AUTO_GEN_UNIT
def test_class_name_generation(name_generator):
	assert name_generator.class_name == "CarsEndpoint"

@pytest.mark.API_AUTO_GEN_UNIT
def test_url_method_name(name_generator):
	assert name_generator.url_method_name == "cars_url"

@pytest.mark.API_AUTO_GEN_UNIT
def test_base_api_param_string(name_generator):
	assert name_generator.base_api_param_string == ", headers=headers"

@pytest.mark.API_AUTO_GEN_UNIT
def test_instance_method_param_string(name_generator):
	assert name_generator.instance_method_param_string == "self, name, headers"

@pytest.mark.API_AUTO_GEN_UNIT
def test_openapiv3_spec_parser(openapi_spec_parser):
	assert openapi_spec_parser.parsed_dict == {'cars_endpoint': {'CarsEndpoint': {'instance_methods': [{'get_cars': {'params': {'query_params': [], 'path_params': []}, 'base_api_param_string': ', headers=headers', 'instance_method_param_string': 'self, headers', 'http_method': 'get', 'endpoint': '/cars'}}, {'post_cars_add': {'params': {'query_params': [], 'path_params': [], 'json_params': [('name', 'str'), ('brand', 'str'), ('price_range', 'str'), ('car_type', 'str')], 'content_schema_type': 'object'}, 'base_api_param_string': ', json=json, headers=headers', 'instance_method_param_string': 'self, json, headers', 'http_method': 'post', 'endpoint': '/cars/add'}}, {'get_cars_find': {'params': {'query_params': [('name', 'str'), ('brand', 'str')], 'path_params': []}, 'base_api_param_string': ', params=params, headers=headers', 'instance_method_param_string': 'self, params, headers', 'http_method': 'get', 'endpoint': '/cars/find'}}, {'get_cars_name': {'params': {'query_params': [], 'path_params': [('name', 'str')]}, 'base_api_param_string': ', headers=headers', 'instance_method_param_string': 'self, name, headers', 'http_method': 'get', 'endpoint': '/cars/{name}'}}, {'put_cars_update_name': {'params': {'query_params': [], 'path_params': [('name', 'str')], 'json_params': [('name', 'str'), ('brand', 'str'), ('price_range', 'str'), ('car_type', 'str')], 'content_schema_type': 'object'}, 'base_api_param_string': ', json=json, headers=headers', 'instance_method_param_string': 'self, name, json, headers', 'http_method': 'put', 'endpoint': '/cars/update/{name}'}}, {'delete_cars_remove_name': {'params': {'query_params': [], 'path_params': [('name', 'str')]}, 'base_api_param_string': ', headers=headers', 'instance_method_param_string': 'self, name, headers', 'http_method': 'delete', 'endpoint': '/cars/remove/{name}'}}, {'get_cars_filter_car_type': {'params': {'query_params': [], 'path_params': [('car_type', 'str')]}, 'base_api_param_string': ', headers=headers', 'instance_method_param_string': 'self, car_type, headers', 'http_method': 'get', 'endpoint': '/cars/filter/{car_type}'}}], 'url_method_name': 'cars_url'}}}