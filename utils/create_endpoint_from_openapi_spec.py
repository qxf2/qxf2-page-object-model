"""
This module will create Endpoint files from an OpenAPI spec ver 3.x

What does an Endpoint file hold?:
- It should contain a class with methods to make various http calls against an endpoint
- It should only contain steps to make the http calls and return the data
- It should not contain business logic

For more info read - https://qxf2.com/blog/easily-maintainable-api-test-automation-framework/

What does this module do?:
- It creates an Endpoint file with a class from the OpenAPI spec
- The path key in the spec is translated to an Endpoint
- The operations(http methods) for a path is translated to instance methods for the Endpoint
- The parameters for operations are translated to function parameters for the instance methods
- HTTP Basic, HTTP Bearer and API Keys Auth are currently supported by this module & handled
through headers
"""

from dataclasses import dataclass, field
from enum import Enum
from optparse import OptionParser
from pathlib import Path
import re
import json
from openapi_parser import parse, specification
from jinja2 import FileSystemLoader, Environment
from loguru import logger


ENDPOINT_TEMPLATE_NAME = Path(__file__).parent.joinpath("endpoint_template.txt")
ENDPOINT_DESTINATION_DIR = Path(__file__).parent.parent.joinpath("endpoints")

# pylint: disable=line-too-long
class FunctionParamType(Enum):
    """
    A class to represent request parameter types
    ...

    Attributes:
    -----------
    path:
        A path type parameter
    query:
        A query type parameter
    request_body:
        A request body type parameter
    """
    path = "args"
    query = "params"
    request_body = "json"

@dataclass
class ParsedSpec():
    """
    A data class to represent the parsed spec
    ...

    Attributes:
    -----------
    spec_file: str
        OpenAPI specification file
    spec: specification.Specification
        a data class that represents the parsed spec
    paths: list[specification.Path]
        a list of specification.Path data class to represent the endpoint paths
    """
    spec_file: str
    spec: specification.Specification = field(init=False, repr=False)
    paths: list[specification.Path] = field(init=False, repr=False)

    def __post_init__(self):
        self.spec = parse(self.spec_file)
        logger.info(f"Parsing spec - {self.spec_file}")
        self.paths = self.spec.paths
        # parameters can be in two places:
        # 1. path.parameter
        # 2. path.operation.parameter
        # move all parameters to #2
        for path in self.paths:
            if hasattr(path, 'parameters'):
                for operation in path.operations:
                    if not operation.parameters:
                        operation.parameters = path.parameters

