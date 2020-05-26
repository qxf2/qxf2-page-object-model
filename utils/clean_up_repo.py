"""
The Qxf2 automation repository ships with example tests.
Run this file to delete all the example files and start fresh with your example.
After this script runs, you will need to edit a few files to configure them to suit your own repository
Usage: python clean_up_repo.py
"""
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import clean_up_repo_conf as conf

def delete_file(file_name):
    "The method will delete a particular file"
    if os.path.exists(file_name):
        os.remove(file_name)
        print(f'{file_name} deleted')


def delete_files_in_dir(directory, files):
    "The method will delete files in a particular directory"
    for file_name in files:
        delete_file(os.path.join(directory, file_name))


def delete_files_used_in_example():
    "The method will delete set of files"
    #Files mentioned are in the blog post: https://qxf2.com/bloghow-to-start-using-the-qxf2-framework-with-a-new-project/"
    for every_dir_list, every_file_list in zip(conf.dir_list, conf.file_list):
        delete_files_in_dir(every_dir_list, every_file_list)


#---USAGE EXAMPLES
if __name__ == "__main__":
    print("Running utility to delete the files")
    delete_files_used_in_example()
    print(f'All the files related to the sample example from Page Object Model have been removed from {conf.dir_list} folders.\n For next steps, please refer to the edit files section of this blog post: https://qxf2.com/blog/how-to-start-using-the-qxf2-framework-with-a-new-project/')