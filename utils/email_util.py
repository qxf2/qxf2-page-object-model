"""
A simple IMAP util that will help us with account activation
* Connect to your imap host
* Login with username/password
* Fetch latest messages in inbox
* Get a recent registration message
* Filter based on sender and subject
* Return text of recent messages

[TO DO](not in any particular order)
1. Extend to POP3 servers
2. Add a try catch decorator
3. Enhance get_latest_email_uid to make all parameters optional
"""
#The import statements import: standard Python modules,conf
import os,sys,time,imaplib,email,datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import conf.email_conf as conf_file

class Email_Util:
    "Class to interact with IMAP servers"

    def connect(self,imap_host):
        "Connect with the host"
        self.mail = imaplib.IMAP4_SSL(imap_host)

        return self.mail


    def login(self,username,password):
        "Login to the email"
        result_flag = False
        try:
            self.mail.login(username,password)
        except Exception as e:
            print('\nException in Email_Util.login')
            print('PYTHON SAYS:')
            print(e)
            print('\n')
        else:
            result_flag = True

        return result_flag


    def get_folders(self):
        "Return a list of folders"
        return self.mail.list()


    def select_folder(self,folder):
        "Select the given folder if it exists. E.g.: [Gmail]/Trash"
        result_flag = False
        response = self.mail.select(folder)
        if response[0] == 'OK':
            result_flag = True

        return result_flag


    def get_latest_email_uid(self,subject=None,sender=None,time_delta=10,wait_time=300):
        "Search for a subject and return the latest unique ids of the emails"
        uid = None
        time_elapsed = 0
        search_string = ''
        if subject is None and sender is None:
            search_string = 'ALL'

        if subject is None and sender is not None:
            search_string = '(FROM "{sender}")'.format(sender=sender)

        if subject is not None and sender is None:
            search_string = '(SUBJECT "{subject}")'.format(subject=subject)

        if subject is not None and sender is not None:
            search_string = '(FROM "{sender}" SUBJECT "{subject}")'.format(sender=sender,subject=subject)

        print("  - Automation will be in search/wait mode for max %s seconds"%wait_time)
        while (time_elapsed < wait_time and uid is None):
            time.sleep(time_delta)
            result,data = self.mail.uid('search',None,str(search_string))

            if data[0].strip() != '': #Check for an empty set
                uid = data[0].split()[-1]

            time_elapsed += time_delta

        return uid


    def fetch_email_body(self,uid):
        "Fetch the email body for a given uid"
        email_body = []
        if uid is not None:
            result,data = self.mail.uid('fetch',uid,'(RFC822)')
            raw_email = data[0][1]
            email_msg = email.message_from_string(raw_email)
            email_body = self.get_email_body(email_msg)

        return email_body


    def get_email_body(self,email_msg):
        "Parse out the text of the email message. Handle multipart messages"
        email_body = []
        maintype = email_msg.get_content_maintype()
        if maintype == 'multipart':
            for part in email_msg.get_payload():
                if part.get_content_maintype() == 'text':
                    email_body.append(part.get_payload())
        elif maintype == 'text':
            email_body.append(email_msg.get_payload())

        return email_body


    def logout(self):
        "Logout"
        result_flag = False
        response, data = self.mail.logout()
        if response == 'BYE':
            result_flag = True

        return result_flag


#---EXAMPLE USAGE---
if __name__=='__main__':
    #Fetching conf details from the conf file
    imap_host = conf_file.imaphost
    username = conf_file.username
    password = conf_file.app_password

    #Initialize the email object
    email_obj = Email_Util()

    #Connect to the IMAP host
    email_obj.connect(imap_host)

    #Login
    if email_obj.login(username,password):
        print("PASS: Successfully logged in.")
    else:
        print("FAIL: Failed to login")

    #Get a list of folder
    folders = email_obj.get_folders()
    if folders != None or []:
        print("PASS: Email folders:", email_obj.get_folders())

    else:
        print("FAIL: Didn't get folder details")

    #Select a folder
    if email_obj.select_folder('Inbox'):
        print("PASS: Successfully selected the folder: Inbox")
    else:
        print("FAIL: Failed to select the folder: Inbox")

    #Get the latest email's unique id
    uid = email_obj.get_latest_email_uid(wait_time=300)
    if uid != None:
        print("PASS: Unique id of the latest email is: ",uid)
    else:
        print("FAIL: Didn't get unique id of latest email")

    #A. Look for an Email from provided sender, print uid and check it's contents
    uid = email_obj.get_latest_email_uid(sender="Andy from Google",wait_time=300)
    if uid != None:
        print("PASS: Unique id of the latest email with given sender is: ",uid)

        #Check the text of the latest email id
        email_body = email_obj.fetch_email_body(uid)
        data_flag = False
        print("  - Automation checking mail contents")
        for line in email_body:
            line = line.replace('=','')
            line = line.replace('<','')
            line = line.replace('>','')

            if "Hi Email_Util" and "This email was sent to you" in line:
                data_flag = True
                break
        if data_flag == True:
            print("PASS: Automation provided correct Email details. Email contents matched with provided data.")
        else:
            print("FAIL: Provided data not matched with Email contents. Looks like automation provided incorrect Email details")

    else:
        print("FAIL: After wait of 5 mins, looks like there is no email present with given sender")

    #B. Look for an Email with provided subject, print uid, find Qxf2 POM address and compare with expected address
    uid = email_obj.get_latest_email_uid(subject="Qxf2 Services: Public POM Link",wait_time=300)
    if uid != None:
        print("PASS: Unique id of the latest email with given subject is: ",uid)
        #Get pom url from email body
        email_body = email_obj.fetch_email_body(uid)
        expected_pom_url = "https://github.com/qxf2/qxf2-page-object-model"
        pom_url = None
        data_flag = False
        print("  - Automation checking mail contents")
        for body in email_body:
            search_str = "/qxf2/"
            body = body.split()
            for element in body:
                if search_str in element:
                    pom_url = element
                    data_flag = True
                    break

            if data_flag == True:
                break

        if data_flag == True and expected_pom_url == pom_url:
            print("PASS: Automation provided correct mail details. Got correct Qxf2 POM url from mail body. URL: %s"%pom_url)
        else:
            print("FAIL: Actual POM url not matched with expected pom url. Actual URL got from email: %s"%pom_url)

    else:
        print("FAIL: After wait of 5 mins, looks like there is no email present with given subject")

    #C. Look for an Email with provided sender and subject and print uid
    uid = email_obj.get_latest_email_uid(subject="get more out of your new Google Account",sender="andy-noreply@google.com",wait_time=300)
    if uid != None:
        print("PASS: Unique id of the latest email with given subject and sender is: ",uid)
    else:
        print("FAIL: After wait of 5 mins, looks like there is no email present with given subject and sender")

    #D. Look for an Email with non-existant sender and non-existant subject details
    uid = email_obj.get_latest_email_uid(subject="Activate your account",sender="support@qxf2.com",wait_time=120) #you can change wait time by setting wait_time variable
    if uid != None:
        print("FAIL: Unique id of the latest email with non-existant subject and non-existant sender is: ",uid)
    else:
        print("PASS: After wait of 2 mins, looks like there is no email present with given non-existant subject and non-existant sender")

