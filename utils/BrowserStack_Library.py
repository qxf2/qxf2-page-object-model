"""
First version of a library to interact with BrowserStack's artifacts.

For now, this is useful for:
a) Obtaining the session URL
b) Obtaining URLs of screenshots

To do:
a) Handle expired sessions better
"""

import os,requests,sys
from conf import remote_credentials as remote_credentials


class BrowserStack_Library():
    "BrowserStack library to interact with BrowserStack artifacts"
    def __init__(self):
        "Constructor for the BrowserStack library"
        self.browserstack_url = "https://www.browserstack.com/automate/"
        self.auth = self.get_auth()

    
    def get_auth(self):
        "Set up the auth object for the Requests library"
        USERNAME = remote_credentials.USERNAME
        PASSWORD = remote_credentials.ACCESS_KEY
        auth = (USERNAME,PASSWORD)

        return auth


    def get_build_id(self):
        "Get the build ID"
        self.build_url = self.browserstack_url + "builds.json"
        builds = requests.get(self.build_url, auth=self.auth).json()
        build_id =  builds[0]['automation_build']['hashed_id']
        
        return build_id


    def get_sessions(self):
        "Get a JSON object with all the sessions"
        build_id = self.get_build_id()
        sessions= requests.get(self.browserstack_url + 'builds/%s/sessions.json'%build_id, auth=self.auth).json()

        return sessions


    def get_active_session_id(self):
        "Return the session ID of the first active session"
        session_id = None
        sessions = self.get_sessions()
        for session in sessions:
            #Get session id of the first session with status = running 
            if session['automation_session']['status']=='running':
                session_id = session['automation_session']['hashed_id']
                break
                
        return session_id


    def get_session_url(self):
        "Get the session URL"
        build_id = self.get_build_id()
        session_id = self.get_active_session_id()
        session_url = self.browserstack_url + 'builds/%s/sessions/%s'%(build_id,session_id)

        return session_url


    def get_session_logs(self):
        "Return the session log in text format"
        build_id = self.get_build_id()
        session_id = self.get_active_session_id()
        session_log = requests.get(self.browserstack_url + 'builds/%s/sessions/%s/logs'%(build_id,session_id),auth=self.auth).text

        return session_log


    def get_latest_screenshot_url(self):
        "Get the URL of the latest screenshot"
        session_log = self.get_session_logs()
        
        #Process the text to locate the URL of the last screenshot
        #Extract the https://s2.amazonaws from example lines:
        #2016-2-9 4:42:39:52 RESPONSE {"state":"success","sessionId":"f77e1de6e4f42a72e6a6ecfd80ed07b95036ca35","hCode":29018101,"value":"https://s3.amazonaws.com/testautomation/f77e1de6e4f42a72e6a6ecfd80ed07b95036ca35/screenshot-selenium-b14d4ec62a.png","class":"org.openqa.selenium.remote.Response","status":0}
        #[2016-2-9 4:42:45:892] REQUEST [[2016-2-9 4:42:45:892]] GET /session/f77e1de6e4f42a72e6a6ecfd80ed07b95036ca35/title {}
        #2016-2-9 4:42:45:957 RESPONSE {"state":"success","sessionId":"f77e1de6e4f42a72e6a6ecfd80ed07b95036ca35","hCode":19687124,"value":"New Member Registration & Signup - Chess.com","class":"org.openqa.selenium.remote.Response","status":0}

        screenshot_request = session_log.split('screenshot {}')[-1]
        response_result = screenshot_request.split('REQUEST')[0]
        image_url = response_result.split('https://')[-1]
        image_url = image_url.split('.png')[0]
        screenshot_url = 'https://' + image_url + '.png'
        
        return screenshot_url
