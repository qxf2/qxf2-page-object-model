# -*- coding: utf-8 -*-

"""
email.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of Emails' exceptions.

"""


class EmailException(RuntimeError):
    """There was an ambiguous exception that occurred while handling your
    request."""

class EmailConnectionError(EmailException):
    """A Connection error occurred."""

class AuthenticationError(EmailException):
    """Email Authentication failed."""

class Timeout(EmailException):
    """The request timed out."""
