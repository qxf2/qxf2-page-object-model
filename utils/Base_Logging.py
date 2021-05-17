"""
Qxf2 Services: A plug-n-play class for logging.
This class wraps around Python's loguru module.
"""
import os, inspect
import pytest,logging
from loguru import logger
from pytest_reportportal import RPLogger, RPLogHandler

class Base_Logging():
    "A plug-n-play class for logging"
    def __init__(self,log_file_name=None,level="DEBUG",format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module} | {message}"):
        "Constructor for the logging class"
        self.log_file_name=log_file_name
        self.log_file_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','log'))
        self.level=level
        self.format=format
        self.log = self.set_log(self.log_file_name,self.level,self.format)
        self.rp_logger = None


    def set_log(self,log_file_name,level,format,test_module_name=None):
        "Add an handler sending log messages to a sink"
        if test_module_name is None:
            test_module_name = self.get_calling_module()
        if not os.path.exists(self.log_file_dir):
            os.makedirs(self.log_file_dir)
        if log_file_name is None:
            log_file_name = self.log_file_dir + os.sep + test_module_name + '.log'
        else:
            log_file_name = self.log_file_dir + os.sep + log_file_name

        logger.add(log_file_name,level=level,format=format,
        rotation="30 days", filter=None, colorize=None, serialize=False, backtrace=True, enqueue=False, catch=True)


    def get_calling_module(self):
        "Get the name of the calling module"
        calling_file = inspect.stack()[-1][1]
        if 'runpy' in calling_file:
            calling_file = inspect.stack()[4][1]

        calling_filename = calling_file.split(os.sep)

        #This logic bought to you by windows + cygwin + git bash
        if len(calling_filename) == 1: #Needed for
            calling_filename = calling_file.split('/')

        self.calling_module = calling_filename[-1].split('.')[0]

        return self.calling_module


    def setup_rp_logging(self, rp_pytest_service):
        "Setup reportportal logging"
        try:
            # Setting up a logging.
            logging.setLoggerClass(RPLogger)
            self.rp_logger = logging.getLogger(__name__)
            self.rp_logger.setLevel(logging.INFO)
            # Create handler for Report Portal.
            rp_handler = RPLogHandler(rp_pytest_service)
            # Set INFO level for Report Portal handler.
            rp_handler.setLevel(logging.INFO)
            return self.rp_logger
        except Exception as e:
            self.write("Exception when trying to set rplogger")
            self.write(str(e))
            self.exceptions.append("Error when setting up the reportportal logger")


    def write(self,msg,level='info'):
        "Write out a message"
        #fname = inspect.stack()[2][3] #May be use a entry-exit decorator instead
        all_stack_frames = inspect.stack()
        for stack_frame in all_stack_frames[1:]:
            if 'Base_Page' not in stack_frame[1]:
                break
        fname = stack_frame[3]
        d = {'caller_func': fname}
        if self.rp_logger:
            if level.lower()== 'debug':
                self.rp_logger.debug(msg=msg)
            elif level.lower()== 'info':
                self.rp_logger.info(msg)
            elif level.lower()== 'warn' or level.lower()=='warning':
                self.rp_logger.warning(msg)
            elif level.lower()== 'error':
                self.rp_logger.error(msg)
            elif level.lower()== 'critical':
                self.rp_logger.critical(msg)
            else:
                self.rp_logger.critical(msg)
            return

        if level.lower()== 'debug':
            logger.debug("{module} | {msg}",module=d['caller_func'],msg=msg)
        elif level.lower()== 'info':
            logger.info("{module} | {msg}",module=d['caller_func'],msg=msg)
        elif level.lower()== 'warn' or level.lower()=='warning':
            logger.warning("{module} | {msg}",module=d['caller_func'],msg=msg)
        elif level.lower()== 'error':
            logger.error("{module} | {msg}",module=d['caller_func'],msg=msg)
        elif level.lower()== 'critical':
            logger.critical("{module} | {msg}",module=d['caller_func'],msg=msg)
        else:
            logger.critical("Unknown level passed for the msg: {}", msg)