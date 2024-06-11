"""
This Endpoint file is generated using the api_auto_generator/endpoint_module_generator.py file
"""
class CarsEndpoint:


    def cars_url(self, suffix=''):
        "Append endpoint to base URI"
        return self.base_url + suffix


    def get_cars(self, headers):
        """
        Run get request against /cars
        :parameters:
         """
        url = self.cars_url(f"/cars")
        json_response = self.make_request(method='get', url=url, headers=headers)
        return {
            'url' : url,
            'response' : json_response['json_response']
            } 


    def post_cars_add(self, json, headers):
        """
        Run post request against /cars/add
        :parameters:
            :json: dict
                :name: str
                :brand: str
                :price_range: str
                :car_type: str
         """
        url = self.cars_url(f"/cars/add")
        json_response = self.make_request(method='post', url=url, json=json, headers=headers)
        return {
            'url' : url,
            'response' : json_response['json_response']
            } 


    def get_cars_find(self, params, headers):
        """
        Run get request against /cars/find
        :parameters:
            :params: dict
                :name: str
                :brand: str
         """
        url = self.cars_url(f"/cars/find")
        json_response = self.make_request(method='get', url=url, params=params, headers=headers)
        return {
            'url' : url,
            'response' : json_response['json_response']
            } 


    def get_cars_name(self, name, headers):
        """
        Run get request against /cars/{name}
        :parameters:
            :name: str
         """
        url = self.cars_url(f"/cars/{name}")
        json_response = self.make_request(method='get', url=url, headers=headers)
        return {
            'url' : url,
            'response' : json_response['json_response']
            } 


    def put_cars_update_name(self, name, json, headers):
        """
        Run put request against /cars/update/{name}
        :parameters:
            :name: str
            :json: dict
                :name: str
                :brand: str
                :price_range: str
                :car_type: str
         """
        url = self.cars_url(f"/cars/update/{name}")
        json_response = self.make_request(method='put', url=url, json=json, headers=headers)
        return {
            'url' : url,
            'response' : json_response['json_response']
            } 


    def delete_cars_remove_name(self, name, headers):
        """
        Run delete request against /cars/remove/{name}
        :parameters:
            :name: str
         """
        url = self.cars_url(f"/cars/remove/{name}")
        json_response = self.make_request(method='delete', url=url, headers=headers)
        return {
            'url' : url,
            'response' : json_response['json_response']
            } 


    def get_cars_filter_car_type(self, car_type, headers):
        """
        Run get request against /cars/filter/{car_type}
        :parameters:
            :car_type: str
         """
        url = self.cars_url(f"/cars/filter/{car_type}")
        json_response = self.make_request(method='get', url=url, headers=headers)
        return {
            'url' : url,
            'response' : json_response['json_response']
            } 


 