class EndpointGenerator(ParsedSpec):
    """
    A class to Generate Endpoint module
    ...

    Attributes:
    ----------
    spec_file: str
        name and location of the spec file
    endpoint_template_filename: str
        endpoint template filename
    jinja_template_dir: str
        jinja template location directory

    Methods:
    --------
    generate_endpoint_metadata() -> dict
    content_generator() -> str
    """
    def __init__(self, spec_file: str):
        """
        Initialize Endpoint Generator class
        """
        super().__init__(spec_file)
        self.endpoint_template_filename = ENDPOINT_TEMPLATE_NAME.name
        self.jinja_template_dir = ENDPOINT_TEMPLATE_NAME.parent.name
        self.jinja_environment = Environment(loader=FileSystemLoader(self.jinja_template_dir))
        self.endpoint_metadata = self.generate_endpoint_metadata()

    def generate_endpoint_metadata(self) -> dict:
        """
        Extract endpoint information from the OpenAPI spec

        Returns:
        -------
        dict_from_spec: dict
            a metadata dict extracted from the spec
        """
        dict_from_spec = {}
        logger.info(f"Generating dictionary from OpenAPI spec")
        for path in self.paths:
            try:
                # group endpoints together based on the base endpoint
                # group /users & /users/add together
                # this is useful to add all similar endpoints in one file
                path_name = path.url
                logger.info(f"Parsing path - {path_name}")
                # if the endpoint is only /
                # make it /home
                # this is going to be a problem when there is /home
                if path_name == "/":
                    endpoint_split = ["home"]
                else:
                    endpoint_split = path_name.split("/")
                    endpoint_split = [ text for text in endpoint_split if text ]
                common_base_endpoint = endpoint_split[0]
                if dict_from_spec.get(common_base_endpoint):
                    dict_from_spec[common_base_endpoint]['endpoints'].append(path_name)
                else:
                    dict_from_spec[common_base_endpoint] = {'endpoints': [path_name]}

                # create filename module name for an endpoint group
                endpoints_in_a_file = [endpoint.capitalize() for endpoint in re.split("-|_", common_base_endpoint)]
                dict_from_spec[common_base_endpoint]['module_name'] = "_".join(endpoints_in_a_file) + "_" + "Endpoint"
                dict_from_spec[common_base_endpoint]['class_name'] = "".join(endpoints_in_a_file) + "Endpoint"
                dict_from_spec[common_base_endpoint]['url_method_name'] = common_base_endpoint.replace('-', '_') + "_" + "url"

                # create functions for every operation - http methods
                # identify the parameters for the functions
                for operation in path.operations:
                    function_details = {}
                    function_parameters = []
                    function_parameters.append({'name':'self', 'param_expression':'args'})
                    updated_endpoint_split = []
                    request_function_param = ''
                    parameter_string = 'self'
                    http_method = operation.method.name.lower()
                    for endpoint in endpoint_split:
                        endpoint = endpoint.replace("-","_")
                        if "{" in endpoint:
                            endpoint = re.sub("{|}", "", endpoint)
                            endpoint = "by_" + endpoint
                        updated_endpoint_split.append(endpoint)
                    name = http_method + "_" + "_".join(updated_endpoint_split)
                    function_details['name'] = name
                    function_details['endpoint'] = path_name
                    function_details['http_method'] = http_method
                    for param in operation.parameters:
                        param_dict = {}
                        if param.location.name.lower() == "path":
                            param_dict['name'] = param.name
                            param_dict['param_expression'] = FunctionParamType.path.value
                            param_dict['data_type'] = param.schema.type.name.lower()
                            parameter_string += ', ' + param.name
                        elif param.location.name.lower() == "query":
                            param_dict['param_expression'] = FunctionParamType.query.value
                            param_dict['name'] = param.name
                            param_dict['data_type'] = param.schema.type.name.lower()
                            if 'params' not in parameter_string:
                                parameter_string += ', ' + 'params'
                            if 'params' not in request_function_param:
                                request_function_param += ', ' + "params=params"
                        function_parameters.append(param_dict)
                    if operation.request_body is not None:
                        for content in operation.request_body.content:
                            for property in content.schema.properties:
                                if hasattr(property.schema, 'properties'):
                                    for schema_prop in property.schema.properties:
                                        param_dict = {}
                                        param_dict['param_expression'] = FunctionParamType.request_body.value
                                        param_dict['name'] = schema_prop.name
                                        param_dict['data_type'] = schema_prop.schema.type.name.lower()
                                        function_parameters.append(param_dict)
                                else:
                                    param_dict = {}
                                    param_dict['param_expression'] = FunctionParamType.request_body.value
                                    param_dict['name'] = property.name
                                    param_dict['data_type'] = property.schema.type.name.lower()
                                    function_parameters.append(param_dict)
                                if 'json' not in request_function_param:
                                    request_function_param += ', '+ 'json=json'
                                if 'json' not in parameter_string:
                                    parameter_string += ', ' + 'json'
                    function_details['parameters'] = function_parameters

                    # Add headers to function param string
                    # auth should be handled in headers
                    request_function_param += ", " + "headers=headers"
                    parameter_string += ", " + "headers"
                    function_details['request_function_param'] = request_function_param
                    function_details['parameter_string'] = parameter_string
                    if dict_from_spec[common_base_endpoint].get('functions'):
                        dict_from_spec[common_base_endpoint]['functions'].append(function_details)
                    else:
                        dict_from_spec[common_base_endpoint]['functions'] = [function_details]
                    logger.info(f"Completed parsing path {path_name} & generated a dict from the path spec")
            except Exception as err:
                logger.warning(f"Unable to Parse Path - {path}, due to {err}")
                continue

        return dict_from_spec

    def content_generator(self, endpoint_details: dict) -> str:
        """
        Create Jinja2 template content

        Returns:
        --------
        content: str
            The Endpoint file content
        """
        content = None
        try:
            logger.info(f"Using template file - {self.endpoint_template_filename}")
            template = self.jinja_environment.get_template(self.endpoint_template_filename)
            content = template.render(endpoint=endpoint_details)
        except Exception as err:
            raise err
        return content

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--spec",
                      dest="spec",
                      help="Location to the OpenAPI spec file")
    parser.add_option("--verbose",
                      dest="verbose",
                      action="store_true",
                      default=False,
                      help="Pass the verbose flag to print generated dict and content")
    parser.add_option("--create-endpoints",
                      dest="create_endpoints",
                      default=False,
                      action="store_true",
                      help="Create endpoint file if this option is passed")

    (options, args) = parser.parse_args()
    if options.spec:
        endpoint_generator = EndpointGenerator(options.spec)
        metadata_dict = endpoint_generator.endpoint_metadata
        if options.verbose:
            print(json.dumps(metadata_dict, indent=4))
        if options.create_endpoints:
            for endpoint in metadata_dict.keys():
                endpoint_filename = ENDPOINT_DESTINATION_DIR.joinpath(metadata_dict[endpoint]['module_name'] + '.py')
                logger.info(f"The resultant Endpoint filename will be - {endpoint_filename}")
                endpoint_template_content = endpoint_generator.content_generator(metadata_dict[endpoint])
                if options.verbose:
                    print(endpoint_template_content)
                with open(endpoint_filename, 'w', encoding='utf-8') as endpoint_file:
                    endpoint_file.write(endpoint_template_content)
                    logger.info(f"Endpoint content render complete and saved the endpoint as file - {endpoint_filename}")
    else:
        parser.print_help()
