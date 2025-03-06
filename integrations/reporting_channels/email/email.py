from __future__ import absolute_import
import os
import sys
import re
import imaplib
import logging
from dotenv import load_dotenv
from integrations.reporting_channels.email.mailbox import Mailbox
from integrations.reporting_channels.email.utf import encode as encode_utf7, decode as decode_utf7
from integrations.reporting_channels.email.exceptions import *
from integrations.reporting_channels.email.exceptions import AuthenticationError
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Email():
    # EMail IMAP defaults
    IMAP_HOST = os.getenv('imaphost')
    IMAP_PORT = 993

    # EMail SMTP defaults
    EMAIL_SMTP_HOST = os.getenv('smtp_ssl_host')
    EMAIL_SMTP_PORT = os.getenv('smtp_ssl_port')

    def __init__(self):
        self.username = None
        self.password = None
        self.access_token = None

        self.imap = None
        self.smtp = None
        self.logged_in = False
        self.mailboxes = {}
        self.current_mailbox = None


        # self.connect()


    def connect(self, raise_errors=True):
        # try:
        #     self.imap = imaplib.IMAP4_SSL(self.GMAIL_IMAP_HOST, self.GMAIL_IMAP_PORT)
        # except socket.error:
        #     if raise_errors:
        #         raise Exception('Connection failure.')
        #     self.imap = None

        self.imap = imaplib.IMAP4_SSL(self.IMAP_HOST, self.IMAP_PORT)

        # self.smtp = smtplib.SMTP(self.server,self.port)
        # self.smtp.set_debuglevel(self.debug)
        # self.smtp.ehlo()
        # self.smtp.starttls()
        # self.smtp.ehlo()

        return self.imap


    # Add fetch_mailboxes method in the Email class
    def fetch_mailboxes(self):
        response, mailbox_list = self.imap.list()
        if response == 'OK':
            mailbox_list = [item.decode('utf-8') if isinstance(item, bytes) else item for item in mailbox_list]
            for mailbox in mailbox_list:
                mailbox_name = mailbox.split('"/"')[-1].replace('"', '').strip()
                mailbox = Mailbox(self)
                mailbox.external_name = mailbox_name
                self.mailboxes[mailbox_name] = mailbox
            return list(self.mailboxes.keys())
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

    def fetch_multiple_messages(self, messages):
        if not isinstance(messages, dict):
            raise Exception('Messages must be a dictionary')

        fetch_str = ','.join(messages.keys())
        _, results = self.imap.uid('FETCH', fetch_str, '(UID BODY.PEEK[] FLAGS)')

        for raw_message in results:
            if isinstance(raw_message, tuple):
                uid_match = re.search(rb'UID (\d+)', raw_message[0])
                if uid_match:
                    uid = uid_match.group(1).decode('utf-8')
                    if uid in messages:
                        messages[uid].parse(raw_message)
                    else:
                        logging.warning(f'UID {uid} not found in messages dictionary')
                else:
                    logging.warning('UID not found in raw message')
            elif isinstance(raw_message, bytes):
                continue
            else:
                logging.warning('Invalid raw message format')

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