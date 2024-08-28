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
import pytest
from integrations.reporting_channels.gmail.gmail import Gmail
from integrations.reporting_channels.gmail.mailbox import Mailbox
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

def login_to_gmail(gmail, username, password):
    "Login to mail"
    result_flag = gmail.login(username, password)
    if not result_flag:
        raise RuntimeError("Login failed!")
    print("Login successful!")
    return 1, 1

def fetch_and_print_mailboxes(gmail):
    "fetch mailboxes the get the mailbox names"
    mailboxes = gmail.fetch_mailboxes()
    if not mailboxes:
        raise ValueError("Failed to fetch mailboxes!")
    print(f"Fetched mailboxes: {mailboxes}")
    return 1, 1

def fetch_and_print_messages(inbox_mailbox):
    "fetch and get the messages"
    messages = inbox_mailbox.mail()
    print(f"Number of messages in SPAM: {len(messages)}")
    return 1, 1, messages

def fetch_subjects(gmail, messages):
    "fetch the mails and get the subjects"
    messages_dict = {msg.uid.decode('utf-8'): msg for msg in messages}
    fetched_messages = gmail.fetch_multiple_messages(messages_dict)
    if not fetched_messages:
        raise RuntimeError("Failed to fetch multiple messages!")
    print(f"Fetched multiple messages: {fetched_messages}")

    for uid, message in fetched_messages.items():
        subject = getattr(message, 'subject', 'No subject attribute')
        print(f"UID: {uid}, Subject: {subject}")
    return 1, 1

@pytest.mark.GMAIL
def test_gmail_util():
    "Run the test"
    expected_pass = 0
    actual_pass = 0

    try:
        gmail = Gmail()
        gmail.connect()

        username = os.getenv('app_username')
        password = os.getenv('app_password')

        expected, actual = login_to_gmail(gmail, username, password)
        expected_pass += expected
        actual_pass += actual

        expected, actual = fetch_and_print_mailboxes(gmail)
        expected_pass += expected
        actual_pass += actual

        inbox_mailbox = gmail.use_mailbox('[Gmail]/Spam')
        if not isinstance(inbox_mailbox, Mailbox):
            raise TypeError(f"Error: Expected Mailbox instance, got {type(inbox_mailbox)}.")
        print("SPAM selected successfully!")
        expected_pass += 1
        actual_pass += 1

        expected, actual, messages = fetch_and_print_messages(inbox_mailbox)
        expected_pass += expected
        actual_pass += actual

        if messages:
            msg = messages[0]
            fetched_msg = msg.fetch()
            print(f"Fetching Message subject from test script: {fetched_msg.get('subject')}")
            expected_pass += 1
            actual_pass += 1

            expected, actual = fetch_subjects(gmail, messages)
            expected_pass += expected
            actual_pass += actual
        else:
            print("No messages found in SPAM.")

    except (TypeError, ValueError, KeyError) as e:
        print(f"Exception when trying to run test: {__file__}")
        print(f"Python says {str(e)}")

    finally:
        gmail.logout()
        print("Logged out!")
        expected_pass += 1
        actual_pass += 1

    if expected_pass != actual_pass:
        raise RuntimeError(f"Test failed: {__file__}")
