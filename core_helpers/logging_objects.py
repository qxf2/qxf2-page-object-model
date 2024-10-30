"""
Helper class for Logging Objects
"""

from utils.Base_Logging import Base_Logging
from utils.stop_test_exception_util import Stop_Test_Exception
import logging

class Logging_Objects:
    def __init__(self):
        self.msg_list = []
        self.exceptions = []

    def write_test_summary(self):
        "Print out a useful, human readable summary"
        self.write('\n\n************************\n--------RESULT--------\nTotal number of checks=%d'%self.result_counter)
        self.write('Total number of checks passed=%d\n----------------------\n************************\n\n'%self.pass_counter)
        self.write('Total number of mini-checks=%d'%self.mini_check_counter)
        self.write('Total number of mini-checks passed=%d'%self.mini_check_pass_counter)
        self.make_gif()
        if self.gif_file_name is not None:
            self.write("Screenshots & GIF created at %s"%self.screenshot_dir)
        if len(self.exceptions) > 0:
            self.exceptions = list(set(self.exceptions))
            self.write('\n--------USEFUL EXCEPTION--------\n',level="critical")
            for (i,msg) in enumerate(self.exceptions,start=1):
                self.write(str(i)+"- " + msg,level="critical")

    def write(self,msg,level='info', trace_back=None):
        "Log the message"
        msg = str(msg)
        self.msg_list.append('%-8s:  '%level.upper() + msg)
        self.log_obj.write(msg,level,trace_back)

    def success(self,msg,level='success',pre_format='PASS: '):
        "Write out a success message"
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
                # Collect the failed scenarios for prettytable summary
                self.failed_scenarios.append(positive)
            else:
                self.success(negative,level="success")
        else:
            if flag is True:
                self.success(positive,level="success")
            else:
                self.failure(negative,level="error")
                # Collect the failed scenarios for prettytable summary
                self.failed_scenarios.append(negative)

    def get_failure_message_list(self):
        "Return the failure message list"
        return self.failure_message_list

    def failure(self,msg,level='error',pre_format='FAIL: '):
        "Write out a failure message"
        self.log_obj.write(pre_format + msg,level)
        self.result_counter += 1
        self.failure_message_list.append(pre_format + msg)
        if level.lower() == 'critical':
            raise Stop_Test_Exception("Stopping test because: "+ msg)

    def set_rp_logger(self,rp_pytest_service):
        "Set the reportportal logger"
        self.rp_logger = self.log_obj.setup_rp_logging(rp_pytest_service)
