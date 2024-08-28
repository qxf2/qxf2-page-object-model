"""
This is an example automated test to check gmail utils
Our automated test will do the following:
    #login to gmail and fetch mailboxes
    #After fetching the mail box ,select and fetch messages and print the number of messages and the subject of the messages

Prerequisites:
    - Gmail account with app password
"""

import sys
import os
from integrations.reporting_channels.gmail.gmail import Gmail
from integrations.reporting_channels.gmail.mailbox import Mailbox
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest

load_dotenv()

@pytest.mark.GMAIL
def test_gmail_util():
    try:
        # Initialize flags for test summary
        expected_pass = 0
        actual_pass = 0

        # Initialize Gmail class instance
        gmail = Gmail()
        gmail.connect()

        username = os.getenv('app_username')
        password = os.getenv('app_password')

        # Attempt to log in
        result_flag = gmail.login(username, password)
        if not result_flag:
            raise Exception("Login failed!")
        print("Login successful!")
        expected_pass += 1
        actual_pass += 1

        # Fetch and print mailboxes
        mailboxes = gmail.fetch_mailboxes()
        if not mailboxes:
            raise ValueError("Failed to fetch mailboxes!")
        print(f"Fetched mailboxes: {mailboxes}")
        expected_pass += 1
        actual_pass += 1

        # Select the SPAM mailbox
        inbox_mailbox = gmail.use_mailbox('[Gmail]/Spam')
        if not isinstance(inbox_mailbox, Mailbox):
            raise TypeError(f"Error: Expected Mailbox instance, got {type(inbox_mailbox)}.")
        print("SPAM selected successfully!")
        expected_pass += 1
        actual_pass += 1

        # Fetch and print number of messages in SPAM
        messages = inbox_mailbox.mail()
        print(f"Number of messages in SPAM: {len(messages)}")
        expected_pass += 1
        actual_pass += 1

        if messages:
            # Fetch and print the subject of the first message
            msg = messages[0]
            fetched_msg = msg.fetch()
            print(f"Fetching Message subject from test script: {fetched_msg.get('subject')}")
            expected_pass += 1
            actual_pass += 1

            # Fetch and print subjects of multiple messages
            messages_dict = {msg.uid.decode('utf-8'): msg for msg in messages}
            fetched_messages = gmail.fetch_multiple_messages(messages_dict)
            if not fetched_messages:
                raise RuntimeError("Failed to fetch multiple messages!")
            else:
                print(f"Fetched multiple messages: {fetched_messages}")
                expected_pass += 1
                actual_pass += 1

                for uid, message in fetched_messages.items():
                    subject = getattr(message, 'subject', 'No subject attribute')
                    print(f"UID: {uid}, Subject: {subject}")
        else:
            print("No messages found in SPAM.")

    except Exception as e:
        print("Exception when trying to run test: %s" %__file__)
        print("Python says: %s" % str(e))

    finally:
        # logout
        gmail.logout()
        print("Logged out!")
        expected_pass += 1
        actual_pass += 1

    if expected_pass != actual_pass:
        raise RuntimeError(f"Test failed: {__file__}")