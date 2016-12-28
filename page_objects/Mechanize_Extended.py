"""
Mechanize Extended class to overwrite the get_method() in Request class to perform DELETE and PUT requests
refer- http://stackoverflow.com/questions/13810547/http-put-method-in-python-mechanize/23404541?noredirect=1#comment62723398_23404541
"""

import mechanize


class Mechanize_Delete(mechanize.Request):
    "Extend the mechanize Request class to allow a http DELETE"
    def get_method(self):
        return "DELETE"


class Mechanize_Put(mechanize.Request):
	"Extend the Mechanize request class to allow a http PUT"
	def get_method(self):
		return "PUT"