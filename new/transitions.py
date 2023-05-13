import pandas as pd
import configparser
import os


class ExcelParser:
    """
    The dictionaries are called: dict_temperature, inside self.transition
    ie: dict_16.5 as the key for the dictionary of the temperature 16.5
    """

    def __init__(self, config_path, excel_path):
        self.transition = None
        self.file_path = config_path
        self.transitions_path = excel_path
        self.parse_config_file()
        self.heat_trans = self.parse_transitions("Heating")
        self.cool_trans = self.parse_transitions("Cooling")

    def parse_config_file(self):
        # Load the INI configuration file
        self.config = configparser.ConfigParser()
        if not os.path.exists(self.file_path):
            print("File not found")
            exit(-1)
        self.config.read(self.file_path)

    def parse_transitions(self, action):
        if not os.path.exists(self.transitions_path):
            print("File not found")
            exit(-1)
        df = pd.read_excel('data.xlsx', sheet_name=action)
        result = df.to_dict(orient='records')
        # Remove the NaN values from the dictionary and replace them with 0
        result = [{k: v if pd.notna(v) else 0 for k, v in row.items()} for row in result]
        transition = {}
        base = int(self.config.get("general", "minimum_temperature"))
        for i, row_dict in enumerate(result):
            dict_name = f'dict_{i / 2 + base}'
            transition[dict_name] = row_dict

        for key in transition.keys():
            transition[key].pop("Unnamed: 0")

        """for dict_name, row_dict in self.transition.items():
            print(f'{dict_name}: {row_dict}')"""
        return transition

if __name__ == "__main__":
    a = ExcelParser("config.ini", "data.xlsx")