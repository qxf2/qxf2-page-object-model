"""
A module to house prettytable custom objects
This tail made objects are used by pytest to print table output of failure summary
"""
from abc import ABC, abstractmethod
from prettytable.colortable import ColorTable, Theme, Themes

#pylint: disable=too-few-public-methods
class PrettyTableTheme(Themes):
    "A custom color theme object"
    FAILURE = Theme(default_color="31",
                    vertical_color="31",
                    horizontal_color="31",
                    junction_color="31")

class SummaryTable(ABC):
    "An abstract Summary Table object"
    @abstractmethod
    def print_table(self, values_dict: dict):
        "Print the table"
        return

class FailureSummaryTable(SummaryTable):
    "Failure Summary Table to be printed in the pytest result summary"
    def __init__(self, title="Consolidated Failures") -> None:
        """
        Initializer
        """
        # Create a pretty color table in red to mark failures
        self.table = ColorTable(theme=PrettyTableTheme.FAILURE)
        self.table.title = title
        self.table.field_names = ["Tests Failed"]
        self.table.align = "l" # <- Align the content of the table left
        self.table.padding_width = 10

    def print_table(self, values_dict: dict) -> None:
        """
        Print the Failure Summary table
        :param:
            :values_dict: A dict with testname as key and failed scenarios as a list
        """
        try:
            for testname, testscenarios in values_dict.items():
                self.table.add_row([f"{testname}:"])
                for scenario in testscenarios:
                    self.table.add_row([f"\u2717 {scenario}"]) # <- Add unicode x mark
                self.table.add_row([""]) # Add a empty row for spacing after a testname
            print(self.table)
        except Exception as err: # pylint: disable=broad-except
            print("Unable to print prettytable failure summary")
            raise err

class ConfigSummaryTable(SummaryTable):
    "Configuration summary"
    def __init__(self, title="Test Configuration") -> None:
        """
        Initializer
        """
        # Create a pretty table to print config values
        self.table = ColorTable(theme=PrettyTableTheme.PASTEL)
        self.table.title = title
        self.table.field_names = ["Parameters", "Values"]
        self.table.align = "l" # <- Align the content of the table left
        self.table.padding_width = 10

    def print_table(self, values_dict: dict) -> None:
        """
        Print the configuration summary
        :param:
            :values_dict: A dict with config values
        """
        try: # pylint: disable=too-many-nested-blocks
            for key, value in values_dict.items():
                if key == "test":
                    continue
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        if isinstance(sub_value, dict):
                            for param, value in sub_value.items():
                                new_sub_key = sub_key + "_" + param
                                new_sub_value = value
                                self.table.add_row([new_sub_key, new_sub_value])
                        else:
                            if key in ["browser", "platform"]:
                                sub_key = key + '_' + sub_key
                            if sub_key == "flag":
                                sub_key = "remote_flag"
                            if not isinstance(sub_value, list):
                                self.table.add_row([sub_key, sub_value])
                            else:
                                self.table.add_row([sub_key, ",".join(sub_value)])
            print("\n")
            print(self.table)
            print("\n")
        except Exception as err: # pylint: disable=broad-except
            print("Unable to print prettytable failure summary")
            raise err
