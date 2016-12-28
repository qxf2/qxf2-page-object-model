"""
This conf file would have the relative paths of the files & folders.
"""
import os,sys

#POM
#Files from src POM:
src_pom_file1 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','__init__.py'))
src_pom_file2 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','conftest.py'))
src_pom_file3 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','Readme.md'))
src_pom_file4 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','Requirements.txt'))
src_pom_file5 = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','setup.cfg'))

#src POM file list:
src_pom_files_list = [src_pom_file1,src_pom_file2,src_pom_file3,src_pom_file4,src_pom_file5]

#destination folder for POM which user has to mention. This folder should be created by user.
dst_folder_pom = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..','clients','Play_Arena','POM'))