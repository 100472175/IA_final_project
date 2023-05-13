from constants import *
import numpy as np
import configparser
import os
from transitions import ExcelParser



class Markov:
    def __init__(self, file_path):
        self.transitions = None
        self.file_path = file_path
        self.options = ["heating", "cooling"]
        self.actions_to_take = {}
        self.parse_files()
        # Old:
        # self.verify_values_config()
        self.verify_values()
        self.transitions_dict = self.merge_transitions()
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
            print("File not found")
            exit(-1)
        self.config.read(self.file_path)

        # Load the Excel file
        self.transitions = ExcelParser(self.config.get("general", "transitions_path"))

    """def verify_values_config(self):
        # Check if the values are correct for each of the sections in the INI file
        for section in self.config.sections():
            if section == "general":
                continue
            add = 0
            for key in self.config.options(section):
                try:
                    add += float(self.config.get(section, key))
                except ValueError:
                    raise Exception("The value of {} is not a number".format(key))

            if 1 - add > 0.0001:
                print(add)
                raise Exception("The sum of the values of {} is not 1".format(section))"""


    def verify_values(self):
        data = self.data
        for element in data.heat_trans.keys():
            add = 0
            for key in data.heat_trans[element].keys():
                try:
                    data.heat_trans[element][key] = float(data.heat_trans[element][key])
                except ValueError:
                    raise Exception("The value of {} is not a number".format(key))
                add += data.heat_trans[element][key]
            if 1 - add > 0.0001:
                raise Exception("The sum of the values of {} is not 1".format(element))

        for element in data.cool_trans.keys():
            add = 0
            for key in data.cool_trans[element].keys():
                try:
                    data.cool_trans[element][key] = float(data.cool_trans[element][key])
                except ValueError:
                    raise Exception("The value of {} is not a number".format(key))
            add += data.cool_trans[element][key]
            if 1 - add > 0.0001:
                raise Exception("The sum of the values of {} is not 1".format(element))

    def merge_transitions(self):
        return {"heating": self.transitions.heat_trans, "cooling": self.transition.cool_trans}

    def assign_general_values(self):
        self.c_on = self.config.get("general", "cost_heating")
        self.c_off = self.config.get("general", "cost_cooling")
        self.tolerance = self.config.get("general", "tolerance")
        try:
            self.c_on = float(self.c_on)
        except ValueError:
            raise Exception("The cost of heating is not a number")
        try:
            self.c_off = float(self.c_off)
        except ValueError:
            raise Exception("The cost of cooling is not a number")
        try:
            self.tolerance = float(self.tolerance)
        except ValueError:
            raise Exception("The tolerance is not a number")

    def define_states(self):
        self.states_values = {}
        self.states = {}
        self.min_temp = self.config.get("general", "minimum_temperature")
        self.max_temp = self.config.get("general", "maximum_temperature")
        self.temp_step = self.config.get("general", "temperature_step")
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
        actions = [self.c_on, self.c_off]
        for i in self.transitions_dict.keys(): # i is the action, heating or cooling
            name = f'dict_{temperature}'
            for k in self.transitions_dict[i][name].keys():
                # Ahora estoy en en el diccionario del estado
                if self.transitions_dict[i][name][k] == 0:
                    continue
                actions += self.transitions_dict[i][name][k] * self.states_values[k]
        if actions[0] < actions[1]:
            return "Heating", actions[0]
        else:
            return "Cooling", actions[1]

    def _iterations(self):
        # TODO
        pass



    def _bellman2(self, temperature):
        # Get the values of all the states

        if temperature == self.desired:
            return "Cooling", 0
        elif temperature == self.min_temp:
            section = "minimum_temperature"
        elif temperature == self.max_temp:
            section = "maximum_temperature"
        elif temperature == self.max_temp - self.temp_step:
            section = "maximum-1_temperature"
        else:
            section = "normal"
        # Actions are on and off, declared as the cost of each action
        actions = [self.c_on, self.c_off]
        for i in range(2):
            data = {}
            working_section = section + "_" + self.options[i]
            for keys in self.config.options(working_section):
                data[keys] = float(self.config.get(working_section, keys))

            try:
                actions[i] += data["stay"] * self.states_values[temperature]
            except KeyError:
                pass
            try:
                actions[i] += data["next"] * self.states_values[temperature + TEMPERATURE_STEP]
            except KeyError:
                pass
            try:
                actions[i] += data["next2"] * self.states_values[temperature + 2 * TEMPERATURE_STEP]
            except KeyError:
                pass
            try:
                actions[i] += data["prev"] * self.states_values[temperature - TEMPERATURE_STEP]
            except KeyError:
                pass

        if actions[0] < actions[1]:
            return "Heating", actions[0]
        else:
            return "Cooling", actions[1]

    def _iterations2(self):
        while True:
            for temperature in self.states_values:
                if temperature == self.desired:
                    self.states[temperature] = 0
                    continue
                else:
                    if temperature == self.min_temp:
                        section = "minimum_temperature"
                    elif temperature == self.max_temp:
                        section = "maximum_temperature"
                    elif temperature == self.max_temp - self.temp_step:
                        section = "maximum-1_temperature"
                    else:
                        section = "normal"
                        # Actions are on and off, declared as the cost of each action
                    actions = [self.c_on, self.c_off]
                    for i in range(2):
                        data = {}
                        working_section = section + "_" + self.options[i]
                        for keys in self.config.options(working_section):
                            data[keys] = float(self.config.get(working_section, keys))
                        try:
                            actions[i] += data["stay"] * self.states[temperature]
                        except KeyError:
                            pass

                        try:
                            actions[i] += data["next"] * self.states[temperature + TEMPERATURE_STEP]
                        except KeyError:
                            pass

                        try:
                            actions[i] += data["next2"] * self.states[temperature + 2 * TEMPERATURE_STEP]
                        except KeyError:
                            pass

                        try:
                            actions[i] += data["prev"] * self.states[temperature - TEMPERATURE_STEP]
                        except KeyError:
                            pass

                    self.states_values[temperature] = min(actions)

                valids = 0
                for j in self.states_values.keys():
                    if abs(self.states_values[j] - self.states[j]) < self.tolerance:
                        valids += 1
                    else:
                        self.states[j] = self.states_values[j]
                if valids == len(self.states_values):
                    return



mk = Markov("config.ini")
mk.solve()
print(mk)
