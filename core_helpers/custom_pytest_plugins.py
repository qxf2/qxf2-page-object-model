"""
This module houses custom pytest plugins implemented
Plugins added:
- CustomTerminalReporter: Print a prettytable failure summary using pytest
"""

from _pytest.terminal import TerminalReporter
from .prettytable_object import FailureSummaryTable # pylint: disable=relative-beyond-top-level

class CustomTerminalReporter(TerminalReporter): # pylint: disable=subclassed-final-class
    "A custom pytest TerminalReporter plugin"
    def __init__(self, config):
        self.failed_scenarios = {}
        super().__init__(config)

    # Overwrite the summary_failures method to print the prettytable summary
    def summary_failures(self):
        if self.failed_scenarios:
            table = FailureSummaryTable()
            # Print header
            self.write_sep(sep="=", title="Failure Summary", red=True)
            # Print table
            table.print_table(self.failed_scenarios)
