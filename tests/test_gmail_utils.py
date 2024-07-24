import sys
import os
from integrations.reporting_channels.gmail.gmail import Gmail
from integrations.reporting_channels.gmail.message import Message 
from integrations.reporting_channels.gmail.mailbox import Mailbox
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))



def main():
    gmail = Gmail()
    gmail.connect()

    username = "username"
    password = "password"
    
    # if gmail.login(username, password):
    #     print("Login successful!")
    #     try:
    #         test_mailboxes = ["INBOX", '"[Gmail]/All Mail"', '"[Gmail]/Sent Mail"']
    #         for mailbox in test_mailboxes:
    #             try:
    #                 gmail.use_mailbox(mailbox)
    #                 print(f"{mailbox} selected successfully!")
    #             except Exception as e:
    #                 print(f"Error selecting {mailbox}: {e}")
    #     except Exception as e:
    #         print(f"Error during mailbox operations: {e}")
    
            # inbox_mailbox = gmail.use_mailbox('INBOX')
            # message_uids = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] 
            # messages = {uid: Message(inbox_mailbox, uid) for uid in message_uids}
            # fetched_messages = gmail.fetch_multiple_messages(messages)
            # for uid, msg in fetched_messages.items():
            #     print(f"Message UID: {uid}, Subject: {msg.subject}")

    try:
        if gmail.login(username, password):
            print("Login successful!")
            
            mailboxes = gmail.fetch_mailboxes()
            print(f"Fetched mailboxes: {mailboxes}")
            
            if mailboxes:
                for mailbox_name in mailboxes:
                    print(f"Mailbox found: {mailbox_name}")
            
            try:
                inbox_mailbox = gmail.use_mailbox('INBOX')
                print(f"Type of inbox_mailbox: {type(inbox_mailbox)}")

                if isinstance(inbox_mailbox, Mailbox):
                    print(f"INBOX selected successfully!")
                    messages = inbox_mailbox.mail()
                    print(f"Messages in INBOX: {[msg.uid.decode('utf-8') if isinstance(msg.uid, bytes) else msg.uid for msg in messages]}")

                    if messages:
                        msg = messages[0]  # Use a valid UID
                        msg.fetch()
                        print(f"Message subject: {msg.subject}")
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
