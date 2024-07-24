"""
Qxf2 Services: A plug-n-play class for logging.
This class wraps around Python's loguru module.
"""
import os, inspect
import sys
import logging
from loguru import logger
import re
from reportportal_client import RPLogger, RPLogHandler

class Base_Logging():
    "A plug-n-play class for logging"
    def __init__(self,log_file_name=None,level="DEBUG"):
        "Constructor for the logging class"
        logger.remove()
        logger.add(sys.stderr,format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>")
        self.log_file_name=log_file_name
        self.log_file_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','log'))
        self.level=level
        self.set_log(self.log_file_name,self.level)
        self.rp_logger = None

    def set_log(self,log_file_name,level,log_format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",test_module_name=None):
        "Add an handler sending log messages to a sink"
        if test_module_name is None:
            test_module_name = self.get_calling_module()
        if not os.path.exists(self.log_file_dir):
            os.makedirs(self.log_file_dir)
        if log_file_name is None:
            log_file_name = self.log_file_dir + os.sep + test_module_name + '.log'
        else:
            log_file_name = self.log_file_dir + os.sep + log_file_name

        logger.add(log_file_name,level=level, format=log_format,
        rotation="30 days", filter=None, colorize=None, serialize=False, backtrace=True, enqueue=False, catch=True)
        # Create temporary log files for consolidating log data of all tests of a session to a single file
        logger.add(log_file_name + '-temp',level=level, format=log_format,
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


    def write(self,msg,level='info',trace_back=None):
        "Write out a message"
        all_stack_frames = inspect.stack()
        for stack_frame in all_stack_frames[2:]:
            if all(helper not in stack_frame[1] for helper in ['web_app_helper', 'mobile_app_helper', 'logging_objects']):
                break
        module_path = stack_frame[1]
        modified_path = module_path.split("qxf2-page-object-model")[-1]
        if module_path == modified_path:
            modified_path = module_path.split("project")[-1]

        fname = stack_frame[3]
        d = {'caller_func': fname, 'file_name': modified_path}

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

        exception_source = self.get_exception_module(trace_back)
        if level.lower() == 'debug':
            file_name = d['file_name']
            module = d['caller_func'] if d['caller_func'] != "inner" else exception_source
            logger.opt(colors=True).debug("<cyan>{file_name}</cyan>::<yellow>{module}</yellow> | {msg}", file_name=file_name, module=module, msg=msg)
        elif level.lower() == 'info':
            file_name = d['file_name']
            module = d['caller_func'] if d['caller_func'] != "inner" else exception_source
            logger.opt(colors=True).info("<cyan>{file_name}</cyan>::<yellow>{module}</yellow> | {msg}", file_name=file_name, module=module, msg=msg)
        elif level.lower() == 'warn' or level.lower() == 'warning':
            file_name = d['file_name']
            module = d['caller_func'] if d['caller_func'] != "inner" else exception_source
            logger.opt(colors=True).warn("<cyan>{file_name}</cyan>::<yellow>{module}</yellow> | {msg}", file_name=file_name, module=module, msg=msg)
        elif level.lower() == 'error':
            file_name = d['file_name']
            module = d['caller_func'] if d['caller_func'] != "inner" else exception_source
            logger.opt(colors=True).error("<cyan>{file_name}</cyan>::<yellow>{module}</yellow> | {msg}", file_name=file_name, module=module, msg=msg)
        elif level.lower() == 'critical':
            file_name = d['file_name']
            module = d['caller_func'] if d['caller_func'] != "inner" else exception_source
            logger.opt(colors=True).critical("<cyan>{file_name}</cyan>::<yellow>{module}</yellow> | {msg}", file_name=file_name, module=module, msg=msg)
        else:
            logger.critical("Unknown level passed for the msg: {}", msg)

    def get_exception_module(self,trace_back):
        "Get the actual name of the calling module where exception arises"
        module_name = None
        if trace_back is not None:
            try:
                pattern = r'in (\w+)\n'
                # Extracting file name using regular expression
                match = re.search(pattern, trace_back)
                module_name = match.group(1)
            except Exception as e:
                self.write("Module where exception arises not found.")
                self.write(str(e))
        return module_name
