"""
What does this module do?:
- It creates an Endpoint file with a class from the OpenAPI spec
- The path key in the spec is translated to an Endpoint
- The operations(http methods) for a path is translated to instance methods for the Endpoint
- The parameters for operations are translated to function parameters for the instance methods
- HTTP Basic, HTTP Bearer and API Keys Auth are currently supported by this module & should passed
through headers
"""


import json
from argparse import ArgumentParser
from pathlib import Path
from jinja2 import FileSystemLoader, Environment
from jinja2.exceptions import TemplateNotFound
from loguru import logger
from openapi_spec_parser import OpenAPISpecParser


# pylint: disable=line-too-long
# Get the template file location & endpoint destination location relative to this script
ENDPOINT_TEMPLATE_NAME = Path(__file__).parent.joinpath("templates").joinpath("endpoint_template.jinja2") # <- Jinja2 template needs to be on the same directory as this script
ENDPOINT_DESTINATION_DIR = Path(__file__).parent.parent.joinpath("endpoints") # <- The Endpoint files are created in the endpoints dir in the project root


class EndpointGenerator():
    """
    A class to Generate Endpoint module using Jinja2 template
    """


    def __init__(self, logger_obj: logger):
        """
        Initialize Endpoint Generator class
        """
        self.endpoint_template_filename = ENDPOINT_TEMPLATE_NAME.name
        self.jinja_template_dir = ENDPOINT_TEMPLATE_NAME.parent.absolute()
        self.logger = logger_obj
        self.logger.debug(f"Using {self.endpoint_template_filename} from {self.jinja_template_dir}")
        self.jinja_environment = Environment(loader=FileSystemLoader(self.jinja_template_dir),
                                             autoescape=True)


    def endpoint_class_content_generator(self,
                                         endpoint_class_name: str,
                                         endpoint_class_content: dict) -> str:
        """
        Create Jinja2 template content
        """
        content = None
        try:
            template = self.jinja_environment.get_template(self.endpoint_template_filename)
            content = template.render(class_name=endpoint_class_name, class_content=endpoint_class_content)
            self.logger.success("Successfully generated Endpoint class content for {endpoint_class_name}")
            return content
        except Exception as error:
            raise error


    def generate_endpoint_file(self,
                               endpoint_filename: str,
                               endpoint_class_name: str,
                               endpoint_class_content: dict):
        """
        Create an Endpoint file
        """
        try:
            endpoint_filename = ENDPOINT_DESTINATION_DIR.joinpath(endpoint_filename+'.py')
            endpoint_content = self.endpoint_class_content_generator(endpoint_class_name,
                                                                     endpoint_class_content)
            with open(endpoint_filename, 'w', encoding='utf-8') as endpoint_f:
                endpoint_f.write(endpoint_content)
            self.logger.success(f"Successfully generated Endpoint file - {endpoint_filename}")
        except TemplateNotFound:
            self.logger.error(f"Unable to find {ENDPOINT_TEMPLATE_NAME.absolute()}")
        except Exception as endpoint_creation_err:
            self.logger.error("Unable to generate Endpoint file - {endpoint_filename} due to {endpoint_creation_err}")


if __name__ == "__main__":
    arg_parser = ArgumentParser(prog="GenerateEndpointFile",
                                description="Generate Endpoint.py file from OpenAPI spec")
    arg_parser.add_argument("--spec",
                            dest="spec_file",
                            required=True,
                            help="Pass the location to the OpenAPI spec file, Passing this param alone will run a dry run of endpoint content generation with actually creating the endpoint")
    arg_parser.add_argument("--generate-endpoints",
                            dest='if_generate_endpoints',
                            action='store_true',
                            help="This param will create <endpoint_name>_Endpoint.py file for Path objects from the OpenAPI spec")

    args = arg_parser.parse_args()
    try:
        parser = OpenAPISpecParser(args.spec_file, logger)
        logger.debug(json.dumps(parser.parsed_dict, indent=4))
        if args.if_generate_endpoints:
            endpoint_generator = EndpointGenerator(logger)
            for module_name, file_content in parser.parsed_dict.items():
                for class_name, class_content in file_content.items():
                    endpoint_generator.generate_endpoint_file(module_name,
                                                            class_name,
                                                            class_content)
                    logger.success(f"Successfully generated Endpoint file - {module_name}")
    except Exception as ep_generation_err:
        raise ep_generation_err
