"""
API endpoints for Cars 
"""

from .Base_API import Base_API
import json

class Cars_API_Endpoints(Base_API):
	"Class for cars endpoints"

	def cars_url(self,suffix=''):
		"""Append API end point to base URL"""
		return self.base_url+'/cars'+suffix


	def add_car(self,data,headers):
		"Adds a new car"
		url = self.cars_url('/add')
		json_response = self.post(url,json=data,headers=headers)
		return {
			'url':url,
			'response':json_response['json_response']
		}


	def get_cars(self,headers):
		"gets list of cars"
		url = self.cars_url()
		json_response = self.get(url,headers=headers)
		return {
			'url':url,
			'response':json_response['json_response']
		}


	def get_car(self,url_params,headers):
		"gets given car details"
		url = self.cars_url('/find?')+url_params
		json_response = self.get(url,headers=headers)
		return {
			'url':url,
			'response':json_response['json_response']
		}
	

	def update_car(self,car_name,json,headers):
		"updates a given car"
		url = self.cars_url('/update/%s'%car_name)
		json_response =self.put(url,json=json,headers=headers)
		return {
			'url':url,
			'response':json_response['json_response']
		}
		
	
	def remove_car(self,car_name,headers):
		"deletes a car entry"
		url =self.cars_url('/remove/%s'%car_name)
		json_response = self.delete(url,headers=headers)
		return{
			'url':url,
			'response':json_response['json_response']
		}