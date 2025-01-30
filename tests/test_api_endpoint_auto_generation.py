"""
API Endpoint Auto generation test validates:
1. Endpoint Module name generation from an OpenAPI spec
2. Endpoint class name generation from the spec
3. URL method name generation for the Endpoint class from the spec
4. Base API method call string generation for Jinja template
5. Endoint object instance method call string generation for Jinja template
6. Values obtained for an endpoint after parsing the spec
7. JSON params for an endpoint obtained after parsing the spec
8. Query params for an endpoint after parsing the spec
9. Path params for an endpoint after parsing the spec
"""

import pytest
import requests

@pytest.mark.API_AUTO_GEN_UNIT
def test_module_name_generation(name_generator):
	"Validate module name generation from spec"
	assert name_generator.module_name == "cars_endpoint"

@pytest.mark.API_AUTO_GEN_UNIT
def test_class_name_generation(name_generator):
	"Validate class name generation from spec"
	assert name_generator.class_name == "CarsEndpoint"

@pytest.mark.API_AUTO_GEN_UNIT
def test_url_method_name(name_generator):
	"Validate URL method name generation from spec"
	assert name_generator.url_method_name == "cars_url"

@pytest.mark.API_AUTO_GEN_UNIT
def test_base_api_param_string(name_generator):
	"Validate Base_API method call generation string"
	assert name_generator.base_api_param_string == ", headers=headers"

@pytest.mark.API_AUTO_GEN_UNIT
def test_instance_method_param_string(name_generator):
	"Validate Endpoint method call generation string"
	assert name_generator.instance_method_param_string == "self, name, headers"

@pytest.mark.API_AUTO_GEN_UNIT
def test_parsed_spec_get_method(parsed_spec, requests_mock):
	"Validate OpenAPI spec parsed values"
	http_method_in_test = parsed_spec[0]["get_cars"]
	endpoint = http_method_in_test["endpoint"]
	http_method = http_method_in_test["http_method"]
	requests_mock.get("http://stub-cars-api/cars", status_code=200)
	# Validate that the endpoint value was rightly parsed from the spec
	assert requests.request(method=http_method, url=f"http://stub-cars-api{endpoint}").status_code == 200

@pytest.mark.API_AUTO_GEN_UNIT
def test_parsed_spec_post_method(parsed_spec, requests_mock):
	"Validate OpenAPI spec parsed values for json params"
	http_method_in_test = parsed_spec[1]["post_cars_add"]
	endpoint = http_method_in_test["endpoint"]
	http_method = http_method_in_test["http_method"]
	json_keys = http_method_in_test["params"]["json_params"]
	json_content = {}
	for key in json_keys:
		json_content[key[0]] = "random_string"
	requests_mock.post("http://stub-cars-api/cars/add", json=json_content)
	json_response = requests.request(method=http_method, url=f"http://stub-cars-api{endpoint}").json()
	# Validate that the JSON keys were rightly parsed for the endpoint
	assert json_response.get("name")
	assert json_response.get("brand")
	assert json_response.get("price_range")
	assert json_response.get("car_type")

@pytest.mark.API_AUTO_GEN_UNIT
def test_parsed_spec_query_params(parsed_spec, requests_mock):
	"Validate OpenAPI spec parsed values for query params"
	http_method_in_test = parsed_spec[2]["get_cars_find"]
	endpoint = http_method_in_test["endpoint"]
	http_method = http_method_in_test["http_method"]
	query_keys = http_method_in_test["params"]["query_params"]
	query_params = {}
	for key in query_keys:
		query_params[key[0]] =  "random_string"
	requests_mock.get(f"http://stub-cars-api/cars/find?name={query_params['name']}&brand={query_params['brand']}", status_code=200)
	response = requests.request(method=http_method, url=f"http://stub-cars-api{endpoint}", params=query_params)
	# Validat that the Query params were rightly parsed from the spec
	assert response.status_code==200

@pytest.mark.API_AUTO_GEN_UNIT
def test_parsed_spec_path_param(parsed_spec, requests_mock):
	"Validate OpenAPI spec parsed values for path params"
	http_method_in_test = parsed_spec[3]["get_cars_name"]
	http_method = http_method_in_test["http_method"]
	path_keys = http_method_in_test["params"]["path_params"][0]
	path_param = {path_keys[0]: "foo"}
	requests_mock.get("http://stub-cars-api/cars/foo", status_code=200)
	response = requests.request(method=http_method, url=f"http://stub-cars-api/cars/{path_param['name']}")
	# Validate that the path params were rightly parsed from the spec
	assert response.status_code==200
