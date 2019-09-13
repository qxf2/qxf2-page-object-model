'''
Qxf2 Services: This utility is for converting string to integer.
string_to_int(): This is particularly useful when you want to convert any string to integer.
'''

class String_To_Int():
    "Class to convert string to integer"
      
    def string_to_int(self,str_var):
        "Method to convert string to integer"
        try:
            int_var = int(str_var)
        except Exception as e:
            print("Error type casting var to int")
            print("Obtained the %s"%int_var)
            print("Python says: " + str(e))
            return str_var
        return int_var