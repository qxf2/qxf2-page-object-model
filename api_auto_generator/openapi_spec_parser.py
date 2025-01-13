"""
OpenAPI specification Parser
"""
# pylint: disable=locally-disabled, multiple-statements, fixme, line-too-long
# pylint: disable=too-many-nested-blocks


from typing import Union, TextIO
from openapi_parser import parse, specification
from openapi_spec_validator.readers import read_from_filename
from openapi_spec_validator import validate_spec
import openapi_spec_validator as osv
from endpoint_name_generator import NameGenerator


# pylint: disable=too-many-instance-attributes
# pylint: disable=broad-except
class OpenAPIPathParser():
    "OpenAPI Path object parser"


    def __init__(self, path: specification.Path, logger_obj):
        "Init the instance"
        self.module_name = None
        self.class_name = None
        self.url_method_name = None
        self.instance_methods = []
        self.path_dict = {}
        self.path = path
        self.operations = self.path.operations
        self.logger = logger_obj

        # parameters can be in two places:
        # 1. path.parameter
        # 2. path.operation.parameter
        # move all parameters to #2
        for operation in self.operations:
            try:
                if self.path.parameters:
                    operation.parameters.append(*path.parameters)

                # Parse operations(HTTP Methods) to get Endpoint instance method details
                instance_method_details = {} # Dict to collect all instance methods for a HTTP Method
                parsed_parameters = {} # Dict to collect: 1.Query, 2.Path & 3.RequestBody params

                # Parse Query & Path parameters
                q_params, p_params = self.parse_parameters(operation.parameters)
                parsed_parameters['query_params'] = q_params
                parsed_parameters['path_params'] = p_params

                # Parse RequestBody parameters
                rb_type = None
                rb_param = None
                con_schma_type = None
                if operation.request_body:
                    rb_type, rb_param, con_schma_type = self.parse_request_body(operation.request_body)
                    if rb_type == "json":
                        parsed_parameters['json_params'] = rb_param
                    elif rb_type == "data":
                        parsed_parameters['data_params'] = rb_param
                    parsed_parameters['content_schema_type'] = con_schma_type

                # Generate: 1.Module, 2.Class, 3.url_method_name, 4.base_api_param_string,
                # 5.instance_method_param_string, 6.instance_method_name name using NameGenerator Obj
                name_gen_obj = NameGenerator(path.url,
                                            bool(q_params),
                                            p_params,
                                            rb_type)
                self.module_name = name_gen_obj.module_name
                self.class_name = name_gen_obj.class_name
                self.url_method_name = name_gen_obj.url_method_name
                base_api_param_string = name_gen_obj.base_api_param_string
                instance_method_param_string = name_gen_obj.instance_method_param_string
                instance_method_name = name_gen_obj.get_instance_method_name(operation.method.name.lower())

                # Collect the Endpoint instance method details
                instance_method_details[instance_method_name] = {'params':parsed_parameters,
                                                                    'base_api_param_string':base_api_param_string,
                                                                    'instance_method_param_string': instance_method_param_string,
                                                                    'http_method': operation.method.name.lower(),
                                                                    'endpoint':self.path.url}
                self.instance_methods.append(instance_method_details)
                self.logger.info(f"Parsed {operation.method.name} for {self.path.url}")
            except Exception as failed_to_parse_err:
                self.logger.debug(f"Failed to parse {operation.method.name} for {self.path.url} due to {failed_to_parse_err}, skipping it")
                continue


    # pylint: disable=inconsistent-return-statements
    def get_function_param_type(self, type_str: str) -> Union[str, None]:
        "Translate the datatype in spec to corresponding Python type"
        if type_str.lower() == 'boolean':
            return 'bool'
        if type_str.lower() == 'integer':
            return 'int'
        if type_str.lower() == 'number':
            return 'float'
        if type_str.lower() == 'string':
            return 'str'
        if type_str.lower() == 'array':
            return 'list'
        if type_str.lower() == 'object':
            return 'dict'


    def parse_parameters(self, parameters: list[specification.Parameter]) -> tuple[list, list]:
        """
        Create class parameters for Endpoint module
        This function will parse:
            1. Query Parameters
            2. Path Parameters
        """
        query_params = []
        path_params = []

        # Loop through list[specification.Parameter] to identify: 1.Query, 2.Path params
        for parameter in parameters:
            if parameter.location.name.lower() == "path":
                name = parameter.name
                param_type = self.get_function_param_type(parameter.schema.type.name)
                if (name, param_type,) not in path_params:
                    path_params.append((name, param_type))
            elif parameter.location.name.lower() == "query":
                name = parameter.name
                param_type = self.get_function_param_type(parameter.schema.type.name)
                if (name, param_type,) not in query_params:
                    query_params.append((name, param_type))
        return (query_params, path_params,)


    def get_name_type_nested_prop(self, property) -> list:
        "Get the name & type for nested property"
        nested_param_list = []
        for nested_prop in property.schema.properties:
            nested_name = nested_prop.name
            nested_param_type = self.get_function_param_type(nested_prop.schema.type.name)
            nested_param_list.append(nested_name, nested_param_type)
        return nested_param_list

    # pylint: disable=too-many-branches
    def parse_request_body(self, request_body: specification.RequestBody) -> tuple[str, list, str]:
        """
        Parse the requestBody from the spec and return a list of json & data params
        This function will parse dict inside a JSON/Form param to only one level only
        i.e this function will identify another_dict in this example:
        json_param = {
            another_dict: {
                'nested_key': 'nested_value'},
            'key':'value
        }
        but will not identify nested_dict in:
        json_param = {
        another_dict:{
            'nested_dict':{
                'nested_key': 'nested_value'}
            }
        },
        'key':'value
        }
        """
        requestbody_type = None
        requestbody_param = []
        content_schema_type = None

        # Parse the request_body in the spec
        # Identify the content type of the request_body
        # This module currently supports: 1.json, 2.form content types
        for content in request_body.content:
            if content.type.name.lower() == "json":
                if content.schema.type.name.lower() == 'object':
                    for prop in content.schema.properties:
                        name = prop.name
                        requestbody_type = self.get_function_param_type(prop.schema.type.name)
                        if requestbody_type == 'dict':
                            nested_dict_param = {}
                            nested_param_list = self.get_name_type_nested_prop(prop)
                            nested_dict_param[name] = nested_param_list
                            requestbody_param.append(nested_dict_param)
                        else:
                            requestbody_param.append((name, requestbody_type))
                        requestbody_type = "json"
                if content.schema.type.name.lower() == 'array':
                    for prop in content.schema.items.properties:
                        name = prop.name
                        requestbody_type = self.get_function_param_type(prop.schema.type.name)
                        if requestbody_type == 'dict':
                            nested_dict_param = {}
                            nested_param_list = self.get_name_type_nested_prop(prop)
                            nested_dict_param[name] = nested_param_list
                            requestbody_param.append(nested_dict_param)
                        else:
                            requestbody_param.append((name, requestbody_type))
                        requestbody_type = "json"
                content_schema_type = content.schema.type.name.lower()
            if content.type.name.lower() == "form":
                if content.schema.type.name.lower() == 'object':
                    for prop in content.schema.properties:
                        name = prop.name
                        requestbody_type = self.get_function_param_type(prop.schema.type.name)
                        if requestbody_type == 'dict':
                            nested_dict_param = {}
                            nested_param_list = self.get_name_type_nested_prop(prop)
                            nested_dict_param[name] = nested_param_list
                            requestbody_param.append(nested_dict_param)
                        else:
                            requestbody_param.append((name, requestbody_type))
                        requestbody_type = "data"
                content_schema_type = content.schema.type.name.lower()
        return (requestbody_type, requestbody_param, content_schema_type,)


