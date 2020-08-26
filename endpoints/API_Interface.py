"""
A composed interface for all the API objects
Use the API_Player to talk to this class
"""
from .Cars_API_Endpoints import Cars_API_Endpoints
from .Registration_API_Endpoints import Registration_API_Endpoints
from .User_API_Endpoints import User_API_Endpoints

class API_Interface(Cars_API_Endpoints,Registration_API_Endpoints,User_API_Endpoints):
	"A composed interface for the API objects"

	def __init__(self, url):
		"Constructor"
		# make base_url available to all API endpoints
		self.base_url = url
