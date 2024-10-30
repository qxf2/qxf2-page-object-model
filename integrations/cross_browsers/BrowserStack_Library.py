"""
First version of a library to interact with BrowserStack's artifacts.

For now, this is useful for:
a) Obtaining the session URL
b) Obtaining URLs of screenshots

To do:
a) Handle expired sessions better
"""
import os
import requests
from conf import remote_url_conf

class BrowserStack_Library():
    "BrowserStack library to interact with BrowserStack artifacts"
    def __init__(self):
        "Constructor for the BrowserStack library"
        self.browserstack_api_server_url = remote_url_conf.browserstack_api_server_url
        self.browserstack_cloud_api_server_url = remote_url_conf.browserstack_cloud_api_server_url
        self.auth = self.get_auth()


    def get_auth(self):
        "Set up the auth object for the Requests library"
        USERNAME = os.getenv('REMOTE_USERNAME')
        PASSWORD = os.getenv('REMOTE_ACCESS_KEY')
        auth = (USERNAME,PASSWORD)

        return auth


    def get_build_id(self,timeout=10):
        "Get the build ID"
        build_url = self.browserstack_api_server_url + "/builds.json?status=running"
        builds = requests.get(build_url, auth=self.auth, timeout=timeout).json()
        build_id =  builds[0]['automation_build']['hashed_id']

        return build_id


    def get_sessions(self,timeout=10):
        "Get a JSON object with all the sessions"
        build_id = self.get_build_id()
        sessions= requests.get(f'{self.browserstack_api_server_url}/builds/{build_id}/sessions.json?browserstack_status=running', auth=self.auth, timeout=timeout).json()

        return sessions


    def get_active_session_details(self):
        "Return the session ID of the first active session"
        session_details = None
        sessions = self.get_sessions()
        for session in sessions:
            #Get session id of the first session with status = running
            if session['automation_session']['status']=='running':
                session_details = session['automation_session']
                #session_id = session['automation_session']['hashed_id']
                #session_url = session['automation_session']['browser_url']
                break

        return session_details

    def extract_session_id(self, session_url):
        "Extract session id from session url"
        import re
        # Use regex to match the session ID, which is a 40-character hexadecimal string
        match = re.search(r'/sessions/([a-f0-9]{40})', session_url)
        if match:
            return match.group(1)
        else:
            return None

    def upload_terminal_logs(self, file_path, session_id = None, appium_test = False, timeout=30):
        "Upload the terminal log to BrowserStack"
        try:
            # Get session ID if not provided
            if session_id is None:
                session_details = self.get_active_session_details()
                session_id = session_details['hashed_id']
                if not session_id:
                    raise ValueError("Session ID could not be retrieved. Check active session details.")

            # Determine the URL based on the type of test
            if appium_test:
                url = f'{self.browserstack_cloud_api_server_url}/app-automate/sessions/{session_id}/terminallogs'
            else:
                url = f'{self.browserstack_cloud_api_server_url}/automate/sessions/{session_id}/terminallogs'

            # Open the file using a context manager to ensure it is properly closed
            with open(file_path, 'rb') as file:
                files = {'file': file}
                # Make the POST request to upload the file
                response = requests.post(url, auth=self.auth, files=files, timeout=timeout)

            # Check if the request was successful
            if response.status_code == 200:
                print("Log file uploaded to BrowserStack session successfully.")
            else:
                print(f"Failed to upload log file. Status code: {response.status_code}")
                print(response.text)

            return response

        except FileNotFoundError as e:
            print(f"Error: Log file '{file_path}' not found.")
            return {"error": "Log file not found.", "details": str(e)}

        except ValueError as e:
            print(f"Error: {str(e)}")
            return {"error": "Invalid session ID.", "details": str(e)}

        except requests.exceptions.RequestException as e:
            # Handle network-related errors
            print(f"Error: Failed to upload log file to BrowserStack. Network error: {str(e)}")
            return {"error": "Network error during file upload.", "details": str(e)}

        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred: {str(e)}")
            return {"error": "Unexpected error occurred during file upload.", "details": str(e)}
