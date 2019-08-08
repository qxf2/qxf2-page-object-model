'''
This utility is for Custom Exceptions.

a) Stop_Test_Exception
You can raise a generic exceptions using just a string.
This is particularly useful when you want to end a test midway based on some condition.
'''

class Stop_Test_Exception(Exception):
    def __init__(self,message):
        self.message=message

    def __str__(self):
        return self.message