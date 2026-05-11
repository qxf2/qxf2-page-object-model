"""
Command Executor Utility

This utility provides a simple and reusable way to execute CLI commands
from Python code and capture their response.

It can be used:
- Inside Qxf2 Page Object Model framework
- As a standalone utility in any Python project

What it captures:
- Executed command
- Exit code
- Standard output (stdout)
- Standard error (stderr)

No assertions or test logic are included here by design.
"""

import subprocess
import shutil
from dataclasses import dataclass
from typing import Optional, List


class UnsafeCommandError(ValueError):
    """
    Raised when an unsafe or invalid command is detected
    """
    pass


@dataclass
class CommandResult:
    """
    Holds the result of a CLI command execution
    """
    command: str
    exit_code: int
    stdout: str
    stderr: str


class CommandExecutor:
    """
    Executes CLI commands and returns structured results
    """

    @staticmethod
    def _validate_command(command: List[str]) -> None:
        """
        Validate command structure and executable safety
        """

        if not isinstance(command, list) or not command:
            raise UnsafeCommandError("Command must be a non-empty list")

        for arg in command:
            if not isinstance(arg, str):
                raise UnsafeCommandError(
                    "All command arguments must be strings"
                )

        executable = command[0]
        if shutil.which(executable) is None:
            raise UnsafeCommandError(
                f"Executable not found in PATH: {executable}"
            )

    @staticmethod
    def run(
        command: List[str],
        cwd: Optional[str] = None,
        timeout: int = 30,
        env: Optional[dict] = None
    ) -> CommandResult:
        """
        Execute a CLI command securely.

        :param command: Command and arguments as list
                        Example: ["git", "--version"]
        :param cwd: Directory in which command should be executed
        :param timeout: Max execution time in seconds
        :param env: Environment variables for command execution
        :return: CommandResult object
        """

        # Validate command before execution
        CommandExecutor._validate_command(command)

        completed_process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=cwd,
            timeout=timeout,
            env=env,
            check=False
        )

        return CommandResult(
            command=" ".join(command),
            exit_code=completed_process.returncode,
            stdout=completed_process.stdout.strip(),
            stderr=completed_process.stderr.strip()
        )


# -- START OF SCRIPT
if __name__ == "__main__":
    print("\nExample 1: Basic command execution")
    print("-" * 40)

    result = CommandExecutor.run(["echo", "hello-qxf2"])

    print(f"Command   : {result.command}")
    print(f"Exit Code : {result.exit_code}")
    print(f"STDOUT    : {result.stdout}")
    print(f"STDERR    : {result.stderr}")

    print("\nExample 2: Command with working directory")
    print("-" * 40)

    result = CommandExecutor.run(
        command=["git", "status"],
        cwd="."
    )

    print(f"Command   : {result.command}")
    print(f"Exit Code : {result.exit_code}")
    print(f"STDOUT    : {result.stdout}")
    print(f"STDERR    : {result.stderr}")


# """
# ====================
# How to use this util
# ====================

# 1. Run directly from terminal

# python utils/command_executor.py

# This will execute the examples defined under __main__.


# 2. Use inside tests or Page Objects

# from utils.command_executor import CommandExecutor

# result = CommandExecutor.run(["git", "--version"])

# assert result.exit_code == 0
# assert "git version" in result.stdout
# """
