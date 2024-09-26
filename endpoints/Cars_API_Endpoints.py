"""
API endpoints for Cars
"""
class Cars_API_Endpoints:
	"Class for cars endpoints"

	def cars_url(self,suffix=''):
		"""Append API end point to base URL"""
		return self.base_url+'/cars'+suffix


	def add_car(self,data,headers):
		"Adds a new car"
		try:
			url = self.cars_url('/add')
			json_response = self.post(url,json=data,headers=headers)
		except Exception as e:
			print("Python says:%s" % str(e))
			json_response = None
		return {
			'url':url,
			'response':json_response.json()
		}


	def get_cars(self,headers):
		"gets list of cars"
		try:
			url = self.cars_url()
			json_response = self.get(url,headers=headers)
		except Exception as e:
			print("Python says:%s" % str(e))
			json_response = None
		return {
			'url':url,
			'response':json_response.json()
		}


	def get_car(self,url_params,headers):
		"gets given car details"
		try:
			url = self.cars_url('/find?')+url_params
			json_response = self.get(url,headers=headers)
		except Exception as e:
			print("Python says:%s" % str(e))
			json_response = None
		return {
			'url':url,
			'response':json_response.json()
		}


	def update_car(self,car_name,json,headers):
		"updates a given car"
		try:
			url = self.cars_url('/update/%s'%car_name)
			json_response =self.put(url,json=json,headers=headers)
		except Exception as e:
			print("Python says:%s" % str(e))
			json_response = None
		return {
			'url':url,
			'response':json_response.json()
		}


	def remove_car(self,car_name,headers):
		"deletes a car entry"
		try:
			url =self.cars_url('/remove/%s'%car_name)
			json_response = self.delete(url,headers=headers)
		except Exception as e:
			print("Python says:%s" % str(e))
			json_response = None
		return{
			'url':url,
			'response':json_response.json()
		}

	# Async methods
	async def get_cars_async(self,headers):
		"Get the list of cars"
		url = self.cars_url()
		response = await self.async_get(url,headers=headers)
		return response


	async def add_car_async(self,data,headers):
		"Add a new car"
		url = self.cars_url('/add')
		response = await self.async_post(url,json=data,headers=headers)
		return response


	async def get_car_async(self,url_params,headers):
		"Get car using URL params"
		url = self.cars_url('/find?')+url_params
		response = await self.async_get(url,headers=headers)
		return response

