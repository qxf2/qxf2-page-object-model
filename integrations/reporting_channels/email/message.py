import datetime
import email
import re
import time
import os
from email.header import decode_header

class Message():


    def __init__(self, mailbox, uid):
        self.uid = uid
        self.mailbox = mailbox
        self.email = mailbox.email if mailbox else None

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
        self.email.imap.uid('STORE', self.uid, '+FLAGS', flag)
        if flag not in self.flags: self.flags.append(flag)

    def unread(self):
        flag = '\\Seen'
        self.email.imap.uid('STORE', self.uid, '-FLAGS', flag)
        if flag in self.flags: self.flags.remove(flag)

    def is_starred(self):
        return ('\\Flagged' in self.flags)

    def star(self):
        flag = '\\Flagged'
        self.email.imap.uid('STORE', self.uid, '+FLAGS', flag)
        if flag not in self.flags: self.flags.append(flag)

    def unstar(self):
        flag = '\\Flagged'
        self.email.imap.uid('STORE', self.uid, '-FLAGS', flag)
        if flag in self.flags: self.flags.remove(flag)

    def is_draft(self):
        return ('\\Draft' in self.flags)

    def has_label(self, label):
        full_label = '%s' % label
        return (full_label in self.labels)

    def add_label(self, label):
        full_label = '%s' % label
        self.email.imap.uid('STORE', self.uid, '+X-GM-LABELS', full_label)
        if full_label not in self.labels: self.labels.append(full_label)

    def remove_label(self, label):
        full_label = '%s' % label
        self.email.imap.uid('STORE', self.uid, '-X-GM-LABELS', full_label)
        if full_label in self.labels: self.labels.remove(full_label)


    def is_deleted(self):
        return ('\\Deleted' in self.flags)

    def delete(self):
        flag = '\\Deleted'
        self.email.imap.uid('STORE', self.uid, '+FLAGS', flag)
        if flag not in self.flags: self.flags.append(flag)

        trash = '[Gmail]/Trash' if '[Gmail]/Trash' in self.email.labels() else '[Gmail]/Bin'
        if self.mailbox.name not in ['[Gmail]/Bin', '[Gmail]/Trash']:
            self.move_to(trash)

    # def undelete(self):
    #     flag = '\\Deleted'
    #     self.email.imap.uid('STORE', self.uid, '-FLAGS', flag)
    #     if flag in self.flags: self.flags.remove(flag)


    def move_to(self, name):
        self.email.copy(self.uid, name, self.mailbox.name)
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
        try:
            match = re.search(r'FLAGS \((.*?)\)', headers)
            if match:
                flags = match.group(1).split()
                return flags
            else:
                return []
        except Exception as e:
            print(f"Error parsing flags: {e}")
            return []

    def parse_labels(self, headers):
        try:
            match = re.search(r'X-GM-LABELS \((.*?)\)', headers)
            if match:
                labels = match.group(1).split()
                labels = [label.replace('"', '') for label in labels]
                return labels
            else:
                return []
        except Exception as e:
            print(f"Error parsing labels: {e}")
            return []

    def parse_subject(self, encoded_subject):
        dh = decode_header(encoded_subject)
        default_charset = 'ASCII'
        subject_parts = []
        for part, encoding in dh:
            if isinstance(part, bytes):
                try:
                    subject_parts.append(part.decode(encoding or default_charset))
                except Exception as e:
                    print(f"Error decoding part {part} with encoding {encoding}: {e}")
                    subject_parts.append(part.decode(default_charset, errors='replace'))
            else:
                subject_parts.append(part)
        parsed_subject = ''.join(subject_parts)
        return parsed_subject

    def parse(self, raw_message):
        raw_headers = raw_message[0]
        raw_email = raw_message[1]

        if isinstance(raw_headers, bytes):
            raw_headers = raw_headers.decode('utf-8', errors='replace')

        if isinstance(raw_email, bytes):
            raw_email = raw_email.decode('utf-8', errors='replace')

        if not isinstance(raw_email, str):
            raise ValueError("Decoded raw_email is not a string")
        try:
            self.message = email.message_from_string(raw_email)

        except Exception as e:
            print(f"Error creating email message: {e}")
            raise

        self.to = self.message.get('to')
        self.fr = self.message.get('from')
        self.delivered_to = self.message.get('delivered_to')
        self.subject = self.parse_subject(self.message.get('subject'))

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

        thread_match = re.search(r'X-GM-THRID (\d+)', raw_headers)
        if thread_match:
            self.thread_id = thread_match.group(1)
        if re.search(r'X-GM-MSGID (\d+)', raw_headers):
            self.message_id = re.search(r'X-GM-MSGID (\d+)', raw_headers).groups(1)

        self.attachments = [
            Attachment(attachment) for attachment in self.message.get_payload()
                if not isinstance(attachment, str) and attachment.get('Content-Disposition') is not None
        ]

    def fetch(self):
        if not self.message:
            check_gmail_host = 'gmail.com' in self.email.IMAP_HOST

            if check_gmail_host:
                _, results = self.email.imap.uid('FETCH', self.uid, '(UID BODY.PEEK[] X-GM-THRID)')
                self.parse(results[0])

            else:
                _, results = self.email.imap.uid('FETCH', self.uid, '(UID BODY.PEEK[])')
                self.parse(results[0])

        return self.message


    def fetch_thread(self):
        self.fetch()
        original_mailbox = self.mailbox
        self.email.use_mailbox(original_mailbox.name)
        
        combined_messages = {}

        # Check whether it's Gmail or Outlook based on IMAP host
        check_gmail_host = 'gmail.com' in self.email.IMAP_HOST

        if check_gmail_host:
            # Gmail - Use X-GM-THRID for fetching the thread
            response, results = self.email.imap.uid('SEARCH', None, f'(X-GM-THRID {self.thread_id})')
        else:
            # Outlook - Use Message-ID and References to fetch the thread
            response, results = self.email.imap.uid('FETCH', self.uid, '(UID BODY[HEADER.FIELDS (References)])')
            if response == 'OK' and results:
                headers = results[0][1].decode('utf-8')
                message_id_match = re.search(r'References:\s*(.*)', headers)
                if message_id_match:
                    message_id = message_id_match.group(1).strip()
                    response, results = self.email.imap.uid('SEARCH', None, f'(HEADER References "{message_id}")')

        # Common processing for received messages
        if response == 'OK' and results and results[0]:
            uids = results[0].decode('utf-8').split(' ')
            received_messages = {uid: Message(original_mailbox, uid) for uid in uids}
            self.email.fetch_multiple_messages(received_messages)
            combined_messages.update(received_messages)
        else:
            print(f"No received messages found with thread ID: {self.thread_id} in {self.email.current_mailbox}.")

        # Fetch messages from the sent mail folder for both Gmail and Outlook
        sent_mailbox = '"[Gmail]/Sent Mail"' if check_gmail_host else 'Sent'
        self.email.use_mailbox(sent_mailbox)

        search_criteria = f'(X-GM-THRID {self.thread_id})' if check_gmail_host else f'(HEADER Message-ID "{message_id}")'
        response, results = self.email.imap.uid('SEARCH', None, search_criteria)
        if response == 'OK' and results and results[0]:
            uids = results[0].decode('utf-8').split(' ')
            sent_messages = {uid: Message(self.email.mailboxes[sent_mailbox], uid) for uid in uids}
            self.email.fetch_multiple_messages(sent_messages)
            combined_messages.update(sent_messages)
        else:
            print(f"No sent messages found in {sent_mailbox}.")

        self.email.use_mailbox(original_mailbox.name)
        # Combine and sort messages if any were found
        if combined_messages:
            sorted_messages = sorted(combined_messages.values(), key=lambda m: m.sent_at)
            return sorted_messages
        else:
            print("No messages found in the thread.")
            return None

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
