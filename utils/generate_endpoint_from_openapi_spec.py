"""
What does this module do?:
- It creates an Endpoint file with a class from the OpenAPI spec
- The path key in the spec is translated to an Endpoint
- The operations(http methods) for a path is translated to instance methods for the Endpoint
- The parameters for operations are translated to function parameters for the instance methods
- HTTP Basic, HTTP Bearer and API Keys Auth are currently supported by this module & should passed
through headers
"""


import re
from argparse import ArgumentParser
from dataclasses import dataclass, field
from pathlib import Path
from typing import Union
from jinja2 import FileSystemLoader, Environment
from openapi_parser import parse, specification
from loguru import logger
from openapi_spec_validator.readers import read_from_filename
from openapi_spec_validator import validate_spec
import openapi_spec_validator as osv


# pylint: disable=line-too-long
# Get the template file location & endpoint destination location relative to this script
ENDPOINT_TEMPLATE_NAME = Path(__file__).parent.joinpath("endpoint_template.jinja2") # <- Jinja2 template needs to be on the same directory as this script
ENDPOINT_DESTINATION_DIR = Path(__file__).parent.parent.joinpath("endpoints") # <- The Endpoint files are created in the endpoints dir in the project root


def create_endpoint_split(endpoint_url: str) -> list[str]:
    """
    Split the text in the endpoint, clean it up & return a list of text
    """
    # if the endpoint is only /
    # make it /home_base (it needs to be unique)
    if endpoint_url == "/":
        endpoint_split = ["home_base"]
    else:
        endpoint_split = endpoint_url.split("/")
        endpoint_split = [ re.sub("{|}","",text) for text in endpoint_split if text ]
    return endpoint_split


def create_module_class_url_name(endpoint_url:str) -> tuple[str, str, str]:
    """
    Create:
        1. Module name
        2. Class name
        3. url method name
    """
    endpoint_split = create_endpoint_split(endpoint_url)
    common_base_endpoint = endpoint_split[0]

    # create filename module name for an endpoint group
    endpoints_in_a_file = [endpoint.capitalize() for endpoint in re.split("-|_", common_base_endpoint)]
    module_name = "_".join(endpoints_in_a_file) + "_" + "Endpoint"
    class_name = "".join(endpoints_in_a_file) + "Endpoint"
    url_method_name = common_base_endpoint.replace('-', '_') + "_" + "url"
    return (module_name, class_name, url_method_name,)


def get_function_param_type(type_str: str) -> Union[str, None]:
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


def parse_request_body(request_body: specification.RequestBody) -> tuple[str,list]:
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
    parsed_rb = []
    param_type = None
    for content in request_body.content:
        if content.type.name.lower() == "json":
            if content.schema.type.name.lower() == 'object':
                for prop in content.schema.properties:
                    name = prop.name
                    param_type = get_function_param_type(prop.schema.type.name)
                    if param_type == 'dict':
                        nested_dict_param = {name: []}
                        for nested_prop in prop.schema.properties:
                            nested_name = nested_prop.name
                            nested_param_type = get_function_param_type(nested_prop.schema.type.name)
                            nested_dict_param[name].append((nested_name, nested_param_type))
                        parsed_rb.append(nested_dict_param)
                    else:
                        parsed_rb.append((name, param_type))
                    param_type = "json"
        if content.type.name.lower() == "form":
            if content.schema.type.name.lower() == 'object':
                for prop in content.schema.properties:
                    name = prop.name
                    param_type = get_function_param_type(prop.schema.type.name)
                    if param_type == 'dict':
                        nested_dict_param = {name: []}
                        for nested_prop in prop.schema.properties:
                            nested_name = nested_prop.name
                            nested_param_type = get_function_param_type(nested_prop.schema.type.name)
                            nested_dict_param[name].append((nested_name, nested_param_type))
                        parsed_rb.append(nested_dict_param)
                    else:
                        parsed_rb.append((name, param_type))
                    param_type = "data"
    return (param_type,parsed_rb,)


