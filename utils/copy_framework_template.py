r"""
This script would copy the required framework files from the input source to
the input destination given by the user.
1. Copy root files from POM to the newly created destination directory.
2. Create the sub-folder to copy files from POM\conf.
3. Create the sub-folder to copy files from POM\page_objects.
4. Create the sub-folder to copy files and folders from POM\utils.
5. Create the sub-folder to copy files and folders from POM\core_helpers
6. Create the sub-folder to copy files and folders from POM\integrations
7. Create the sub-folder to copy files from POM\tests

From root directory, run following command to execute the script correctly.
python utils/copy_framework_template.py -s . -d ../copy_pom_temp/

"""

import os
import sys
import argparse
import shutil
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import copy_framework_template_conf as conf

def copy_selected_files(file_list,dst_folder):
	"copy selected files into destination folder"
	# Create the new destination directory
	if not os.path.exists(dst_folder):
		os.makedirs(dst_folder)

	# Check if destination folder exists and then copy files
	if os.path.exists(dst_folder):
		for every_src_file in file_list:
			shutil.copy2(every_src_file,dst_folder)


def copy_contents(src_folder, dst_folder, exclude_dirs=None):
    "Copy all content from source directory to destination directory"
    if exclude_dirs is None:
        exclude_dirs = ['__pycache__']

    # Create destination folder if it doesn't exist
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    for root, dirs, files in os.walk(src_folder):
        # Exclude specified directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        # Calculate relative path
        rel_path = os.path.relpath(root, src_folder)
        dst_path = os.path.join(dst_folder, rel_path)

        # Create directories in the destination folder
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)

        # Copy files
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dst_path, file)
            shutil.copy2(src_file, dst_file)


def copy_framework_template(src_folder,dst_folder):
	"Copy files from POM to the destination directory path."
	# Get details from conf file
	src_files_list = conf.src_files_list # root files list to copy
	#copy selected files from source root
	copy_selected_files(src_files_list,dst_folder)

	#2. Create the sub-folder to copy files from POM\conf.
	# Get details from conf file for Conf
	src_conf_files_list = conf.src_conf_files_list
	dst_folder_conf = os.path.abspath(os.path.join(dst_folder,'conf'))
	#copy selected files from source conf directory
	copy_selected_files(src_conf_files_list,dst_folder_conf)

	#3. Create the sub-folder to copy files from POM\page_objects.
	#3 Get details from conf file for Page_Objects
	src_page_objects_files_list = conf.src_page_objects_files_list
	dst_folder_page_objects = os.path.abspath(os.path.join(dst_folder,'page_objects'))
	#copy selected files from source page_objeccts directory
	copy_selected_files(src_page_objects_files_list,dst_folder_page_objects)

	#4. Create the sub-folder to copy files from POM\utils.
	# utils directory paths
	src_folder_utils = os.path.abspath(os.path.join(src_folder,'utils'))
	dst_folder_utils = os.path.abspath(os.path.join(dst_folder,'utils'))
	#copy all contents from source utils directory
	copy_contents(src_folder_utils,dst_folder_utils)

	#5. Create the sub-folder to copy files from POM\core_helpers
	# core helpers directory paths
	src_folder_core_helpers = os.path.abspath(os.path.join(src_folder,'core_helpers'))
	dst_folder_core_helpers = os.path.abspath(os.path.join(dst_folder,'core_helpers'))
	#copy all contents from source core_helpers directory
	copy_contents(src_folder_core_helpers,dst_folder_core_helpers)

	#6. Create the sub-folder to copy files from POM\integrations
	# integrations directory paths
	src_folder_integrations = os.path.abspath(os.path.join(src_folder,'integrations'))
	dst_folder_integrations = os.path.abspath(os.path.join(dst_folder,'integrations'))
	#copy all contents from source integrations directory
	copy_contents(src_folder_integrations,dst_folder_integrations)

	#7. Create the sub-folder to copy files from POM\tests.
	# Get details from conf file for Conf
	src_tests_files_list = conf.src_tests_files_list
	dst_folder_tests = os.path.abspath(os.path.join(dst_folder,'tests'))
	#copy selected files from source page_objeccts directory
	copy_selected_files(src_tests_files_list,dst_folder_tests)

	print(f"Template copied to destination {os.path.abspath(dst_folder)} successfully")


#---START OF SCRIPT
if __name__=='__main__':
	#run the test
	parser=argparse.ArgumentParser(description="Copy framework template.")
	parser.add_argument("-s","--source",dest="src",
                   help="The name of the source folder: ie, POM",default=".")
	parser.add_argument("-d","--destination",dest="dst",
                    help="The name of the destination folder: ie, client name",
                    default="../copy_pom_templete/")
	args = parser.parse_args()

	copy_framework_template(args.src,args.dst)
