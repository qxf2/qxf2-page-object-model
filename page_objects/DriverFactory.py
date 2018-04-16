"""
DriverFactory class
NOTE: Change this class as you add support for:
1. SauceLabs/BrowserStack
2. More browsers like Opera
"""
import dotenv,os,sys,requests,json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.webdriver import RemoteConnection
from appium import webdriver as mobile_webdriver
from conf import remote_credentials

class DriverFactory():
    
    def __init__(self,browser='ff',browser_version=None,os_name=None):
        "Constructor for the Driver factory"
        self.browser=browser
        self.browser_version=browser_version
        self.os_name=os_name

        
    def get_web_driver(self,remote_flag,os_name,os_version,browser,browser_version):
        "Return the appropriate driver"
        if (remote_flag.lower() == 'y'):
            try:
                if remote_credentials.REMOTE_BROWSER_PLATFORM == 'BS':
                    web_driver = self.run_browserstack(os_name,os_version,browser,browser_version)
                else:
                    web_driver = self.run_sauce_lab(os_name,os_version,browser,browser_version)
                    
            except Exception,e:
                print "\nException when trying to get remote webdriver:%s"%sys.modules[__name__]
                print "Python says:%s"%str(e)
                print "SOLUTION: It looks like you are trying to use a cloud service provider (BrowserStack or Sauce Labs) to run your test. \nPlease make sure you have updated ./conf/remote_credentials.py with the right credentials and try again. \nTo use your local browser please run the test with the -M N flag.\n"
                
        elif (remote_flag.lower() == 'n'):
                web_driver = self.run_local(os_name,os_version,browser,browser_version)       
        else:
            print "DriverFactory does not know the browser: ",browser
            web_driver = None

        return web_driver   
    

    def run_browserstack(self,os_name,os_version,browser,browser_version):
        "Run the test in browser stack when remote flag is 'Y'"
        #Get the browser stack credentials from browser stack credentials file
        USERNAME = remote_credentials.USERNAME
        PASSWORD = remote_credentials.ACCESS_KEY
        if browser.lower() == 'ff' or browser.lower() == 'firefox':
            desired_capabilities = DesiredCapabilities.FIREFOX            
        elif browser.lower() == 'ie':
            desired_capabilities = DesiredCapabilities.INTERNETEXPLORER
        elif browser.lower() == 'chrome':
            desired_capabilities = DesiredCapabilities.CHROME            
        elif browser.lower() == 'opera':
            desired_capabilities = DesiredCapabilities.OPERA        
        elif browser.lower() == 'safari':
            desired_capabilities = DesiredCapabilities.SAFARI

        desired_capabilities['os'] = os_name
        desired_capabilities['os_version'] = os_version
        desired_capabilities['browser_version'] = browser_version
        
        return webdriver.Remote(RemoteConnection("http://%s:%s@hub-cloud.browserstack.com/wd/hub"%(USERNAME,PASSWORD),resolve_ip= False),
            desired_capabilities=desired_capabilities)
    

    def run_sauce_lab(self,os_name,os_version,browser,browser_version):
        "Run the test in sauce labs when remote flag is 'Y'"
        #Get the sauce labs credentials from sauce.credentials file
        USERNAME = remote_credentials.USERNAME
        PASSWORD = remote_credentials.ACCESS_KEY
        if browser.lower() == 'ff' or browser.lower() == 'firefox':
            desired_capabilities = DesiredCapabilities.FIREFOX            
        elif browser.lower() == 'ie':
            desired_capabilities = DesiredCapabilities.INTERNETEXPLORER
        elif browser.lower() == 'chrome':
            desired_capabilities = DesiredCapabilities.CHROME            
        elif browser.lower() == 'opera':
            desired_capabilities = DesiredCapabilities.OPERA        
        elif browser.lower() == 'safari':
            desired_capabilities = DesiredCapabilities.SAFARI
        desired_capabilities['version'] = browser_version
        desired_capabilities['platform'] = os_name + ' '+os_version
        
        
        return webdriver.Remote(command_executor="http://%s:%s@ondemand.saucelabs.com:80/wd/hub"%(USERNAME,PASSWORD),
                desired_capabilities= desired_capabilities)


    def run_local(self,os_name,os_version,browser,browser_version):
        "Return the local driver"
        local_driver = None
        if browser.lower() == "ff" or browser.lower() == 'firefox':
            local_driver = webdriver.Firefox()    
        elif  browser.lower() == "ie":
            local_driver = webdriver.Ie()
        elif browser.lower() == "chrome":
            local_driver = webdriver.Chrome('C:\Python27\Scripts\chromedriver.exe')
        elif browser.lower() == "opera":
            local_driver = webdriver.Opera()
        elif browser.lower() == "safari":
            local_driver = webdriver.Safari()

        return local_driver


    def run_mobile(self,mobile_os_name,mobile_os_version,device_name,app_package,app_activity,remote_flag,device_flag,app_name):
        "Setup mobile device"
        #Get the remote credentials from remote_credentials file
        USERNAME = remote_credentials.USERNAME
        PASSWORD = remote_credentials.ACCESS_KEY
        desired_capabilities = {}
        desired_capabilities['platformName'] = mobile_os_name
        desired_capabilities['platformVersion'] = mobile_os_version
        desired_capabilities['deviceName'] = device_name

        if (remote_flag.lower() == 'y'):
            desired_capabilities['idleTimeout'] = 300
            desired_capabilities['name'] = 'Appium Python Test'

            try:
                if remote_credentials.REMOTE_BROWSER_PLATFORM == 'SL':
                    self.sauce_upload(app_name) #Saucelabs expects the app to be uploaded to Sauce storage everytime the test is run
                    desired_capabilities['app'] = 'sauce-storage:'+app_name
                    desired_capabilities['autoAcceptAlert']= 'true'

                    driver = mobile_webdriver.Remote(command_executor="http://%s:%s@ondemand.saucelabs.com:80/wd/hub"%(USERNAME,PASSWORD),
                        desired_capabilities= desired_capabilities)

                else:
                    desired_capabilities['realMobile'] = 'true'
                    desired_capabilities['app'] = self.browser_stack_upload(app_name) #upload the application to the Browserstack Storage
                                    
                    driver = mobile_webdriver.Remote(command_executor="http://%s:%s@hub.browserstack.com:80/wd/hub"%(USERNAME,PASSWORD),
                        desired_capabilities= desired_capabilities)
            except Exception,e:
                print "\nException when trying to get remote webdriver:%s"%sys.modules[__name__]
                print "Python says:%s"%str(e)
                print "SOLUTION: It looks like you are trying to use a cloud service provider (BrowserStack or Sauce Labs) to run your test. \nPlease make sure you have updated ./conf/remote_credentials.py with the right credentials and try again. \nTo use your local browser please run the test with the -M N flag.\n"
        else:
            desired_capabilities['appPackage'] = app_package
            desired_capabilities['appActivity'] = app_activity
            if device_flag.lower() == 'y':
                driver = mobile_webdriver.Remote('http://localhost:4723/wd/hub', desired_capabilities)
            else:
                desired_capabilities['app'] = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','app',app_name))
                driver = mobile_webdriver.Remote('http://localhost:4723/wd/hub', desired_capabilities)

        return driver


    def sauce_upload(self,app_name):  
        "Upload the apk to the sauce temperory storage"
        USERNAME = remote_credentials.USERNAME
        PASSWORD = remote_credentials.ACCESS_KEY
        headers = {'Content-Type':'application/octet-stream'}
        params = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','app',app_name)) 
        fp = open(params,'rb')
        data = fp.read()
        fp.close()
        response = requests.post('https://saucelabs.com/rest/v1/storage/%s/%s?overwrite=true'%(USERNAME,app_name),headers=headers,data=data,auth=(USERNAME,PASSWORD)) 


    def browser_stack_upload(self,app_name):
        "Upload the apk to the BrowserStack storage if its not done earlier"
        USERNAME = remote_credentials.USERNAME
        ACESS_KEY = remote_credentials.ACCESS_KEY
        app_url = None 
        try:
            # Check if the apk file already present
            get_response = requests.get("https://api.browserstack.com/app-automate/recent_apps",auth=(USERNAME,ACESS_KEY))
            # If the apk is already present get the app url
            if len(get_response.json()) != 0:
                get_json_data = json.loads(get_response.text)
                app_url = get_json_data[0]['app_url']
            # If the apk is not already present Upload the apk            
            if app_url == None:
                apk_file = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','app',app_name))
                files = {'file': open(apk_file,'rb')}
                post_response = requests.post("https://api.browserstack.com/app-automate/upload",files=files,auth=(USERNAME,ACESS_KEY))
                post_json_data = json.loads(post_response.text)
                # Get the app url of the newly uploaded apk
                app_url = post_json_data['app_url']            
        except Exception as e:
            print str(e)

        return app_url
                

    def get_firefox_driver(self):
        "Return the Firefox driver"
        driver = webdriver.Firefox(firefox_profile=self.get_firefox_profile())

        return driver 


    def get_firefox_profile(self):
        "Return a firefox profile"

        return self.set_firefox_profile()

    
    def set_firefox_profile(self):
        "Setup firefox with the right preferences and return a profile"
        try:
            self.download_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','downloads'))
            if not os.path.exists(self.download_dir):
                os.makedirs(self.download_dir)
        except Exception,e:
            print("Exception when trying to set directory structure")
            print(str(e))
            
        profile = webdriver.firefox.firefox_profile.FirefoxProfile()
        set_pref = profile.set_preference
        set_pref('browser.download.folderList', 2)
        set_pref('browser.download.dir', self.download_dir)
        set_pref('browser.download.useDownloadDir', True)
        set_pref('browser.helperApps.alwaysAsk.force', False)
        set_pref('browser.helperApps.neverAsk.openFile', 'text/csv,application/octet-stream,application/pdf')
        set_pref('browser.helperApps.neverAsk.saveToDisk', 'text/csv,application/vnd.ms-excel,application/pdf,application/csv,application/octet-stream')
        set_pref('plugin.disable_full_page_plugin_for_types', 'application/pdf')
        set_pref('pdfjs.disabled',True)

        return profile