def parse_parameters(parameters: list[specification.Parameter]) -> tuple[list, list]:
    """
    Create class parameters for Endpoint module
    This function will parse:
        1. Query Parameters
        2. Path Parameters
    """
    query_params = []
    path_params = []
    for parameter in parameters:
        if parameter.location.name.lower() == "path":
            name = parameter.name
            param_type = get_function_param_type(parameter.schema.type.name)
            if (name, param_type,) not in path_params:
                path_params.append((name, param_type))
        elif parameter.location.name.lower() == "query":
            name = parameter.name
            param_type = get_function_param_type(parameter.schema.type.name)
            if (name, param_type,) not in query_params:
                query_params.append((name, param_type))
    return (query_params, path_params,)


@dataclass
class Endpoint(specification.Path):
    """
    This dataclass defines attributes for Endpoint
    """
    module_name: str = field(init=False)
    class_name: str = field(init=False)
    url_method_name: str = field(init=False)
    instance_methods: list = field(init=False, default_factory=list)

    def __post_init__(self):
        "Set post init attributes"
        module_name, class_name, url_method_name = create_module_class_url_name(self.url)
        self.module_name = module_name
        self.class_name = class_name
        self.url_method_name = url_method_name.lower()
        # parameters can be in two places:
        # 1. path.parameter
        # 2. path.operation.parameter
        # move all parameters to #2
        for operation in self.operations:
            parsed_parameters = {}
            base_api_param_string = ''
            instance_method_param_string = 'self'
            if self.parameters:
                operation.parameters.append(*self.parameters)

            # Parse and get the Path & Query Parameters
            query_params, path_params = parse_parameters(operation.parameters)
            if query_params:
                base_api_param_string += ', params=params' # <- this string is the parameters that will be passed to the Base_API method calls
                instance_method_param_string += ', params' # <- this string is the parameters that will be passed to the Endpoint instance methods
            if path_params:
                for path_param in path_params:
                    instance_method_param_string += f', {path_param[0]}'
            parsed_parameters['query_params'] = query_params
            parsed_parameters['path_params'] = path_params

            # Parse the request body and create the JSON params that needs to be passed to request function
            if operation.request_body:
                request_body_type, request_body_params = parse_request_body(operation.request_body)
                if request_body_type == "json":
                    base_api_param_string += ', json=json'
                    instance_method_param_string += ', json'
                    parsed_parameters['json_params'] = request_body_params
                elif request_body_type == "data":
                    base_api_param_string += ', data=data'
                    instance_method_param_string += ', data'
                    parsed_parameters['data_params'] = request_body_params
            endpoint_split = create_endpoint_split(self.url)
            endpoint_split = [text.lower() for text in endpoint_split]
            endpoint_split = [text.replace('-','_') for text in endpoint_split]
            http_method = operation.method.name.lower()
            instance_method_name = http_method + "_" + "_".join(endpoint_split)
            # Add headers to parameter strings
            base_api_param_string += ", headers=headers"
            instance_method_param_string += ', headers'
            self.instance_methods.append({instance_method_name:{'params':parsed_parameters,
                                                                'base_api_param_string':base_api_param_string,
                                                                'instance_method_param_string': instance_method_param_string,
                                                                'http_method': http_method,
                                                                'endpoint':self.url}})


