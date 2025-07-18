"""
This module defines the `Gmail` class, which provides methods to interact with a Gmail account
via IMAP. The class includes functionalities to connect to the Gmail server, login using 
credentials, and manage various mailboxes. Also, has functions for fetching mailboxes,
selecting a specific mailbox, searching for and retrieving emails 
based on different criteria, managing labels, and handling authentication.
"""

from __future__ import absolute_import
import re
import imaplib
from .gmail import Mailbox
from integrations.reporting_channels.gmail.utf import encode as encode_utf7, decode as decode_utf7
from integrations.reporting_channels.gmail.exceptions import *

class Gmail():
    "Class interact with Gmail using IMAP"
    # GMail IMAP defaults
    GMAIL_IMAP_HOST = 'imap.gmail.com'
    GMAIL_IMAP_PORT = 993

    # GMail SMTP defaults
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
        # self.connect()

    def connect(self, raise_errors=True):
        "Establishes an IMAP connection to the Gmail server."
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

    def fetch_mailboxes(self):
        "Retrieves and stores the list of mailboxes available in the Gmail account."
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
        "Selects a specific mailbox for further operations."
        if mailbox:
            self.imap.select(mailbox)
        self.current_mailbox = mailbox
        return Mailbox(self, mailbox)

    def mailbox(self, mailbox_name):
        "Returns a Mailbox object for the given mailbox name."
        if mailbox_name not in self.mailboxes:
            mailbox_name = encode_utf7(mailbox_name)
        mailbox = self.mailboxes.get(mailbox_name)

        if mailbox and not self.current_mailbox == mailbox_name:
            self.use_mailbox(mailbox_name)

        return mailbox

    def create_mailbox(self, mailbox_name):
        "Creates a new mailbox with the given name if it does not already exist."
        mailbox = self.mailboxes.get(mailbox_name)
        if not mailbox:
            self.imap.create(mailbox_name)
            mailbox = Mailbox(self, mailbox_name)
            self.mailboxes[mailbox_name] = mailbox

        return mailbox

    def delete_mailbox(self, mailbox_name):
        "Deletes the specified mailbox and removes it from the cache."
        mailbox = self.mailboxes.get(mailbox_name)
        if mailbox:
            self.imap.delete(mailbox_name)
            del self.mailboxes[mailbox_name]

    def login(self, username, password):
        "Login to Gmail using the provided username and password. "
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

        return self.logged_in

    def authenticate(self, username, access_token):
        "Login to Gmail using OAuth2 with the provided username and access token."
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
        "Logout from the Gmail account and closes the IMAP connection."
        self.imap.logout()
        self.logged_in = False

    def label(self, label_name):
        "Retrieves a Mailbox object for the specified label (mailbox)."
        return self.mailbox(label_name)

    def find(self, mailbox_name="[Gmail]/All Mail", **kwargs):
        "Searches and returns emails based on the provided search criteria."
        box = self.mailbox(mailbox_name)
        return box.mail(**kwargs)

    def copy(self, uid, to_mailbox, from_mailbox=None):
        "Copies an email with the given UID from one mailbox to another."
        if from_mailbox:
            self.use_mailbox(from_mailbox)
        self.imap.uid('COPY', uid, to_mailbox)

    def fetch_multiple_messages(self, messages):
        "Fetches and parses multiple messages given a dictionary of `Message` objects."
        if not isinstance(messages, dict):
            raise Exception('Messages must be a dictionary')

        fetch_str = ','.join(messages.keys())
        response, results = self.imap.uid('FETCH', fetch_str, '(BODY.PEEK[] FLAGS X-GM-THRID X-GM-MSGID X-GM-LABELS)')

        for raw_message in results:
            if isinstance(raw_message, tuple):
                uid_match = re.search(rb'UID (\d+)', raw_message[0])
                if uid_match:
                    uid = uid_match.group(1).decode('utf-8')
                    if uid in messages:
                        messages[uid].parse(raw_message)
        return messages

    def labels(self, require_unicode=False):
        "Returns a list of all available mailbox names."
        keys = self.mailboxes.keys()
        if require_unicode:
            keys = [decode_utf7(key) for key in keys]
        return keys

    def inbox(self):
        "Returns a `Mailbox` object for the Inbox."
        return self.mailbox("INBOX")

    def spam(self):
        "Returns a `Mailbox` object for the Spam."
        return self.mailbox("[Gmail]/Spam")

    def starred(self):
        "Returns a `Mailbox` object for the starred folder."
        return self.mailbox("[Gmail]/Starred")

    def all_mail(self):
        "Returns a `Mailbox` object for the All mail."
        return self.mailbox("[Gmail]/All Mail")

    def sent_mail(self):
        "Returns a `Mailbox` object for the Sent mail."
        return self.mailbox("[Gmail]/Sent Mail")

    def important(self):
        "Returns a `Mailbox` object for the Important."
        return self.mailbox("[Gmail]/Important")

    def mail_domain(self):
        "Returns the domain part of the logged-in email address"
        return self.username.split('@')[-1]
