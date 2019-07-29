'''
This utility is for converting string to integer.

a)string_to_int()
This is particularly useful when you want convert string to integer.
'''

class string_to_int():
    def string_to_int(str_var)
        try:
            str_var = int(str_var)
        except Exception as e:
            self.write("Error type casting var to int",level="error")
            self.write("Obtained the str_var %s"%str_var)
            self.write("Python says: " + str(e))
            return str_var

    return string_to_int