def build_template_dict(endpoint_dcls: Endpoint, default_endpoint_dict: dict) -> dict:
    """
    Generate a dict from Endpoint dataclass
    This dict will be rendered on the Jinja2 template
    """
    if default_endpoint_dict.get(endpoint_dcls.module_name):
        if default_endpoint_dict[endpoint_dcls.module_name].get(endpoint_dcls.class_name):
            if default_endpoint_dict[endpoint_dcls.module_name][endpoint_dcls.class_name].get('instance_methods'):
                for instance_method in endpoint_dcls.instance_methods:
                    endpoint_dict[endpoint_dcls.module_name][endpoint_dcls.class_name]['instance_methods'].append(instance_method)
            else:
                default_endpoint_dict[endpoint_dcls.module_name][endpoint_dcls.class_name]= {'instance_methods': endpoint_dcls.instance_methods}
        else:
            default_endpoint_dict[endpoint_dcls.module_name][endpoint_dcls.class_name]={'instance_methods': endpoint_dcls.instance_methods}

    else:
        default_endpoint_dict[endpoint_dcls.module_name]= {endpoint_dcls.class_name:{'instance_methods': endpoint_dcls.instance_methods}}
    default_endpoint_dict[endpoint_dcls.module_name][endpoint_dcls.class_name]['url_method_name'] = endpoint_dcls.url_method_name


class EndpointGenerator():
    """
    A class to Generate Endpoint module
    """
    def __init__(self):
        """
        Initialize Endpoint Generator class
        """
        self.endpoint_template_filename = ENDPOINT_TEMPLATE_NAME.name
        self.jinja_template_dir = ENDPOINT_TEMPLATE_NAME.parent.name
        self.jinja_environment = Environment(loader=FileSystemLoader(self.jinja_template_dir),
                                             autoescape=True)


    def content_generator(self, endpoint_class_name: str, endpoint_class_content: dict) -> str:
        """
        Create Jinja2 template content
        """
        content = None
        try:
            template = self.jinja_environment.get_template(self.endpoint_template_filename)
            content = template.render(class_name=endpoint_class_name, class_content=endpoint_class_content)
            return content
        except Exception as error:
            raise error


    def generate_endpoint_file(self, endpoint_filename: str, endpoint_filecontent: str):
        """
        Create an Endpoint file
        """
        try:
            endpoint_filename = ENDPOINT_DESTINATION_DIR.joinpath(endpoint_filename+'.py')
            with open(endpoint_filename, 'w', encoding='utf-8') as endpoint_f:
                endpoint_f.write(endpoint_filecontent)
            logger.success(f"Successfully generated Endpoint file - {endpoint_filename}")
        except Exception as endpoint_creation_err:
            raise endpoint_creation_err


if __name__ == "__main__":
    arg_parser = ArgumentParser(prog="GenerateEndpointFile",
                                description="Generate Endpoint.py file from OpenAPI spec")
    arg_parser.add_argument("--spec",
                            dest="spec_file",
                            required=True,
                            help="Pass the location to the OpenAPI spec file, Passing this param alone will run a dry run of endpoint content generation with actually creating the endpoint")
    arg_parser.add_argument("--generate-endpoint",
                            dest='if_generate_endpoint',
                            action='store_true',
                            help="This param will create <endpoint_name>_Endpoint.py file for Path objects from the OpenAPI spec")

    args = arg_parser.parse_args()
    endpoint_dict = {}
    try:
        spec_dict, base_uri = read_from_filename(args.spec_file)
        validate_spec(spec_dict)
        try:
            parser = parse(args.spec_file)
            endpoint_generator = EndpointGenerator()
            for path in parser.paths:
                logger.info(f"Parsing endpoing {path.url}")
                # pylint: disable=E1121
                endpoint = Endpoint(path.url,
                                    path.summary,
                                    path.description,
                                    path.operations,
                                    path.parameters,
                                    path.extensions)
                build_template_dict(endpoint, endpoint_dict)
                logger.success(f"Successfully parsed Path - {path.url}")
            for  mod_name, cl_content in endpoint_dict.items():
                for cl_name, nested_cl_content in cl_content.items():
                    endpoint_content = endpoint_generator.content_generator(cl_name, nested_cl_content)
                    if args.if_generate_endpoint:
                        endpoint_generator.generate_endpoint_file(mod_name, endpoint_content)
        except Exception as err:
            raise err
    except osv.validation.exceptions.OpenAPIValidationError as err:
        raise err
