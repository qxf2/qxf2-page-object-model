"""
Base Mechanize class that all other pages can inherit from
There are useful wrappers for other common mechanize operations
The login method for droptask is included here. It will be moved to a page object later.
"""

import time, os, logging, sys, re, json, logging, mechanize, requests, urllib, urllib2, httplib
from utils.Base_Logging import Base_Logging
from Mechanize_Extended import Mechanize_Put
from Mechanize_Extended import Mechanize_Delete
import conf.url_conf as conf


class Borg:
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state


    def is_first_time(self):
        "Has the child class been invoked before?"
        result_flag = False
        if len(self.__dict__)== 0:
            result_flag = True

        return result_flag


class Base_Mechanize(Borg):
    "Main base class for Mechanize based scripts"
    def __init__(self,url=None):
        Borg.__init__(self)
        if self.is_first_time():
            #Do these actions if this the first time this class is initialized
            self.log_obj = Base_Logging(level=logging.DEBUG)
            self.reset(url=url)
    

    def reset(self,url=None):
        "Visit the URL given - usually URL is like https://www.client.com/"
        base_url = conf.base_url #Fetch the url from the conf file
        if base_url == None:
            print "NO URL GIVEN!" #Provide client url
        else:
            if base_url[1] == "/": #Removing trailing slash because a lot of the url we use later start with a slash
                base_url = base_url[:-1]
            self.base_url = base_url
        self.browser = mechanize.Browser()
        self.browser.set_handle_robots(False)


    def goto_url(self,url=None):
        "Visit a given url"
        response = None
        if url == None:
            print 'Cant goto a null url, will launch default url instead'
        else:
            response = self.browser.open(url)
        return response
    
    
    def get(self,url,headers={}):
        "Mechanize Get request"
        response = self.browser.open(mechanize.Request(url,headers=headers))
        return response
    

    def post(self,url,data=None,headers={}):
        "Mechanize Post request"
        response = self.browser.open(mechanize.Request(url=url, data= data, headers=headers))
        return response
    
        
    def delete(self,url):
        "Mechanize Delete request"
        response = self.browser.open(Mechanize_Delete(url))
        return response
    
    
    def put(self,url):
        "Mechanize Put request"
        response = self.browser.open(Mechanize_Put(url, data=data, headers=headers))
        return response
    

    def write(self,msg,level='info'):
        " This method use the logging method"
        self.log_obj.write(msg,level)


    def get_url(self,key):
        "fetches locator from the locator conf"
        value = None
        try:
            path_conf_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'conf', 'url.conf'))
            if path_conf_file is not None:
                value = Conf_Reader.get_value(path_conf_file, key)
        except Exception,e:
            print str(e)

        return value

    #Methods specific to the droptask test.To be moved to a pageobject later.
    def login(self,username,password):
        " Login to Droptask "
        login_redirect = conf.login_redirect
        login_url = conf.base_url+login_redirect #Fetch url from conf file and concatenate '/login' to the base url
        my_params = {'email':username,'password':password}
        params_encoded = urllib.urlencode(my_params)
        self.browser.method='POST'
        headers = {'Host': 'auth.droptask.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:46.0) Gecko/20100101 Firefox/46.0','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language': 'en-US,en;q=0.5','Accept-Encoding': 'gzip, deflate, br','Referer': 'https://auth.droptask.com/login?continue=https%3A%2F%2Fapp.droptask.com%2Fauth&clientId=5c8af5ea-fa7c-4cb3-80e8-04b361d9e297&source=web','Cookie':' _ga=GA1.2.2000288028.1449634785; connect.sid=s%3A08sLYE3zBHEDS4T72OeDhDzqUCW-MNxB.bU6Bdt5xDsHeg6yIyIQKPmL4NG%2BgqRaBOMTMkax44N0','Connection': 'keep-alive'}
        login_response = self.post(url=login_url,data=params_encoded,headers=headers)
        forms = mechanize.ParseResponse(login_response, backwards_compat=False)   
        result_flag = False 
        if (len(forms)!= 0) and (forms[0].find_control("password") != None):
            self.write("    -Login failed")
            result_flag = False
        else:
            self.write("    -Login success")
            result_flag = True

        return result_flag


    






    



        


  
