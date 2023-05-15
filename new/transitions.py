"""
# Artificial Intelligence - Final Project Assignment
# Coded by Eduardo Alarcón and Alfonso Pineda
Module to import the transitions from the excel file
"""

import configparser
import os
import pandas as pd


class ExcelParser:
    """
    The dictionaries are called: dict_temperature, inside 'self.transition'
    ie: dict_16.5 as the key for the dictionary of the temperature 16.5
    """

    def __init__(self, config_path, excel_path):
        self.transition = None
        self.file_path = config_path
        self.transitions_path = excel_path
        self.config = None
        self.parse_config_file()
        self.heat_trans = self.parse_transitions("Heating")
        self.cool_trans = self.parse_transitions("Cooling")

    def parse_config_file(self):
        """
        Load the INI configuration file
        :return: None
        """

        self.config = configparser.ConfigParser()
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File {self.file_path} not found")
        self.config.read(self.file_path)

    def parse_transitions(self, action):
        """
        Parse the Excel file and return a dictionary with the transitions depending on the action
        :param action:
        :return:
        """
        if not os.path.exists(self.transitions_path):
            raise FileNotFoundError(f"File {self.transitions_path} not found at "
                                    f"{os.path.abspath('.')}")
        data_frame = pd.read_excel('data.xlsx', sheet_name=action)
        result = data_frame.to_dict(orient='records')
        # Remove the NaN values from the dictionary and replace them with 0
        result = [{k: v if pd.notna(v) else 0 for k, v in row.items()} for row in result]
        transition = {}
        base = int(self.config.get("general", "minimum_temperature"))
        for i, row_dict in enumerate(result):
            dict_name = f'dict_{i / 2 + base}'
            transition[dict_name] = row_dict

        for value in transition.values():
            value.pop("Unnamed: 0")

        return transition

    def __str__(self):
        string = "Heating transitions:\n"
        for i, j in self.heat_trans.items():
            string += str(i) + ": "
            string += j.__str__()
            string += "\n"
        string += "\nCooling transitions:\n"
        for i, j in self.cool_trans.items():
            string += str(i) + ": "
            string += j.__str__()
            string += "\n"
        return string


if __name__ == "__main__":
    a = ExcelParser("config.ini", "data.xlsx")
    print(a)
