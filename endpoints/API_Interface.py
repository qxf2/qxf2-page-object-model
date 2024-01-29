"""
A composed interface for all the API objects
Use the API_Player to talk to this class
"""

import requests
from .Base_API import Base_API

base_classes = [Base_API]

try:
    from .Cars_API_Endpoints import Cars_API_Endpoints
    base_classes.append(Cars_API_Endpoints)
except ImportError:
    pass

try:
    from .Registration_API_Endpoints import Registration_API_Endpoints
    base_classes.append(Registration_API_Endpoints)
except ImportError:
    pass

try:
    from .User_API_Endpoints import User_API_Endpoints
    base_classes.append(User_API_Endpoints)
except ImportError:
    pass

class API_Interface(*base_classes):
	"A composed interface for the API objects"

	def __init__(self, url, session_flag=False):
		"Constructor"
		# make base_url available to all API endpoints
		self.request_obj = requests
		if session_flag:
			self.create_session()
		self.base_url = url

	def create_session(self):
		"Create a session object"
		self.request_obj = requests.Session()

		return self.request_obj