"""
Helper class for Logging Objects
"""

from utils.Base_Logging import Base_Logging
from utils.stop_test_exception_util import Stop_Test_Exception
import logging

class Logging_Objects:
    def write_test_summary(self):
        "Print out a useful, human readable summary"
        self.write('\n\n************************\n--------RESULT--------\nTotal number of checks=%d'%self.result_counter)
        self.write('Total number of checks passed=%d\n----------------------\n************************\n\n'%self.pass_counter)
        self.write('Total number of mini-checks=%d'%self.mini_check_counter)
        self.write('Total number of mini-checks passed=%d'%self.mini_check_pass_counter)
        failure_message_list = self.get_failure_message_list()
        if len(failure_message_list) > 0:
            self.write('\n--------FAILURE SUMMARY--------\n')
            for msg in failure_message_list:
                self.write(msg)
        if len(self.exceptions) > 0:
            self.exceptions = list(set(self.exceptions))
            self.write('\n--------USEFUL EXCEPTION--------\n')
            for (i,msg) in enumerate(self.exceptions,start=1):
                self.write(str(i)+"- " + msg)
        self.make_gif()
        if self.gif_file_name is not None:
            self.write("Screenshots & GIF created at %s"%self.screenshot_dir)
            self.write('************************')

    def write(self,msg,level='info'):
        "Log the message"
        msg = str(msg)
        self.msg_list.append('%-8s:  '%level.upper() + msg)
        if self.browserstack_flag is True:
            if self.browserstack_msg not in msg:
                self.msg_list.pop(-1) #Remove the redundant BrowserStack message
        self.log_obj.write(msg,level)

    def success(self,msg,level='info',pre_format='PASS: '):
        "Write out a success message"
        if level.lower() == 'critical':
            level = 'info'
        self.log_obj.write(pre_format + msg,level)
        self.result_counter += 1
        self.pass_counter += 1

    def set_log_file(self):
        "set the log file"
        self.log_name = self.testname + '.log'
        self.log_obj = Base_Logging(log_file_name=self.log_name,level=logging.DEBUG)

    def log_result(self,flag,positive,negative,level='info'):
        "Write out the result of the test"
        if level.lower() == "inverse":
            if flag is True:
                self.failure(positive,level="error")
            else:
                self.success(negative,level="info")
        else:
            if flag is True:
                self.success(positive,level=level)
            else:
                self.failure(negative,level=level)

    def get_failure_message_list(self):
        "Return the failure message list"
        return self.failure_message_list

    def failure(self,msg,level='info',pre_format='FAIL: '):
        "Write out a failure message"
        self.log_obj.write(pre_format + msg,level)
        self.result_counter += 1
        self.failure_message_list.append(pre_format + msg)
        if level.lower() == 'critical':
            self.teardown()
            raise Stop_Test_Exception("Stopping test because: "+ msg)

    def set_rp_logger(self,rp_pytest_service):
        "Set the reportportal logger"
        self.rp_logger = self.log_obj.setup_rp_logging(rp_pytest_service)
            