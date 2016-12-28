import os,sys
import shutil
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import test_path_conf as conf

#get details from conf file for POM
src_pom_files_list = conf.src_pom_files_list
dst_folder_pom = conf.dst_folder_pom

#check if POM folder exists and then copy files
if os.path.exists(dst_folder_pom):
	for every_src_pom_file in src_pom_files_list:
		shutil.copy2(every_src_pom_file,dst_folder_pom)