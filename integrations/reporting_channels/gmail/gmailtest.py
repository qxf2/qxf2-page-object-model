"""
This is an example automated test to check gmail utils
Our automated test will do the following:
    #login to gmail and fetch mailboxes
    #After fetching the mail box ,select and fetch messages and print the number of messages 
    #and the subject of the messages

Prerequisites:
    - Gmail account with app password
"""
import sys
import os
import io
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from integrations.reporting_channels.gmail.gmail import Gmail, AuthenticationError
from integrations.reporting_channels.gmail.mailbox import Mailbox
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

def gmail_test():
    "Run the Gmail utility test"
    try:
        # 1. Initialize Gmail object and connect
        gmail = Gmail()
        gmail.connect()
        print("Connected to Gmail")

        # 2. Login to Gmail
        username = os.getenv('app_username')
        password = os.getenv('app_password')

        try:
            gmail.login(username, password)
            print("Login successful")
        except AuthenticationError as e:
            print(f"Authentication failed: Check for the login credentials {str(e)}")
            return

        # 3. Fetch mailboxes
        mailboxes = gmail.fetch_mailboxes()
        if mailboxes:
            print(f"Fetched mailboxes: {mailboxes}")
        else:
            raise ValueError("Failed to fetch mailboxes!")

        # 4. Select and fetch messages from SPAM mailbox
        inbox_mailbox = gmail.use_mailbox("Inbox")
        if isinstance(inbox_mailbox, Mailbox):
            print("SPAM mailbox selected successfully")
        else:
            raise TypeError(f"Error: Expected Mailbox instance, got {type(inbox_mailbox)}")

        # 5. Fetch and print messages from SPAM
        messages = inbox_mailbox.mail()
        print(f"Number of messages in SPAM: {len(messages)}")

        # 6. Fetch and print message subjects
        if messages:
            msg = messages[0]
            fetched_msg = msg.fetch()
            print(f"Fetching Message subject: {fetched_msg.get('subject')}")

            # Fetch multiple messages and log subjects
            messages_dict = {msg.uid.decode('utf-8'): msg for msg in messages}
            fetched_messages = gmail.fetch_multiple_messages(messages_dict)
            for uid, message in fetched_messages.items():
                subject = getattr(message, 'subject', 'No subject')
                print(f"UID: {uid}, Subject: {subject.encode('utf-8', errors='replace').decode('utf-8')}")

        else:
            print("No messages found in SPAM")

        # 7. Logout
        gmail.logout()
        print("Logged out successfully")

    except Exception as e:
        print(f"Exception encountered: {str(e)}")
        raise

if __name__ == "__main__":
    gmail_test()
