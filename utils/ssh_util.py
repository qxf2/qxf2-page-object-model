"""
Qxf2 Services: Utility script to ssh into a remote server
* Connect to the remote server
* Execute the given command
* Upload a file
* Download a file
"""

import paramiko
import os,sys,time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import ssh_conf as conf_file   
import socket

class Ssh_Util:
    "Class to connect to remote server" 
    
    def __init__(self):
        self.ssh_output = None
        self.ssh_error = None
        self.client = None
        self.host= conf_file.HOST
        self.username = conf_file.USERNAME
        self.password = conf_file.PASSWORD
        self.timeout = float(conf_file.TIMEOUT)
        self.commands = conf_file.COMMANDS
        self.pkey = conf_file.PKEY
        self.port = conf_file.PORT
        self.uploadremotefilepath = conf_file.UPLOADREMOTEFILEPATH
        self.uploadlocalfilepath = conf_file.UPLOADLOCALFILEPATH
        self.downloadremotefilepath = conf_file.DOWNLOADREMOTEFILEPATH
        self.downloadlocalfilepath = conf_file.DOWNLOADLOCALFILEPATH
       
    def connect(self):
        "Login to the remote server"
        try:
            #Paramiko.SSHClient can be used to make connections to the remote server and transfer files
            print("Establishing ssh connection...")
            self.client = paramiko.SSHClient()
            #Parsing an instance of the AutoAddPolicy to set_missing_host_key_policy() changes it to allow any host.
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            #Connect to the server
            if (self.password == ''):
                private_key = paramiko.RSAKey.from_private_key_file(self.pkey)
                self.client.connect(hostname=self.host, port=self.port, username=self.username,pkey=private_key ,timeout=self.timeout, allow_agent=False, look_for_keys=False)
                print("Connected to the server",self.host)
            else:
                self.client.connect(hostname=self.host, port=self.port,username=self.username,password=self.password,timeout=self.timeout, allow_agent=False, look_for_keys=False)    
                print("Connected to the server",self.host)
        except paramiko.AuthenticationException:
            print("Authentication failed, please verify your credentials")
            result_flag = False
        except paramiko.SSHException as sshException:
            print("Could not establish SSH connection: %s" % sshException)
            result_flag = False
        except socket.timeout as e:
            print("Connection timed out")
            result_flag = False
        except Exception as e:
            print('\nException in connecting to the server')
            print('PYTHON SAYS:',e)
            result_flag = False
            self.client.close()
        else:
            result_flag = True
        
        return result_flag    
  

    def execute_command(self,commands):
        """Execute a command on the remote host.Return a tuple containing
        an integer status and a two strings, the first containing stdout
        and the second containing stderr from the command."""
        self.ssh_output = None
        result_flag = True
        try:
            if self.connect():
                for command in commands:
                    print("Executing command --> {}".format(command))
                    stdin, stdout, stderr = self.client.exec_command(command,timeout=10)
                    self.ssh_output = stdout.read()
                    self.ssh_error = stderr.read()
                    if self.ssh_error:
                        print("Problem occurred while running command:"+ command + " The error is " + self.ssh_error)
                        result_flag = False
                    else:    
                        print("Command execution completed successfully",command)
                    self.client.close()
            else:
                print("Could not establish SSH connection")
                result_flag = False   
        except socket.timeout as e:
            print("Command timed out.", command)
            self.client.close()
            result_flag = False                
        except paramiko.SSHException:
            print("Failed to execute the command!",command)
            self.client.close()
            result_flag = False    
                      
        return result_flag


    def upload_file(self,uploadlocalfilepath,uploadremotefilepath):
        "This method uploads the file to remote server"
        result_flag = True
        try:
            if self.connect():
                ftp_client= self.client.open_sftp()
                ftp_client.put(uploadlocalfilepath,uploadremotefilepath)
                ftp_client.close() 
                self.client.close()
            else:
                print("Could not establish SSH connection")
                result_flag = False  
        except Exception as e:
            print('\nUnable to upload the file to the remote server',uploadremotefilepath)
            print('PYTHON SAYS:',e)
            result_flag = False
            ftp_client.close()
            self.client.close()
        
        return result_flag


    def download_file(self,downloadremotefilepath,downloadlocalfilepath):
        "This method downloads the file from remote server"
        result_flag = True
        try:
            if self.connect():
                ftp_client= self.client.open_sftp()
                ftp_client.get(downloadremotefilepath,downloadlocalfilepath)
                ftp_client.close()  
                self.client.close()
            else:
                print("Could not establish SSH connection")
                result_flag = False  
        except Exception as e:
            print('\nUnable to download the file from the remote server',downloadremotefilepath)
            print('PYTHON SAYS:',e)
            result_flag = False
            ftp_client.close()
            self.client.close()
        
        return result_flag


#---USAGE EXAMPLES
if __name__=='__main__':
    print("Start of %s"%__file__)
     
    #Initialize the ssh object
    ssh_obj = Ssh_Util()

    #Sample code to execute commands
    if ssh_obj.execute_command(ssh_obj.commands) is True:
        print("Commands executed successfully\n")
    else:
        print ("Unable to execute the commands" )   
    
    #Sample code to upload a file to the server
    if ssh_obj.upload_file(ssh_obj.uploadlocalfilepath,ssh_obj.uploadremotefilepath) is True:
        print ("File uploaded successfully", ssh_obj.uploadremotefilepath)
    else:
        print  ("Failed to upload the file")
    
    #Sample code to download a file from the server
    if ssh_obj.download_file(ssh_obj.downloadremotefilepath,ssh_obj.downloadlocalfilepath) is True:
        print ("File downloaded successfully", ssh_obj.downloadlocalfilepath)
    else:
        print  ("Failed to download the file")
    