import argparse

import numpy as np
import configparser
import os
from transitions import ExcelParser


class Markov:
    def __init__(self, file_path, desired=None):
        self.min_temp = None
        self.max_temp = None
        self.temp_step = None
        self.desired = desired
        self.c_on = None
        self.c_off = None
        self.tolerance = None
        self.config = None
        self.states_values = None
        self.states = None

        self.file_path = file_path
        self.actions_to_take = {}
        self.parse_files()
        self.verify_values()

        self.assign_general_values()
        self.define_states()

    def __str__(self):
        list_to_return = ""
        for i in self.actions_to_take.keys():
            list_to_return += ("For the temperature: {} - the optimal policy is: {}, with a cost of: {}"
                               .format(i, self.actions_to_take[i][0], self.actions_to_take[i][1]))
            list_to_return += "\n"
        return list_to_return

    def parse_files(self):
        # Load the INI configuration file
        self.config = configparser.ConfigParser()
        if not os.path.exists(self.file_path):
            print('Configuration file: {} not found at {}'.format(self.file_path, os.path.abspath('.')))
            exit(-1)
        self.config.read(self.file_path)

        # Load the Excel file
        transitions = ExcelParser(self.file_path, self.config.get("general", "transitions_path"))
        self.transitions_dict = {"heating": transitions.heat_trans,
                                 "cooling": transitions.cool_trans}

    def verify_values(self):
        for j, i in self.transitions_dict.items():
            for element in i.keys():
                add = 0
                for key in i[element].keys():
                    try:
                        i[element][key] = float(i[element][key])
                    except ValueError:
                        raise Exception("The value of {} is not a number".format(key))
                    add += i[element][key]
                if abs(1 - add) > 0.0001:
                    raise Exception("The sum of the probabilities of {} in the transition {} is not 1".format(element, j))

    def assign_general_values(self):
        try:
            self.c_on = float(self.config.get("general", "cost_heating"))
        except ValueError:
            raise Exception("The cost of heating is not a number")
        try:
            self.c_off = float(self.config.get("general", "cost_cooling"))
        except ValueError:
            raise Exception("The cost of cooling is not a number")
        try:
            self.tolerance = float(self.config.get("general", "tolerance"))
        except ValueError:
            raise Exception("The tolerance is not a number")

    def define_states(self):
        self.states_values = {}
        self.states = {}
        self.min_temp = self.config.get("general", "minimum_temperature")
        self.max_temp = self.config.get("general", "maximum_temperature")
        self.temp_step = self.config.get("general", "temperature_step")
        if self.desired is None:
            self.desired = self.config.get("general", "desired_temperature")
        try:
            self.min_temp = float(self.min_temp)
            self.max_temp = float(self.max_temp)
            self.temp_step = float(self.temp_step)
            self.desired = float(self.desired)

        except ValueError:
            raise Exception("The values of the general section are not numbers")
        for i in np.arange(self.min_temp, self.max_temp + self.temp_step, self.temp_step):
            self.states[i] = 0
            self.states_values[i] = 0
        if self.desired not in self.states.keys():
            raise ValueError("The desired temperature is not in the range of temperatures")

    def solve(self):
        self._iterations()
        for i in np.arange(self.min_temp, self.max_temp + self.temp_step, self.temp_step):
            self.actions_to_take[i] = self._bellman(i)
            # print(self.states_values)

    def _bellman(self, temperature):
        if temperature == self.desired:
            return "Cooling", 0
        actions = {"heating": self.c_on, "cooling": self.c_off}
        for i in self.transitions_dict.keys():  # for each of the actions, heating or cooling
            name = f'dict_{float(temperature)}'
            for k in self.transitions_dict[i][name].keys():
                if self.transitions_dict[i][name][k] == 0:
                    continue
                actions[i] += self.transitions_dict[i][name][k] * self.states_values[k]

        if actions["heating"] < actions["cooling"]:
            return "Heating", actions["heating"]
        else:
            return "Cooling", actions["cooling"]

    def _iterations(self):
        while True:
            for temperature in self.states_values:
                if temperature == self.desired:
                    continue
                else:
                    actions = {"heating": self.c_on, "cooling": self.c_off}
                    for i in actions.keys():
                        for k in self.transitions_dict[i][f'dict_{temperature}'].keys():
                            actions[i] += self.transitions_dict[i][f'dict_{temperature}'][k] * self.states_values[k]
                    self.states_values[temperature] = min(actions.values())

            valids = 0
            for j in self.states_values.keys():
                if abs(self.states_values[j] - self.states[j]) < self.tolerance:
                    valids += 1
                else:
                    self.states[j] = self.states_values[j]
            if valids == len(self.states_values):
                return


# Parse the arguments:
parser = argparse.ArgumentParser(description='Markov Decision Process')
parser.add_argument("-g", "--goal", help="desired temperature")
parser.add_argument("-f", "--file", help="config file path")
args = parser.parse_args()

if args.file is None:
    args.file = "config.ini"

mk = Markov(args.file, args.goal)
mk.solve()
print(mk)
