"""
A module to house prettytable custom objects
This tail made objects are used by pytest to print table output of failure summary
"""
from prettytable.colortable import ColorTable, Theme, Themes

#pylint: disable=too-few-public-methods
class PrettyTableTheme(Themes):
    "A custom color theme object"
    Failure = Theme(default_color="31",
                    vertical_color="31",
                    horizontal_color="31",
                    junction_color="31")

class FailureSummaryTable():
    "Failure Summary Table to be printed in the pytest result summary"
    def __init__(self) -> None:
        """
        Initializer
        """
        # Create a pretty color table in red to mark failures
        self.table = ColorTable(theme=PrettyTableTheme.Failure)
        self.table.field_names = ["Tests Failed"]
        self.table.align = "l" # <- Align the content of the table left

    def print_table(self, testsummary: dict) -> None:
        """
        Print the Failure Summary table
        :param:
            :testsummary: A dict with testname as key and failed scenarios as a list
        """
        try:
            for testname, testscenarios in testsummary.items():
                self.table.add_row([f"{testname}:"])
                for scenario in testscenarios:
                    self.table.add_row([f"\u2717 {scenario}"]) # <- Add unicode x mark
                self.table.add_row([""]) # Add a empty row for spacing after a testname
            if testsummary:
                print(self.table)
        except Exception as err: # pylint: disable=broad-except
            print("Unable to print prettytable failure summary")
            raise err
