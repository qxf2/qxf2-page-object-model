"""
Helper class for Logging Objects
"""
import os,inspect
from utils.Base_Logging import Base_Logging
from utils.stop_test_exception_util import Stop_Test_Exception
from utils import Gif_Maker
import logging

class Logging_Objects:
    def __init__(self):
        self.msg_list = []
        self.exceptions = []
<<<<<<< HEAD
        self.browserstack_flag = False
        self.mini_check_counter = 0
        self.mini_check_pass_counter = 0
        self.result_counter = 0
        self.pass_counter = 0
        self.failure_message_list = []
        self.screenshot_dir = None
        self.calling_module = None
=======
>>>>>>> master

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

    def write(self,msg,level='info', trace_back=None):
        "Log the message"
        msg = str(msg)
        self.msg_list.append('%-8s:  '%level.upper() + msg)
        self.log_obj.write(msg,level,trace_back)

    def success(self,msg,level='info',pre_format='PASS: '):
        "Write out a success message"
        if level.lower() == 'critical':
            level = 'info'
        self.log_obj.write(pre_format + msg,level)
        self.result_counter += 1
        self.pass_counter += 1

    def set_log_file(self, log_file_path=None):
        "set the log file"
        if log_file_path == None:
            self.log_name = self.testname + '.log'
            self.log_obj = Base_Logging(log_file_name=self.log_name,level=logging.DEBUG)
        else:
            self.log_obj = Base_Logging(log_file_name=log_file_path, level=logging.DEBUG)

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
            raise Stop_Test_Exception("Stopping test because: "+ msg)

    def set_rp_logger(self,rp_pytest_service):
        "Set the reportportal logger"
        self.rp_logger = self.log_obj.setup_rp_logging(rp_pytest_service)

    def conditional_write(self,flag,positive,negative,level='info'):
        "Write out either the positive or the negative message based on flag"
        self.mini_check_counter += 1
        if level.lower() == "inverse":
            if flag is True:
                self.write(positive,level='error')
            else:
                self.write(negative,level='info')
                self.mini_check_pass_counter += 1
        else:
            if flag is True:
                self.write(positive,level='info')
                self.mini_check_pass_counter += 1
            else:
                self.write(negative,level='error')

    def make_gif(self):
        "Create a gif of all the screenshots within the screenshots directory"
        self.gif_file_name = Gif_Maker.make_gif(self.screenshot_dir,name=self.calling_module)

        return self.gif_file_name

    def set_calling_module(self,name):
        "Set the test name"
        self.calling_module = name

    def get_calling_module(self):
        "Get the name of the calling module"
        if self.calling_module is None:
            #Try to intelligently figure out name of test when not using pytest
            full_stack = inspect.stack()
            index = -1
            for stack_frame in full_stack:
                print(stack_frame[1],stack_frame[3])
                #stack_frame[1] -> file name
                #stack_frame[3] -> method
                if 'test_' in stack_frame[1]:
                    index = full_stack.index(stack_frame)
                    break
            test_file = full_stack[index][1]
            test_file = test_file.split(os.sep)[-1]
            testname = test_file.split('.py')[0]
            self.set_calling_module(testname)

        return self.calling_module
