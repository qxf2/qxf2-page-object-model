"""
A composed interface for all the API objects
Use the API_Player to talk to this class
"""
import requests
from .Base_API import Base_API
from .Cars_API_Endpoints import Cars_API_Endpoints
from .Registration_API_Endpoints import Registration_API_Endpoints
from .User_API_Endpoints import User_API_Endpoints

class API_Interface(Base_API,Cars_API_Endpoints,Registration_API_Endpoints,User_API_Endpoints):
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
