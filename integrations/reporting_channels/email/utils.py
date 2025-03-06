

from .email import Email

def login(username, password):
    email = Email()
    email.login(username, password)
    return email

def authenticate(username, access_token):
    email = Email()
    email.authenticate(username, access_token)
    return email