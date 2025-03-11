import re
from .message import Message
from .utf import encode as encode_utf7, decode as decode_utf7

class Mailbox():
    def __init__(self, email, name="INBOX"):
        self.name = name
        self.email = email
        self.date_format = "%d-%b-%Y"
        self.messages = {}

    @property
    def external_name(self):
        if "external_name" not in vars(self):
            vars(self)["external_name"] = encode_utf7(self.name)
        return vars(self)["external_name"]

    @external_name.setter
    def external_name(self, value):
        if "external_name" in vars(self):
            del vars(self)["external_name"]
        self.name = decode_utf7(value)

    def mail(self, prefetch=False, **kwargs):
        search = ['ALL']

        if kwargs.get('read'):
            search.append('SEEN')
        if kwargs.get('unread'):
            search.append('UNSEEN')

        if kwargs.get('starred'):
            search.append('FLAGGED')
        if kwargs.get('unstarred'):
            search.append('UNFLAGGED')

        if kwargs.get('deleted'):
            search.append('DELETED')
        if kwargs.get('undeleted'):
            search.append('UNDELETED')

        if kwargs.get('draft'):
            search.append('DRAFT')
        if kwargs.get('undraft'):
            search.append('UNDRAFT')

        if kwargs.get('before'):
            search.extend(['BEFORE', kwargs['before'].strftime(self.date_format)])
        if kwargs.get('after'):
            search.extend(['SINCE', kwargs['after'].strftime(self.date_format)])
        if kwargs.get('on'):
            search.extend(['ON', kwargs['on'].strftime(self.date_format)])

        if kwargs.get('header'):
            search.extend(['HEADER', kwargs['header'][0], kwargs['header'][1]])

        if kwargs.get('sender'):
            search.extend(['FROM', kwargs['sender']])
        if kwargs.get('fr'):
            search.extend(['FROM', kwargs['fr']])
        if kwargs.get('to'):
            search.extend(['TO', kwargs['to']])
        if kwargs.get('cc'):
            search.extend(['CC', kwargs['cc']])

        if kwargs.get('subject'):
            search.extend(['SUBJECT', kwargs['subject']])
        if kwargs.get('body'):
            search.extend(['BODY', kwargs['body']])

        if kwargs.get('label'):
            search.extend(['X-GM-LABELS', kwargs['label']])
        if kwargs.get('attachment'):
            search.extend(['HAS', 'attachment'])

        if kwargs.get('query'):
            search.append(kwargs['query'])

        emails = []
        search_criteria = ' '.join(search).encode('utf-8')

        response, data = self.email.imap.uid('SEARCH', None, search_criteria)
        if response == 'OK':
            uids = filter(None, data[0].split(b' '))  # filter out empty strings

            for uid in uids:
                if not self.messages.get(uid):
                    self.messages[uid] = Message(self, uid)
                emails.append(self.messages[uid])

            if prefetch and emails:
                messages_dict = {}
                for email in emails:
                    messages_dict[email.uid] = email
                self.messages.update(self.email.fetch_multiple_messages(messages_dict))

        return emails

    # WORK IN PROGRESS. NOT FOR ACTUAL USE
    def threads(self, prefetch=False, **kwargs):
        emails = []
        response, data = self.email.imap.uid('SEARCH', None, 'ALL'.encode('utf-8'))
        if response == 'OK':
            uids = data[0].split(b' ')

            for uid in uids:
                if not self.messages.get(uid):
                    self.messages[uid] = Message(self, uid)
                emails.append(self.messages[uid])

            if prefetch:
                fetch_str = ','.join(uids).encode('utf-8')
                response, results = self.email.imap.uid('FETCH', fetch_str, '(BODY.PEEK[] FLAGS X-GM-THRID X-GM-MSGID X-GM-LABELS)')
                for index in range(len(results) - 1):
                    raw_message = results[index]
                    if re.search(rb'UID (\d+)', raw_message[0]):
                        uid = re.search(rb'UID (\d+)', raw_message[0]).groups(1)[0]
                        self.messages[uid].parse(raw_message)

        return emails

    def count(self, **kwargs):
        return len(self.mail(**kwargs))

    def cached_messages(self):
        return self.messages
