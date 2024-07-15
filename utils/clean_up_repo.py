"""
The Qxf2 automation repository ships with example tests.
Run this file to delete all the example files and start fresh with your example.
Usage: python clean_up_repo.py
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import clean_up_repo_conf as conf
from utils.Base_Logging import Base_Logging

class CleanUpRepo:
    """Utility for cleaning up example files."""
    def __init__(self):
        """Initializes the CleanUpRepo class with a logger"""
        self.logger = Base_Logging(log_file_name="clean_up_repo.log", level="INFO")

    def delete_file(self, file_name):
        """The method will delete a particular file"""
        if os.path.exists(file_name):
            os.remove(file_name)
            self.logger.write(f'{file_name} deleted')

    def delete_directory(self, dir_name):
        """The method will delete a particular directory along with its content"""
        import shutil # pylint: disable=import-error,import-outside-toplevel
        if os.path.exists(dir_name) and os.path.isdir(dir_name):
            shutil.rmtree(dir_name)
            self.logger.write(f'{dir_name} deleted')

    def delete_files_in_dir(self, directory, files):
        """The method will delete files in a particular directory"""
        for file_name in files:
            self.delete_file(os.path.join(directory, file_name))

    def delete_files_used_in_example(self):
        """The method will delete a set of files"""
        for every_dir_list, every_file_list in zip(conf.dir_list, conf.file_list):
            self.delete_files_in_dir(every_dir_list, every_file_list)

    def run_cleanup(self):
        """Runs the utility to delete example files and logs the operation."""
        self.logger.write("Running utility to delete the files")
        self.delete_directory(conf.PAGE_OBJECTS_EXAMPLES_DIR)
        self.delete_files_used_in_example()
        self.logger.write(
            f'All the files related to the sample example from Page Object Model have been removed from {conf.dir_list} folders.\n'
            'For next steps, please refer to the edit files section of this blog post: '
            'https://qxf2.com/blog/how-to-start-using-the-qxf2-framework-with-a-new-project/'
        )

if __name__ == "__main__":
    cleanup = CleanUpRepo()
    cleanup.run_cleanup()
