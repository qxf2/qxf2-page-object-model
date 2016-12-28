"""
This script would copy the required framework files from the input source to the input destination given by the user.
1. Copy files from POM to the newly created destination directory.
2. Verify if the destination directory is created and create the sub-folder to copy files from POM\Conf.
3. Verify if the destination directory is created and create the sub-folder to copy files from POM\Page_Objects.
4. Verify if the destination directory is created and create the sub-folder to copy files from POM\Utils.

"""
import os,sys
import shutil
from optparse import OptionParser
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import copy_framework_template_conf as conf

def copy_framework_template(src_folder,dst_folder):
	"run the test"
	#1. Copy files from POM to the newly created destination directory.
	#1a. Get details from conf file
	src_files_list = conf.src_files_list
		
	#1b. Create the new destination directory
	os.makedirs(dst_folder)
	
	#1c. Check if destination folder exists and then copy files
	if os.path.exists(dst_folder):
		for every_src_file in src_files_list:
			shutil.copy2(every_src_file,dst_folder)
	
	#2. Verify if the destination directory is created and create the sub-folder to copy files from POM\Conf.
	#2a. Get details from conf file for Conf
	src_conf_files_list = conf.src_conf_files_list
	dst_folder_conf = conf.dst_folder_conf
	
	#2b. Create the conf sub-folder
	if os.path.exists(dst_folder):
		os.mkdir(dst_folder_conf)
	
	#2c. Check if conf folder exists and then copy files
	if os.path.exists(dst_folder_conf):
		for every_src_conf_file in src_conf_files_list:
			shutil.copy2(every_src_conf_file,dst_folder_conf)
	
	#3. Verify if the destination directory is created and create the sub-folder to copy files from POM\Page_Objects.
	#3a. Get details from conf file for Page_Objects
	src_page_objects_files_list = conf.src_page_objects_files_list
	dst_folder_page_objects = conf.dst_folder_page_objects

	#3b. Create the page_object sub-folder
	if os.path.exists(dst_folder):
		os.mkdir(dst_folder_page_objects)
	
	#3c. Check if page_object folder exists and then copy files
	if os.path.exists(dst_folder_page_objects):
		for every_src_page_objects_file in src_page_objects_files_list:
			shutil.copy2(every_src_page_objects_file,dst_folder_page_objects)
	
	#4. Verify if the destination directory is created and create the sub-folder to copy files from POM\Utils.
	#4a. Get details from conf file for Utils folder
	src_utils_files_list = conf.src_utils_files_list
	dst_folder_utils = conf.dst_folder_utils
	
	#4b. Create the utils destination directory
	if os.path.exists(dst_folder):
		os.mkdir(dst_folder_utils)
		
	#4c. Check if utils folder exists and then copy files
	if os.path.exists(dst_folder_utils):
		for every_src_utils_file in src_utils_files_list:
			shutil.copy2(every_src_utils_file,dst_folder_utils)
		
#---START OF SCRIPT
if __name__=='__main__':
	#run the test	
	parser=OptionParser()
	parser.add_option("-s","--source",dest="src",help="The name of the source folder: ie, POM",default="POM")
	parser.add_option("-d","--destination",dest="dst",help="The name of the destination folder: ie, client name",default="Myntra")
	(options,args) = parser.parse_args()
	
	copy_framework_template(options.src,options.dst)
	