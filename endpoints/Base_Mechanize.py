"""
A wrapper around Mechanize to make Restful API calls
"""

import json
import mechanize


class Base_Mechanize:
    "Main base class for Mechanize based scripts"

    def __init__(self, url=None):
        pass

    def get_browser(self):
        "Create and return a browser object"
        browser = mechanize.Browser()
        browser.set_handle_robots(False)

        return browser

    def get(self, url, headers={}):
        "Mechanize Get request"
        browser = self.get_browser()
        request_headers = []
        response = {}
        error = {}
        for key, value in headers.iteritems():
            request_headers.append((key, value))
            browser.addheaders = request_headers
        try:
            response = browser.open(mechanize.Request(url))
            response = json.loads(response.read())
        except (mechanize.HTTPError, mechanize.URLError) as e:
            error = e
            if isinstance(e, mechanize.HTTPError):
                error_message = e.read()
                print("\n******\nGET Error: %s %s" %
                      (url, error_message))
            else:
                print(e.reason.args)
            # bubble error back up after printing relevant details
                raise e

        return {'response': response, 'error': error}

    def post(self, url, data=None, headers={}):
        "Mechanize Post request"
        browser = self.get_browser()
        response = {}
        error = {}
        try:
            response = browser.open(mechanize.Request(
                url=url, data=data, headers=headers))
        except (mechanize.HTTPError, mechanize.URLError) as e:
            error = e
            if isinstance(e, mechanize.HTTPError):
                error_message = e.read()
                print("\n******\nPOST Error: %s %s %s" %
                      (url, error_message, str(data)))
            else:
                print(e.reason.args)
            # bubble error back up after printing relevant details
            raise e

        return {'response': response, 'error': error}

    def delete(self, url, headers={}):
        "Mechanize Delete request"
        browser = self.get_browser()
        response = False
        error = {}
        try:
            browser.open(Mechanize_Delete_Request_class(url, headers=headers))
            response = True
        except Exception, e:
            print("Exception in Mechanize_Delete_request: %s" % str(e))
            raise e

        return {'response': response, 'error': error}

    def put(self, url, data=None, headers={}):
        "Mechanize Put request"
        browser = self.get_browser()
        response = {}
        error = {}
        try:
            response = browser.open(Mechanize_Put_Request_class(
                url, data=data, headers=headers))
        except (mechanize.HTTPError, mechanize.URLError) as e:
            error = e
            if isinstance(e, mechanize.HTTPError):
                error_message = e.read()
                print("\n******\nPUT Error: %s %s %s" %
                      (url, error_message, str(data)))
            else:
                print(str(e.reason.args))
            # bubble error back up after printing relevant details
            raise e

        return {'response': response, 'error': error}


class Mechanize_Put_Request_class(mechanize.Request):
    "Extend the mechanize Request class to allow a http PUT"

    def get_method(self):
        return "PUT"


class Mechanize_Delete_Request_class(mechanize.Request):
    "Extend the mechanize Request class to allow a http DELETE"

    def get_method(self):
        return "DELETE"
