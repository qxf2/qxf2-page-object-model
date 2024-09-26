
"""
API endpoints for Registration
"""

class Registration_API_Endpoints:
	"Class for registration endpoints"

	def registration_url(self,suffix=''):
		"""Append API end point to base URL"""
		return self.base_url+'/register/'+suffix


	def register_car(self,url_params,json,headers):
		"register car "
		try:
			url = self.registration_url('car?')+url_params
			json_response = self.post(url,params=url_params,json=json,headers=headers)
		except Exception as e:
			print("Python says:%s" % str(e))
			json_response = None
		return {
			'url':url,
			'response':json_response.json()
		}


	def get_registered_cars(self,headers):
		"gets registered cars"
		try:
			url = self.registration_url('')
			json_response = self.get(url,headers=headers)
		except Exception as e:
			print("Python says:%s" % str(e))
			json_response = None
		return {
			'url':url,
			'response':json_response.json()
		}


	def delete_registered_car(self,headers):
		"deletes registered car"
		try:
			url = self.registration_url('car/delete/')
			json_response = self.delete(url,headers)
		except Exception as e:
			print("Python says:%s" % str(e))
			json_response = None
		return {
		'url':url,
		'response':json_response.json()
		}


	# Async methods
	async def get_registered_cars_async(self,headers):
		"Get registered cars"
		url = self.registration_url('')
		response = await self.async_get(url,headers=headers)
		return response

