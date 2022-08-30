"""This module includes exceptions used in the package."""


class PytestWarning(UserWarning):
    """Pytest warning exception.

    This exception is about to stub absent PytestWarning in Pytest versions
    up to 3.8.0. Get rid of this code once we drop support for Pytest versions
    below 3.8.0.
    """
