"""
API endpoints for Registration
"""

class User_API_Endpoints:
	"Class for user endpoints"

	def user_url(self,suffix=''):
		"""Append API end point to base URL"""
		return self.base_url+'/users'+suffix


	def get_user_list(self,headers):
		"get users list"
		url = self.user_url('')
		json_response = self.get(url,headers=headers)
		return {
                'url':url,
                'response':json_response['response'],
                'error':json_response['error'],
				'user_list':json_response['json_response']
                }





