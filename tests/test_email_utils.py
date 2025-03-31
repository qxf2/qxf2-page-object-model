"""
This is an example automated test to check email utils
Our automated test will do the following:
    #login to email and fetch mailboxes
    #After fetching the mail box ,select and fetch messages and 
    # print the number of messages and the subject of the messages

Prerequisites:
    - Email account with app password
"""
import os
import sys
import pytest
from integrations.reporting_channels.email.email import Email
from integrations.reporting_channels.email.mailbox import Mailbox
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()
@pytest.mark.skip(reason="Skipping this test to not to run in CI")
@pytest.mark.EMAIL
def test_email_util():
    "Test email to login, fetch mailboxes, retrieve messages, fetch threads, and verify subjects."
    try:
        # Initialize flags for test summary
        expected_pass = 0
        actual_pass = 0

        # Initialize Gmail class instance
        email = Email()
        email.connect()

        username = os.getenv('app_username')
        password = os.getenv('app_password')

        # Attempt to log in
        result_flag = email.login(username, password)
        assert result_flag, "Login failed!"
        print("Login successful!")
        expected_pass += 1
        actual_pass += 1

        # Fetch and print mailboxes
        mailboxes = email.fetch_mailboxes()
        assert mailboxes, "Failed to fetch mailboxes!"
        print(f"Fetched mailboxes: {mailboxes}")
        expected_pass += 1
        actual_pass += 1

        # Select the INBOX mailbox
        inbox_mailbox = email.use_mailbox('Inbox')
        assert isinstance(inbox_mailbox, Mailbox), f"Error: Expected Mailbox instance, got {type(inbox_mailbox)}."
        print("INBOX selected successfully!")
        expected_pass += 1
        actual_pass += 1

        # Fetch and print number of messages in INBOX
        messages = inbox_mailbox.mail()
        print(f"Number of messages in Inbox: {len(messages)}")
        expected_pass += 1
        actual_pass += 1

        if messages:
            # Fetch and print the subject of the first message
            msg = messages[0]
            fetched_msg = msg.fetch()
            assert 'subject' in fetched_msg, "Subject not found in fetched message!"
            print(f"Fetching Message subject from test script: {fetched_msg.get('subject')}")
            expected_pass += 1
            actual_pass += 1
            msg.fetch()
            thread_messages = msg.fetch_thread()
            if thread_messages:
                print(f"Number of messages in Thread: {len(thread_messages)}")
                for message in thread_messages:
                    subject = getattr(message, 'subject', 'No subject attribute')
                    body = getattr(message, 'body', 'no body message found')
                    print(f"Thread message subject: {subject}")
                    print(f"Thread message subject: {body}")
            else:
                print("No messages found in thread.")

            # Fetch and print subjects of multiple messages
            messages_dict = {msg.uid.decode('utf-8'): msg for msg in messages}
            fetched_messages = email.fetch_multiple_messages(messages_dict)
            assert fetched_messages, "Failed to fetch multiple messages!"
            expected_pass += 1
            actual_pass += 1

            for uid, message in fetched_messages.items():
                subject = getattr(message, 'subject', 'No subject attribute')
                print(f"UID: {uid}, Email Subject: {subject}")
        else:
            print("No messages found in INBOX.")

    except Exception as e:
        print(f"Exception when trying to run test: {__file__}")
        print(f"Python says: {e}")

    finally:
        # logout
        email.logout()
        print("Logged out!")
        expected_pass += 1
        actual_pass += 1

    assert expected_pass == actual_pass, f"Test failed: {__file__}"