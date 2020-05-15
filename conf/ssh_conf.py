"""
This config file would have the credentials of remote server,
the commands to execute, upload and download file path details.
"""
#Server credential details needed for ssh
HOST='Enter your host details here'
USERNAME='Enter your username here'
PASSWORD='Enter your password here'
PORT = 22
TIMEOUT = 10

#.pem file details
PKEY = 'Enter your key filename here'

#Sample commands to execute(Add your commands here)
COMMANDS = ['ls;mkdir sample']

#Sample file locations to upload and download
UPLOADREMOTEFILEPATH = '/etc/example/filename.txt'
UPLOADLOCALFILEPATH = 'home/filename.txt'
DOWNLOADREMOTEFILEPATH = '/etc/sample/data.txt'
DOWNLOADLOCALFILEPATH = 'home/data.txt'
