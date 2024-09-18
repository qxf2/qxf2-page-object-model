

"""

GMail! Woo!

"""

__title__ = 'gmail'
__version__ = '0.1'
__author__ = 'Charlie Guo'
__build__ = 0x0001
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2013 Charlie Guo'

from .email import Email
from .mailbox import Mailbox
from .message import Message
from .exceptions import EmailException, ConnectionError, AuthenticationError
from .utils import login, authenticate

