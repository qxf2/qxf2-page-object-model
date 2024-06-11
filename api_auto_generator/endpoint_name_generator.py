"""
Module to generate:
    1. Module name
    2. Class name
    3. Method name
"""

import re
from typing import Union
from packaging.version import Version, InvalidVersion

class NameGenerator():
    "Base class for generating names"

    def __init__(self,
                 endpoint_url: str,
                 if_query_param: bool,
                 path_params: list,
                 requestbody_type: str):
        "Init NameGen object"
        self.endpoint_split, self.api_version_num = self.split_endpoint_string(endpoint_url)
        self.common_base = self.endpoint_split[0]
        self.endpoints_in_a_file = [ ep.capitalize() for ep in re.split("-|_", self.common_base)]
        self.if_query_param = if_query_param
        self.path_params = path_params
        self.requestbody_type = requestbody_type

    @property
    def module_name(self) -> str :
        "Module name for an Endpoint"
        return "_".join(self.endpoints_in_a_file) + "_" + "Endpoint"

    @property
    def class_name(self) -> str :
        "Class name for Endpoint"
        return "".join(self.endpoints_in_a_file) + "Endpoint"

    @property
    def url_method_name(self) -> str :
        "URL method name for endpoint"
        return self.common_base.lower().replace('-', '_') + "_" + "url"

    @property
    def base_api_param_string(self) -> str :
        "Base API method parameter string"
        param_string = ""
        if self.if_query_param:
            param_string += ", params=params"
        if self.requestbody_type == "json":
            param_string += ", json=json"
        if self.requestbody_type == "data":
            param_string += ", data=data"
        param_string += ", headers=headers"
        return param_string

    @property
    def instance_method_param_string(self) -> str :
        "Instance method parameter string"
        param_string = "self"
        if self.if_query_param:
            param_string += ", params"
        for param in self.path_params:
            param_string += f", {param[0]}"
        if self.requestbody_type == "json":
            param_string += ", json"
        if self.requestbody_type == "data":
            param_string += ", data"
        param_string += ', headers'
        return param_string

    def get_instance_method_name(self, http_method: str) -> str :
        "Generate Instance method name"
        endpoint_split = [ ep.lower().replace('-','_') for ep in self.endpoint_split ]
        return http_method + "_" + "_".join(endpoint_split)

    def split_endpoint_string(self, endpoint_url: str) -> tuple[list[str], Union[str,None]]:
        """
        Split the text in the endpoint, clean it up & return a list of text
        """
        version_num = None
        if endpoint_url == "/": # <- if the endpoint is only /
            endpoint_split = ["home_base"] # <- make it /home_base (it needs to be unique)
        else:
            endpoint_split = endpoint_url.split("/")
            # remove {} from path paramters in endpoints
            endpoint_split = [ re.sub("{|}","",text) for text in endpoint_split if text ]
            for split_values in endpoint_split:
                try:
                    if_api_version = Version(split_values) # <- check if version number present
                    version_num = [ str(num) for num in if_api_version.release ]
                    version_num = '_'.join(version_num)
                    endpoint_split.remove(split_values)
                except InvalidVersion:
                    if split_values == "api":
                        endpoint_split.remove(split_values)
        return (endpoint_split, version_num,)
