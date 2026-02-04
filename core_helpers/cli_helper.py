"""
CLI Helper

Helper class to interact with command-line tools.
Follows the same design pattern as other helpers in core_helpers.
"""
from .logging_objects import Logging_Objects
#from utils import Results
from utils.command_executor import CommandExecutor

class Borg:
    """
    The borg design pattern is to share state
    #Src: http://code.activestate.com/recipes/66531/
    """
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state

    def is_first_time(self):
        "Has the child class been invoked before?"
        result_flag = False
        if len(self.__dict__)==0:
            result_flag = True

        return result_flag

class CliHelper(Borg, Logging_Objects):
    """
    CLI helper to execute terminal commands
    """
    def __init__(self, workdir=None, timeout=30):
        "Constructor"
        Borg.__init__(self)
        self.workdir = workdir
        self.timeout = timeout
        self.msg_list = []
        self.reset()

    def reset(self):
        "Reset the base page object"
        self.result_counter = 0 #Increment whenever success or failure are called
        self.pass_counter = 0 #Increment everytime success is called
        self.mini_check_counter = 0 #Increment when conditional_write is called
        self.mini_check_pass_counter = 0 #Increment when conditional_write is called with True
        self.failure_message_list = []
        self.failed_scenarios = [] # <- Collect the failed scenarios for prettytable summary
        self.screenshot_counter = 1
        self.exceptions = []
        self.gif_file_name = None
        self.rp_logger = None
        self.highlight_flag = False

    def set_params_and_log_file(self,testname,workdir,timeout):
        "set params and call set log file"
        self.workdir = workdir
        self.timeout = timeout
        self.testname = testname
        self.set_log_file()

    def execute_command(self, command):
        """
        Execute a CLI command and return the execution result
        """
        return CommandExecutor.run(
            command=command,
            cwd=self.workdir,
            timeout=self.timeout
        )

    def execute_command_and_verify_success(self, command):
        """
        Execute a CLI command and verify successful execution
        """
        result_flag = True
        result = self.execute_command(command)

        if result.exit_code != 0:
            result_flag = False

        return result_flag,result
