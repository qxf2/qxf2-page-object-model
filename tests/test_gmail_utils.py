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
from integrations.reporting_channels.gmail.gmail import Gmail , AuthenticationError
from integrations.reporting_channels.gmail.mailbox import Mailbox
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

@pytest.mark.skip(reason="currently no support on CI to test this")
@pytest.mark.GMAIL
def test_gmail_util(test_obj):
    "Run the Gmail utility test"
    expected_pass = 0
    actual_pass = 0

    try:
        # 1. Initialize Gmail object and connect
        gmail = Gmail()
        gmail.connect()
        test_obj.write("Connected to Gmail")

        # 2. Login to Gmail
        username = os.getenv('app_username')
        password = os.getenv('app_password')
        try:
            result_flag = gmail.login(username, password)
            test_obj.log_result(result_flag,
                                positive="Login successful",
                                negative="Login failed due to invalid credentials")
            expected_pass += 1
            if result_flag:
                actual_pass += 1
        except AuthenticationError:
            test_obj.write("Login failed due to invalid credentials")
            raise

        # 3. Fetch mailboxes
        mailboxes = gmail.fetch_mailboxes()
        if mailboxes:
            test_obj.write(f"Fetched mailboxes: {mailboxes}")
            actual_pass += 1
        else:
            raise ValueError("Failed to fetch mailboxes!")
        expected_pass += 1

        # 4. Select and fetch messages from SPAM mailbox
        spam_mailbox_name = "[Gmail]/Spam"
        inbox_mailbox = gmail.use_mailbox(spam_mailbox_name)
        if isinstance(inbox_mailbox, Mailbox):
            test_obj.write("SPAM mailbox selected successfully")
            actual_pass += 1
        else:
            raise TypeError(f"Error: Expected Mailbox instance, got {type(inbox_mailbox)}")
        expected_pass += 1

        # 5. Fetch and print messages from SPAM
        messages = inbox_mailbox.mail()
        test_obj.write(f"Number of messages in SPAM: {len(messages)}")
        actual_pass += 1
        expected_pass += 1

        # 6. Fetch and print message subjects
        if messages:
            msg = messages[0]
            fetched_msg = msg.fetch()
            test_obj.write(f"Fetching Message subject: {fetched_msg.get('subject')}")
            actual_pass += 1
            expected_pass += 1

            # Fetch multiple messages and log subjects
            messages_dict = {msg.uid.decode('utf-8'): msg for msg in messages}
            fetched_messages = gmail.fetch_multiple_messages(messages_dict)
            for uid, message in fetched_messages.items():
                subject = getattr(message, 'subject', 'No subject')
                test_obj.write(f"UID: {uid}, Subject: {subject}")
            actual_pass += 1
        else:
            test_obj.write("No messages found in SPAM")
        expected_pass += 1

        # 7. Logout
        gmail.logout()
        test_obj.write("Logged out successfully")
        actual_pass += 1
        expected_pass += 1

    except Exception as e:
        test_obj.write(f"Exception encountered: {str(e)}")
        raise

    # Write test summary and assert results
    test_obj.write_test_summary()
    assert expected_pass == actual_pass, "Test failed: expected and actual pass count mismatch"