class OpenAPISpecParser():
    "OpenAPI Specification Parser Object"


    # pylint: disable=too-few-public-methods
    def __init__(self, spec_file: TextIO, logger_obj) -> None:
        "Init Spec Parser Obj"

        self.logger = logger_obj
        # Generate Final dict usable against a Jinja2 template from the OpenAPI Spec
        self._fdict = {}
        """
        _fdict structure:
        {
           module_name1:{
                       class_name1:{
                                   instance_methods: [],
                                   url_method_name: str
                                   }
                       }
           module_name2:{
                       class_name1:{
                                   instance_methods: [],
                                   url_method_name: str
                                   }
                       }
        }
        """
        try: # <- Outer level try-catch to prevent exception chaining
            spec_dict, _ = read_from_filename(spec_file)
            validate_spec(spec_dict)
            self.logger.success(f"Successfully validated spec file - {spec_file}")
            try:
                self.parsed_spec = parse(spec_file)
                # Loop through all paths and parse them using OpenAPIPathParser obj
                # Collect the: 1.Module, 2.Class, 3.url_method_name,
                # 4.base_api_param_string, 5.instance_method_param_string,
                # 6.instance_method_name name
                for path in self.parsed_spec.paths:
                    p_path = OpenAPIPathParser(path, logger_obj)
                    if p_path.module_name:
                        if self._fdict.get(p_path.module_name):
                            if self._fdict[p_path.module_name].get(p_path.class_name):
                                if self._fdict[p_path.module_name][p_path.class_name].get('instance_methods'):
                                    for instance_method in p_path.instance_methods:
                                        self._fdict[p_path.module_name][p_path.class_name]['instance_methods'].append(instance_method)
                                else:
                                    self._fdict[p_path.module_name][p_path.class_name]= {'instance_methods': p_path.instance_methods}
                            else:
                                self._fdict[p_path.module_name][p_path.class_name]={'instance_methods': p_path.instance_methods}

                        else:
                            self._fdict[p_path.module_name]= {p_path.class_name:{'instance_methods': p_path.instance_methods}}
                        self._fdict[p_path.module_name][p_path.class_name]['url_method_name'] = p_path.url_method_name
            except Exception as err:
                self.logger.error(err)
        except osv.validation.exceptions.OpenAPIValidationError as val_err:
            self.logger.error(f"Validation failed for {spec_file}")
            self.logger.error(val_err)
        except Exception as gen_err:
            self.logger.error(f"Failed to parse spec {spec_file}")
            self.logger.error(gen_err)
        else:
            self.logger.success(f"Successfully parsed spec file {spec_file}")


    @property
    def parsed_dict(self):
        "Parsed dict for Jinja2 template from OpenAPI spec"
        return self._fdict
