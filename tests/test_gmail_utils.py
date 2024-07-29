"""
This is an example automated test to check gmail utils
Our automated test will do the following:
    #login to gmail and fetch mailboxes
    #After fetching the mail box ,select INBOX and fetch messages print the number of messages and the subject of the first message

Prerequisites:
    - Gmail account with app password
"""
import sys
import os
from integrations.reporting_channels.gmail.gmail import Gmail
from integrations.reporting_channels.gmail.message import Message 
from integrations.reporting_channels.gmail.mailbox import Mailbox
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))



def main():
    gmail = Gmail()
    gmail.connect()

    username = 'username'
    password = 'password'

    try:
        if gmail.login(username, password):
            print("Login successful!")
            
            mailboxes = gmail.fetch_mailboxes()
            print(f"Fetched mailboxes: {mailboxes}")
            
            if mailboxes:
                for mailbox_name in mailboxes:
                    print(f"Mailbox found: {mailbox_name}")
            
            try:
                inbox_mailbox = gmail.use_mailbox('[Gmail]/Spam')
                if isinstance(inbox_mailbox, Mailbox):
                    print("SPAM selected successfully!")
                    messages = inbox_mailbox.mail()
                    print(f"Number of messages in SPAM: {len(messages)}")

                    if messages:
                        msg = messages[0]
                        fetched_msg = msg.fetch()
                        print(f"Fetching Message subject from test script: {fetched_msg.get('subject')}")
                    else:
                        print("No messages found in SPAM.")
                    
                    message_uids = [msg.uid.decode('utf-8') if isinstance(msg.uid, bytes) else msg.uid for msg in messages]
                    print(f"fetched message UIDs: {message_uids}")
                    
                    if messages:
                        messages_dict = {msg.uid: msg for msg in messages}

                        fetched_messages = gmail.fetch_multiple_messages(messages_dict)
                        print(f"Fetched multiple messages: {fetched_messages}")

                        for uid, message in fetched_messages.items():
                            subject = getattr(message, 'subject', 'No subject attribute')
                            print(f"UID: {uid}, Subject: {subject}")
                    
                        # for uid, msg in fetched_messages.items():
                        #     print(f"Message UID: {uid}, Subject: {msg.get('subject')}")

                else:
                    print(f"Error: Expected Mailbox instance, got {type(inbox_mailbox)}.")
            except Exception as e:
                print(f"An error occurred: {e}") 

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        gmail.logout()
        print("Logged out!")

if __name__ == "__main__":
    main()
