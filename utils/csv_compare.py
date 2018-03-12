"""
This script can be used to compare two csv files
"""

import csv,os

class Csv_Compare():
    def is_equal(self,csv_actual,csv_expected):
        "Method to compare the Actual and Expected csv file"
        result_flag = True

        if not os.path.exists(csv_actual):
            result_flag = False
            print 'Could not locate the generated csv: %s'%csv_actual

        if not os.path.exists(csv_expected):
            result_flag = False
            print 'Could not locate the baseline csv: %s'%csv_expected

        if os.path.exists(csv_actual) and os.path.exists(csv_expected):
            #Open the csv file and put the content to list
            with open(csv_actual, 'r') as actual_csvfile, open(csv_expected, 'r') as exp_csvfile:
                reader = csv.reader(actual_csvfile)
                actual_file = [row for row in reader]
                reader = csv.reader(exp_csvfile)
                exp_file = [row for row in reader]

            if (len(actual_file)!= len(exp_file)):
                result_flag = False
                print "Mismatch in number of rows. The actual row count didnt match expected row count"
            else:
                for actual_row, actual_col in zip(actual_file,exp_file):
                    if actual_row == actual_col:
                        pass
                    else:
                        print "Mismatch between actual and expected file at Row: ",actual_file.index(actual_row)
                        print "Row present only in Actual file: %s"%actual_row
                        print "Row present only in Expected file: %s"%actual_col
                        result_flag =  False

        return result_flag


#---USAGE EXAMPLES
if __name__=='__main__':
    print "Start of %s"%__file__
     
    file1 = 'c:/Indira/sample/file1.csv'
    file2 = 'c:/Indira/sample/file2.csv'
    #Initialize the csv object
    csv_obj = Csv_Compare()

    #Sample code to compare csv files
    if csv_obj.is_equal(file1,file2) is True:
        print "Data in both the csv files matched\n"
    else:
        print "Data mismatch in both the csv files"    
