"""
API endpoints for Registration
"""
from .base_api import BaseAPI

class UserAPIEndpoints(BaseAPI):
    "Class for user endpoints"
    def user_url(self,suffix=''):
        """Append API end point to base URL"""
        return self.base_url+'/users'+suffix
    def get_user_list(self,headers):
        "get users list"
        try:
            url = self.user_url('')
            json_response = self.get(url,headers=headers)
        except Exception as err: # pylint: disable=broad-exception-caught
            print(f"Python says: {err}")
            json_response = None
        return {
                'url':url,
                'response':json_response.status_code,
				'user_list':json_response.json()
                }
