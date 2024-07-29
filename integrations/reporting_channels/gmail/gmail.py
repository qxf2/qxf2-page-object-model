from __future__ import absolute_import
import re
import imaplib
import logging
from email.header import decode_header

from integrations.reporting_channels.gmail.mailbox import Mailbox
from integrations.reporting_channels.gmail.utf import encode as encode_utf7, decode as decode_utf7
from integrations.reporting_channels.gmail.exceptions import *

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Gmail():
    # GMail IMAP defaults
    GMAIL_IMAP_HOST = 'imap.gmail.com'
    GMAIL_IMAP_PORT = 993

    # GMail SMTP defaults
    # TODO: implement SMTP functions
    GMAIL_SMTP_HOST = "smtp.gmail.com"
    GMAIL_SMTP_PORT = 587

    def __init__(self):
        self.username = None
        self.password = None
        self.access_token = None

        self.imap = None
        self.smtp = None
        self.logged_in = False
        self.mailboxes = {}
        self.current_mailbox = None
        self.messages = {}


        # self.connect()


    def connect(self, raise_errors=True):
        # try:
        #     self.imap = imaplib.IMAP4_SSL(self.GMAIL_IMAP_HOST, self.GMAIL_IMAP_PORT)
        # except socket.error:
        #     if raise_errors:
        #         raise Exception('Connection failure.')
        #     self.imap = None

        self.imap = imaplib.IMAP4_SSL(self.GMAIL_IMAP_HOST, self.GMAIL_IMAP_PORT)

        # self.smtp = smtplib.SMTP(self.server,self.port)
        # self.smtp.set_debuglevel(self.debug)
        # self.smtp.ehlo()
        # self.smtp.starttls()
        # self.smtp.ehlo()

        return self.imap


    # Add fetch_mailboxes method in the Gmail class
    def fetch_mailboxes(self):
        response, data = self.imap.list()
        if response == 'OK':
            mailboxes = []
            for item in data:
                decoded_item = decode_utf7(item)
                # Extract the mailbox name
                mailbox_name = decoded_item.split(' "/" ')[-1]
                mailboxes.append(mailbox_name.strip('"'))
            return mailboxes
        else:
            raise Exception("Failed to fetch mailboxes.")


    def use_mailbox(self, mailbox):
        if mailbox:
            self.imap.select(mailbox)
        self.current_mailbox = mailbox
        return Mailbox(self, mailbox)


    def mailbox(self, mailbox_name):
        if mailbox_name not in self.mailboxes:
            mailbox_name = encode_utf7(mailbox_name)
        mailbox = self.mailboxes.get(mailbox_name)

        if mailbox and not self.current_mailbox == mailbox_name:
            self.use_mailbox(mailbox_name)

        return mailbox

    def create_mailbox(self, mailbox_name):
        mailbox = self.mailboxes.get(mailbox_name)
        if not mailbox:
            self.imap.create(mailbox_name)
            mailbox = Mailbox(self, mailbox_name)
            self.mailboxes[mailbox_name] = mailbox

        return mailbox

    def delete_mailbox(self, mailbox_name):
        mailbox = self.mailboxes.get(mailbox_name)
        if mailbox:
            self.imap.delete(mailbox_name)
            del self.mailboxes[mailbox_name]



    def login(self, username, password):
        self.username = username
        self.password = password

        if not self.imap:
            self.connect()

        try:
            imap_login = self.imap.login(self.username, self.password)
            self.logged_in = (imap_login and imap_login[0] == 'OK')
            if self.logged_in:
                self.fetch_mailboxes()
        except imaplib.IMAP4.error:
            raise AuthenticationError


        # smtp_login(username, password)

        return self.logged_in

    def authenticate(self, username, access_token):
        self.username = username
        self.access_token = access_token

        if not self.imap:
            self.connect()

        try:
            auth_string = 'user=%s\1auth=Bearer %s\1\1' % (username, access_token)
            imap_auth = self.imap.authenticate('XOAUTH2', lambda x: auth_string)
            self.logged_in = (imap_auth and imap_auth[0] == 'OK')
            if self.logged_in:
                self.fetch_mailboxes()
        except imaplib.IMAP4.error:
            raise AuthenticationError

        return self.logged_in

    def logout(self):
        self.imap.logout()
        self.logged_in = False


    def label(self, label_name):
        return self.mailbox(label_name)

    def find(self, mailbox_name="[Gmail]/All Mail", **kwargs):
        box = self.mailbox(mailbox_name)
        return box.mail(**kwargs)


    def copy(self, uid, to_mailbox, from_mailbox=None):
        if from_mailbox:
            self.use_mailbox(from_mailbox)
        self.imap.uid('COPY', uid, to_mailbox)

    # def fetch_multiple_messages(self, messages):
    #     if not isinstance(messages, dict):
    #         raise Exception('Messages must be a dictionary')
    #     fetch_str = ','.join(messages.keys())
    #     response, results = self.imap.uid('FETCH', fetch_str, '(BODY.PEEK[] FLAGS X-GM-THRID X-GM-MSGID X-GM-LABELS)')
    #     for index in range(len(results) - 1):
    #         raw_message = results[index]
    #         if re.search(rb'UID (\d+)', raw_message[0]):
    #             uid = re.search(rb'UID (\d+)', raw_message[0]).groups(1)[0]
    #             print(f'type of" {uid}": {type(uid)}')
    #             converted_uid = str(uid[0])
    #             # convertedParsedUID = uid[0].split(b' ')
    #             self.messages[uid].parse(raw_message)
    #             print("messages",messages)

    #     return messages

    def fetch_multiple_messages(self, messages):
        if not isinstance(messages, dict):
            raise Exception('Messages must be a dictionary')
        
        fetch_str = ','.join(messages.keys())
        response, results = self.imap.uid('FETCH', fetch_str, '(BODY.PEEK[] FLAGS X-GM-THRID X-GM-MSGID X-GM-LABELS)')
        
        for raw_message in results:
            if isinstance(raw_message, tuple) and re.search(rb'UID (\d+)', raw_message[0]):
                uid_match = re.search(rb'UID (\d+)', raw_message[0])
                if uid_match:
                    uid = uid_match.group(1).decode('utf-8')  
                    # Ensure keys in messages are strings
                    if uid in messages:
                        messages[uid].parse(raw_message)  
                    else:
                        print(f'UID {uid} not found in messages dictionary')
                else:
                    print('UID not found in raw message')
            else:
                print('Invalid raw message format')

        return messages


    def labels(self, require_unicode=False):
        keys = self.mailboxes.keys()
        if require_unicode:
            keys = [decode_utf7(key) for key in keys]
        return keys

    def inbox(self):
        return self.mailbox("INBOX")

    def spam(self):
        return self.mailbox("[Gmail]/Spam")

    def starred(self):
        return self.mailbox("[Gmail]/Starred")

    def all_mail(self):
        return self.mailbox("[Gmail]/All Mail")

    def sent_mail(self):
        return self.mailbox("[Gmail]/Sent Mail")

    def important(self):
        return self.mailbox("[Gmail]/Important")

    def mail_domain(self):
        return self.username.split('@')[-1]