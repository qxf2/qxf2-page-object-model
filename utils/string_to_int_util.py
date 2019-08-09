'''
This utility is for converting string to integer.

a)string_to_int()
This is particularly useful when you want convert string to integer.
'''

class string_to_int():
      
    def string_to_int(str_var):
        try:
            int_var = int(str_var)
        except Exception as e:
            print("Error type casting var to int")
            print("Obtained the %s"%str_var)
            print("Python says: " + str(e))
            return str_var
        return int_var