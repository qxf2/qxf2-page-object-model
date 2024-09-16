
import datetime
import email
import re
import time
import os
from email.header import decode_header, make_header
from imaplib import ParseFlags

class Message():


    def __init__(self, mailbox, uid):
        self.uid = uid
        self.mailbox = mailbox
        self.gmail = mailbox.gmail if mailbox else None

        self.message = None
        self.headers = {}

        self.subject = None
        self.body = None
        self.html = None

        self.to = None
        self.fr = None
        self.cc = None
        self.delivered_to = None

        self.sent_at = None

        self.flags = []
        self.labels = []

        self.thread_id = None
        self.thread = []
        self.message_id = None

        self.attachments = None



    def is_read(self):
        return ('\\Seen' in self.flags)

    def read(self):
        flag = '\\Seen'
        self.gmail.imap.uid('STORE', self.uid, '+FLAGS', flag)
        if flag not in self.flags: self.flags.append(flag)

    def unread(self):
        flag = '\\Seen'
        self.gmail.imap.uid('STORE', self.uid, '-FLAGS', flag)
        if flag in self.flags: self.flags.remove(flag)

    def is_starred(self):
        return ('\\Flagged' in self.flags)

    def star(self):
        flag = '\\Flagged'
        self.gmail.imap.uid('STORE', self.uid, '+FLAGS', flag)
        if flag not in self.flags: self.flags.append(flag)

    def unstar(self):
        flag = '\\Flagged'
        self.gmail.imap.uid('STORE', self.uid, '-FLAGS', flag)
        if flag in self.flags: self.flags.remove(flag)

    def is_draft(self):
        return ('\\Draft' in self.flags)

    def has_label(self, label):
        full_label = '%s' % label
        return (full_label in self.labels)

    def add_label(self, label):
        full_label = '%s' % label
        self.gmail.imap.uid('STORE', self.uid, '+X-GM-LABELS', full_label)
        if full_label not in self.labels: self.labels.append(full_label)

    def remove_label(self, label):
        full_label = '%s' % label
        self.gmail.imap.uid('STORE', self.uid, '-X-GM-LABELS', full_label)
        if full_label in self.labels: self.labels.remove(full_label)


    def is_deleted(self):
        return ('\\Deleted' in self.flags)

    def delete(self):
        flag = '\\Deleted'
        self.gmail.imap.uid('STORE', self.uid, '+FLAGS', flag)
        if flag not in self.flags: self.flags.append(flag)

        trash = '[Gmail]/Trash' if '[Gmail]/Trash' in self.gmail.labels() else '[Gmail]/Bin'
        if self.mailbox.name not in ['[Gmail]/Bin', '[Gmail]/Trash']:
            self.move_to(trash)

    # def undelete(self):
    #     flag = '\\Deleted'
    #     self.gmail.imap.uid('STORE', self.uid, '-FLAGS', flag)
    #     if flag in self.flags: self.flags.remove(flag)


    def move_to(self, name):
        self.gmail.copy(self.uid, name, self.mailbox.name)
        if name not in ['[Gmail]/Bin', '[Gmail]/Trash']:
            self.delete()



    def archive(self):
        self.move_to('[Gmail]/All Mail')

    def parse_headers(self, message):
        hdrs = {}
        for hdr in message.keys():
            hdrs[hdr] = message[hdr]
        return hdrs

    def parse_flags(self, headers):
        return list(ParseFlags(headers))
        # flags = re.search(r'FLAGS \(([^\)]*)\)', headers).groups(1)[0].split(' ')

    def parse_labels(self, headers):
        if re.search(r'X-GM-LABELS \(([^\)]+)\)', headers):
            labels = re.search(r'X-GM-LABELS \(([^\)]+)\)', headers).groups(1)[0].split(' ')
            return map(lambda l: l.replace('"', '').decode("string_escape"), labels)
        else:
            return list()

    def parse_subject(self, encoded_subject):
        if encoded_subject is None:
            print("Encoded subject is None")  
            return "No Subject" 
        
        dh = decode_header(encoded_subject)
        subject = ''.join([str(t[0], t[1] or 'utf-8') for t in dh])
        print(f"Decoded subject: {subject}")  
        return subject

