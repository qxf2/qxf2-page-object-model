"""This module provides RP client static objects and variables.

Copyright (c) 2018 http://reportportal.io .

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import aenum as enum


RP_LOG_LEVELS = {
    60000: 'UNKNOWN',
    50000: 'FATAL',
    40000: 'ERROR',
    30000: 'WARN',
    20000: 'INFO',
    10000: 'DEBUG',
    5000: 'TRACE'
}


class _PresenceSentinel(object):
    """Sentinel object for the None type."""

    def __nonzero__(self):
        """Handle a conditional case like "if not ...".

        Added to handle a conditional clause on attributes that are this
        __class__ objects:
        >>> if not response.error:
        where response.error can be NOT_FOUND or NOT_SET
        The constant must represent False state in bool context.
        :return: bool
        """
        return False

    __bool__ = __nonzero__  # Python3 support


class ItemStartType(str, enum.Enum):
    """This class defines item type mapping."""

    BEFORE_CLASS = 'before_class'
    BEFORE_GROUPS = 'before_groups'
    BEFORE_METHOD = 'before_method'
    BEFORE_SUITE = 'before_suite'
    BEFORE_TEST = 'before_test'

    SUITE = 'class'
    STORY = 'groups'
    TEST = 'method'
    SCENARIO = 'suite'
    STEP = 'test'

    AFTER_CLASS = 'after_class'
    AFTER_GROUPS = 'after_groups'
    AFTER_METHOD = 'after_method'
    AFTER_SUITE = 'after_suite'
    AFTER_TEST = 'after_test'


class Priority(enum.IntEnum):
    """Generic enum for various operations prioritization."""

    PRIORITY_IMMEDIATE = 0x0
    PRIORITY_HIGH = 0x1
    PRIORITY_MEDIUM = 0x2
    PRIORITY_LOW = 0x3


ATTRIBUTE_LENGTH_LIMIT = 128
DEFAULT_PRIORITY = Priority.PRIORITY_MEDIUM
NOT_FOUND = _PresenceSentinel()
NOT_SET = _PresenceSentinel()
