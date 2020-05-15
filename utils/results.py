"""
Tracks test results and logs them.
Keeps counters of pass/fail/total.
"""
import logging
from utils.Base_Logging import Base_Logging


class Results(object):
    """ Base class for logging intermediate test outcomes """

    def __init__(self, level=logging.DEBUG, log_file_path=None):
        self.logger = Base_Logging(log_file_name=log_file_path, level=level)
        self.total = 0  # Increment whenever success or failure are called
        self.passed = 0  # Increment everytime success is called
        self.written = 0  # Increment when conditional_write is called
        # Increment when conditional_write is called with True
        self.written_passed = 0
        self.failure_message_list = []


    def assert_results(self):
        """ Check if the test passed or failed """
        assert self.passed == self.total


    def write(self, msg, level='info'):
        """ This method use the logging method """
        self.logger.write(msg, level)


    def record(self, condition, msg, level='debug', indent=1):
        """ Write out either the positive or the negative message based on flag """
        if condition:
            self.written_passed += 1

        prefix = ''
        for i in range(indent if indent > 0 else 0):
            prefix = prefix + '    '

        self.written += 1
        self.write(prefix + msg + (' False' if condition else ' True'), level)


    def conditional_write(self, condition, positive, negative, level='info', pre_format="  - "):
        """ Write out either the positive or the negative message based on flag """
        if condition:
            self.write(pre_format + positive, level)
            self.written_passed += 1
        else:
            self.write(pre_format + negative, level)
        self.written += 1


    def log_result(self, flag, positive, negative, level='info'):
        """ Write out the result of the test """
        if flag is True:
            self.success(positive, level=level)
        if flag is False:
            self.failure(negative, level=level)
            raise Exception
        self.write('~~~~~~~~\n', level)


    def success(self, msg, level='info', pre_format='PASS: '):
        """ Write out a success message """
        self.logger.write(pre_format + msg, level)
        self.total += 1
        self.passed += 1


    def failure(self, msg, level='info', pre_format='FAIL: '):
        """ Write out a failure message """
        self.logger.write(pre_format + msg, level)
        self.total += 1
        self.failure_message_list.append(pre_format + msg)


    def get_failure_message_list(self):
        """ Return the failure message list """

        return self.failure_message_list


    def write_test_summary(self):
        """ Print out a useful, human readable summary """
        self.write('\n************************\n--------RESULT--------\nTotal number of checks=%d' % self.total)
        self.write('Total number of checks passed=%d\n----------------------\n************************\n\n' % self.passed)
        self.write('Total number of mini-checks=%d' % self.written)
        self.write('Total number of mini-checks passed=%d' % self.written_passed)
        failure_message_list = self.get_failure_message_list()
        if len(failure_message_list) > 0:
            self.write('\n--------FAILURE SUMMARY--------\n')
            for msg in failure_message_list:
                self.write(msg)
