"""
A composed Interface for all the Endpoint abstraction objects:
    * Cars API Endpoints
    * Registration API Endpoints
    * User API Endpoints
The APIPlayer Object interacts only to the Interface to access the Endpoint
"""

from .cars_api_endpoints import CarsAPIEndpoints
from .registration_api_endpoints import RegistrationAPIEndpoints
from .user_api_endpoints import UserAPIEndpoints

class APIInterface(CarsAPIEndpoints, RegistrationAPIEndpoints, UserAPIEndpoints):
    "A composed interface for the API objects"

    def __init__(self, url):
        "Initialize the Interface"
        self.base_url = url