# working demo part
    def parse(self, raw_message):
        raw_headers = raw_message[0]
        raw_email = raw_message[1]

        print(f"Raw email type before decode: {type(raw_email)}")
        print(f"Raw email before decode:", raw_email)
        # print(f"Raw headers: {raw_headers}")  
        # print(f"Raw email content (length: {len(raw_email)}): {raw_email[:200]}...")  

        if isinstance(raw_email, bytes):
            raw_email = raw_email.decode('utf-8', errors='replace')  
        print(f"Raw email after decode:", raw_email)

        if not isinstance(raw_email, str):
            raise ValueError("Decoded raw_email is not a string")
        try:
            self.message = email.message_from_string(raw_email)
        except Exception as e:
            print(f"Error creating email message: {e}")
            raise

        print(f"Message object: \n {self.message}")  
        print(f"Message headers: {self.message.items()}")  
        print(f"Subject: {self.message['subject']}")  
        self.to = self.message['to']
        self.fr = self.message['from']
        self.delivered_to = self.message['delivered_to']
        self.subject = self.parse_subject(self.message['subject'])
        print(f"Parse subject: {self.subject}")  

        if self.message.get_content_maintype() == "multipart":
            for content in self.message.walk():
                if content.get_content_type() == "text/plain":
                    self.body = content.get_payload(decode=True)
                elif content.get_content_type() == "text/html":
                    self.html = content.get_payload(decode=True)
        elif self.message.get_content_maintype() == "text":
            self.body = self.message.get_payload()

        self.sent_at = datetime.datetime.fromtimestamp(time.mktime(email.utils.parsedate_tz(self.message['date'])[:9]))

        self.flags = self.parse_flags(raw_headers)

        self.labels = self.parse_labels(raw_headers)

        if re.search(r'X-GM-THRID (\d+)', raw_headers):
            self.thread_id = re.search(r'X-GM-THRID (\d+)', raw_headers).groups(1)[0]
        if re.search(r'X-GM-MSGID (\d+)', raw_headers):
            self.message_id = re.search(r'X-GM-MSGID (\d+)', raw_headers).groups(1)[0]

        self.attachments = [
            Attachment(attachment) for attachment in self.message._payload
                if not isinstance(attachment, str) and attachment.get('Content-Disposition') is not None
        ]

    # def parse(self, raw_message):
    #     raw_headers = raw_message[0]
    #     raw_email = raw_message[1]

    #     # Print debugging information
    #     print(f"Raw email type before decode: {type(raw_email)}")
    #     print(f"Raw email before decode:", raw_email)
    #     print(f"Raw email content (length: {len(raw_email)}): {raw_email[:200]}...")  # Print first 200 chars

    #     # If raw_email is bytes, decode it
    #     if isinstance(raw_email, bytes):
    #         raw_email = raw_email.decode('utf-8', errors='replace')  # Handle potential decoding issues

    #     print(f"Raw email type after decode: {type(raw_email)}")
    #     print(f"Raw email after decode:", raw_email)

    #     # Ensure raw_email is a valid string
    #     if not isinstance(raw_email, str):
    #         raise ValueError("Decoded raw_email is not a string")

    #     try:
    #         self.message = email.message_from_string(raw_email)
    #     except Exception as e:
    #         print(f"Error creating email message: {e}")
    #         raise

    #     # Process headers and content
    #     self.headers = self.parse_headers(self.message)

    #     self.to = self.message['to']
    #     self.fr = self.message['from']
    #     self.delivered_to = self.message['delivered_to']
    #     self.subject = self.parse_subject(self.message['subject'])

    #     # Handle different content types
    #     if self.message.get_content_maintype() == "multipart":
    #         for content in self.message.walk():
    #             if content.get_content_type() == "text/plain":
    #                 self.body = content.get_payload(decode=True)
    #             elif content.get_content_type() == "text/html":
    #                 self.html = content.get_payload(decode=True)
    #     elif self.message.get_content_maintype() == "text":
    #         self.body = self.message.get_payload()

    #     # Parse the date
    #     date_tuple = email.utils.parsedate_tz(self.message['date'])
    #     if date_tuple:
    #         self.sent_at = datetime.datetime.fromtimestamp(time.mktime(date_tuple[:9]))

    #     # Parse flags and labels
    #     self.flags = self.parse_flags(raw_headers)
    #     self.labels = self.parse_labels(raw_headers)

    #     # Extract thread ID and message ID
    #     thread_id_match = re.search(r'X-GM-THRID (\d+)', raw_headers)
    #     if thread_id_match:
    #         self.thread_id = thread_id_match.groups(1)[0]
        
    #     message_id_match = re.search(r'X-GM-MSGID (\d+)', raw_headers)
    #     if message_id_match:
    #         self.message_id = message_id_match.groups(1)[0]

    #     # Extract attachments
    #     self.attachments = [
    #         Attachment(attachment) for attachment in self.message._payload
    #         if not isinstance(attachment, str) and attachment.get('Content-Disposition') is not None
    #     ]

    def fetch(self):
        if not self.message:
            try:
                response, results = self.gmail.imap.uid('FETCH', self.uid, '(BODY.PEEK[] FLAGS X-GM-THRID X-GM-MSGID X-GM-LABELS)')
                self.parse(results[0])
            except Exception as e:
                print(f"Error fetching message: {e}")
                raise
        return self.message


    # returns a list of fetched messages (both sent and received) in chrological order
    def fetch_thread(self):
        self.fetch()
        original_mailbox = self.mailbox
        self.gmail.use_mailbox(original_mailbox.name)

        # fetch and cache messages from inbox or other received mailbox
        response, results = self.gmail.imap.uid('SEARCH', None, '(X-GM-THRID ' + self.thread_id + ')')
        received_messages = {}
        uids = results[0].split(' ')
        if response == 'OK':
            for uid in uids: received_messages[uid] = Message(original_mailbox, uid)
            self.gmail.fetch_multiple_messages(received_messages)
            self.mailbox.messages.update(received_messages)

        # fetch and cache messages from 'sent'
        self.gmail.use_mailbox('[Gmail]/Sent Mail')
        response, results = self.gmail.imap.uid('SEARCH', None, '(X-GM-THRID ' + self.thread_id + ')')
        sent_messages = {}
        uids = results[0].split(' ')
        if response == 'OK':
            for uid in uids: sent_messages[uid] = Message(self.gmail.mailboxes['[Gmail]/Sent Mail'], uid)
            self.gmail.fetch_multiple_messages(sent_messages)
            self.gmail.mailboxes['[Gmail]/Sent Mail'].messages.update(sent_messages)

        self.gmail.use_mailbox(original_mailbox.name)

        # combine and sort sent and received messages
        return sorted(dict(received_messages.items() + sent_messages.items()).values(), key=lambda m: m.sent_at)


class Attachment:

    def __init__(self, attachment):
        self.name = attachment.get_filename()
        # Raw file data
        self.payload = attachment.get_payload(decode=True)
        # Filesize in kilobytes
        self.size = int(round(len(self.payload)/1000.0))

    def save(self, path=None):
        if path is None:
            # Save as name of attachment if there is no path specified
            path = self.name
        elif os.path.isdir(path):
            # If the path is a directory, save as name of attachment in that directory
            path = os.path.join(path, self.name)

        with open(path, 'wb') as f:
            f.write(self.payload)
