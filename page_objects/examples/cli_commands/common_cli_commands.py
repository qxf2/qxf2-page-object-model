"""
This class models the common cli commands.
"""
# pylint: disable = W0212,E0401
from core_helpers.cli_helper import CliHelper
from utils.Wrapit import Wrapit

class CommonCliCommands(CliHelper):
    "Page objects for the common cli commands"
    @Wrapit._exceptionHandler
    def execute_echo_command(self, message):
        """
        Execute the echo command output
        """
        result_flag = False
        result = self.execute_command(["echo", message])
        if result is not None:
            self.write(result.stdout)
            result_flag = True

        self.conditional_write(result_flag,
                                positive='Successfully executed echo command',
                                negative='Failed to execute echo command')
        return  result

    @Wrapit._exceptionHandler
    def verify_echo_response(self, result, expected_message):
        """
        Verify the echo command output
        """
        result_flag = True

        if result is None:
            result_flag = False
            actual_output = "No result returned"
        else:
            actual_output = (result.stdout or "").strip()
            expected_message = expected_message.strip()

            if actual_output != expected_message:
                result_flag = False

        self.conditional_write(
            result_flag,
            positive=f"Echo output verified successfully: '{expected_message}'",
            negative=(
                f"Echo output verification failed | "
                f"Expected: '{expected_message}' | "
                f"Actual: '{actual_output}'"
            )
        )

        return result_flag

    @Wrapit._exceptionHandler
    def execute_echo_cmd_and_verify_response(self, message):
        "Execute echo command and verify response"
        result = self.execute_echo_command(message)

        if result is None or result.exit_code != 0:
            self.write("Echo command execution failed, skipping verification", level="error")
            return False, result

        result_flag = self.verify_echo_response(result, message)

        return result_flag, result

    @Wrapit._exceptionHandler
    def get_python_version(self):
        "Execute python --version command"
        result_flag = False
        result = self.execute_command(["python", "--version"])

        if result is not None:
            # python --version may write to stdout or stderr
            output = result.stdout or result.stderr
            if output:
                self.write(output.strip())
                result_flag = True

        self.conditional_write(
            result_flag,
            positive='Successfully executed python version command',
            negative='Failed to execute python version command'
        )

        return result

    @Wrapit._exceptionHandler
    def verify_python3_installed(self, result,version_string):
        """
        Verify python is installed and version is Python 3
        """
        result_flag = True

        if result is None:
            result_flag = False
            output = "No result returned"
        else:
            output = (result.stdout or result.stderr or "").strip()

            if result.exit_code != 0:
                result_flag = False
            elif not output.lower().startswith(version_string):
                result_flag = False

        self.conditional_write(
            result_flag,
            positive=f"Python 3 verified successfully: {output}",
            negative=f"Python 3 verification failed. Output: {output}"
        )

        return result_flag

    @Wrapit._exceptionHandler
    def execute_python_version_cmd_and_verify(self, version_string):
        "Execute python version command and verify Python 3 is installed"
        result = self.get_python_version()

        if result is None or result.exit_code != 0:
            self.write("Python version command execution failed, skipping verification",
                       level="error")
            return False, result

        result_flag = self.verify_python3_installed(result,version_string)

        return result_flag, result

    @Wrapit._exceptionHandler
    def cat_file(self, file_name):
        "Execute cat command on a given file"
        result_flag = False
        result = self.execute_command(["cat", file_name])

        if result is not None:
            self.write(result.stdout or result.stderr)
            result_flag = True

        self.conditional_write(
            result_flag,
            positive=f"Successfully executed cat command on {file_name}",
            negative=f"Failed to execute cat command on {file_name}"
        )

        return result

    @Wrapit._exceptionHandler
    def verify_file_contains_strings(self, result, expected_strings):
        """
        Verify given strings are present in file content

        :param result: command execution result
        :param expected_strings: list of strings expected in file
        """
        result_flag = True

        if result is None:
            result_flag = False
            output = "No result returned"
        else:
            output = (result.stdout or "").lower()

            for expected in expected_strings:
                if expected.lower() not in output:
                    result_flag = False
                    break

        self.conditional_write(
            result_flag,
            positive=f"File contains expected entries: {expected_strings}",
            negative=f"File does not contain expected entries: {expected_strings}"
        )

        return result_flag

    @Wrapit._exceptionHandler
    def execute_cat_file_and_verify(self, file_name, expected_strings):
        "Execute cat command on file and verify expected content"
        result = self.cat_file(file_name)

        if result is None or result.exit_code != 0:
            self.write(
                f"cat command execution failed for {file_name}, skipping verification",
                level="error"
            )
            return False, result

        result_flag = self.verify_file_contains_strings(result, expected_strings)

        return result_flag, result
