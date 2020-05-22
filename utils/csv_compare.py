"""
Qxf2 Services: Utility script to compare two csv files.

"""
import csv,os

class Csv_Compare():
    def is_equal(self,csv_actual,csv_expected):
        "Method to compare the Actual and Expected csv file"
        result_flag = True

        if not os.path.exists(csv_actual):
            result_flag = False
            print('Could not locate the csv file: %s'%csv_actual)

        if not os.path.exists(csv_expected):
            result_flag = False
            print('Could not locate the csv file: %s'%csv_expected)

        if os.path.exists(csv_actual) and os.path.exists(csv_expected):
            #Open the csv file and put the content to list
            with open(csv_actual, 'r') as actual_csvfile, open(csv_expected, 'r') as exp_csvfile:
                reader = csv.reader(actual_csvfile)
                actual_file = [row for row in reader]
                reader = csv.reader(exp_csvfile)
                exp_file = [row for row in reader]

            if (len(actual_file)!= len(exp_file)):
                result_flag = False
                print("Mismatch in number of rows. The actual row count didn't match with expected row count")
            else:
                for actual_row, actual_col in zip(actual_file,exp_file):
                    if actual_row == actual_col:
                        pass
                    else:
                        print("Mismatch between actual and expected file at Row: ",actual_file.index(actual_row))
                        print("Row present only in Actual file: %s"%actual_row)
                        print("Row present only in Expected file: %s"%actual_col)
                        result_flag =  False

        return result_flag


#---USAGE EXAMPLES
if __name__=='__main__':
    print("Start of %s"%__file__)

    #Fill in the file1 and file2 paths
    file1 = 'Add path for the first file here'
    file2 = 'Add path for the second file here'

    #Initialize the csv object
    csv_obj = Csv_Compare()

    #Sample code to compare csv files
    if csv_obj.is_equal(file1,file2) is True:
        print("Data matched in both the csv files\n")
    else:
        print("Data mismatch between the actual and expected csv files")
