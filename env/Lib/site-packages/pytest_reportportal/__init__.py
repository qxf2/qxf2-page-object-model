"""This package contains Pytest agent's code for the Report Portal."""

from .rp_logging import RPLogger, RPLogHandler

__all__ = ['RPLogger', 'RPLogHandler']

LAUNCH_WAIT_TIMEOUT = 10
