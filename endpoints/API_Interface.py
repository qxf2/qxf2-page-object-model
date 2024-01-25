import requests
from .Base_API import Base_API

try:
    from .Cars_API_Endpoints import Cars_API_Endpoints
except ImportError:
    Cars_API_Endpoints = object

class API_Interface(Base_API,Cars_API_Endpoints):
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