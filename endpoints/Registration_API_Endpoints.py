
"""
API endpoints for Registration 
"""

from .Base_API import Base_API

class Registration_API_Endpoints(Base_API):
	"Class for registration endpoints"

	def registration_url(self,suffix=''):
		"""Append API end point to base URL"""
		return self.base_url+'/register/'+suffix


	def register_car(self,url_params,json,headers):
		"register car "
		url = self.registration_url('car?')+url_params
		json_response = self.post(url,params=url_params,json=json,headers=headers)
		return {
			'url':url,
			'response':json_response['json_response']
		}


	def get_registered_cars(self,headers):
		"gets registered cars"
		url = self.registration_url('')
		json_response = self.get(url,headers=headers)
		return {
			'url':url,
			'response':json_response['json_response']
		}


	def delete_registered_car(self,headers):
		"deletes registered car"
		url = self.registration_url('car/delete/')
		json_response = self.delete(url,headers)
		return {
		'url':url,
		'response':json_response['json_response']
		}
