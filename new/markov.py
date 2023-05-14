import argparse

import numpy as np
import configparser
import os
from transitions import ExcelParser


class Markov:
    def __init__(self, file_path, desired=None):
        # General values for the MDP
        self.min_temp = None
        self.max_temp = None
        self.temp_step = None
        self.c_on = None
        self.c_off = None
        self.tolerance = None
        self.config = None
        self.states_values = None
        self.states = None
        self.desired = desired
        self.transitions_dict = {}
        self.actions_to_take = {}

        self.file_path = file_path
        # Get the data from the configuration file
        self.parse_files()

        # Verify the transitions from the ExcelParser are valid
        self.verify_values()

        # Define the costs for the actions and the tolerance
        self.assign_general_values()

        # Define the dictionary with the states
        self.define_states()

    def __str__(self) -> str:
        """
        Generate a string with the optimal policy for each temperature and the cost of the policy
        """
        list_to_return = ""
        for i in self.actions_to_take.keys():
            list_to_return += ("For the temperature: {} - the optimal policy is: {}, with a cost of: {}"
                               .format(i, self.actions_to_take[i][0], self.actions_to_take[i][1]))
            list_to_return += "\n"
        return list_to_return

    def parse_files(self):
        """
        Get the configuration file and the Excel file
        :return:
        """
        # Load the INI configuration file
        self.config = configparser.ConfigParser()
        if not os.path.exists(self.file_path):
            print('Configuration file: {} not found at {}'.format(self.file_path, os.path.abspath('.')))
            exit(-1)
        self.config.read(self.file_path)

        # Load the Excel file and get the transitions
        transitions = ExcelParser(self.file_path, self.config.get("general", "transitions_path"))
        self.transitions_dict = {"heating": transitions.heat_trans,
                                 "cooling": transitions.cool_trans}

    def verify_values(self):
        """
        Loop through all the transitions of the ExcelParser and verify that the values are valid
        by checking if the probabilities add to 1
        :return: None
        """
        # Loop through the two sheets of the ExcelParser, heating and cooling
        for j, i in self.transitions_dict.items():
            # Loop through the rows of the ExcelParser, which are the states from where you are
            for element in i.keys():
                add = 0
                # Loop through the columns of the ExcelParser, which are the states to where you are going
                # If the addition of all the states is not 1, raise an exception
                for key in i[element].keys():
                    try:
                        i[element][key] = float(i[element][key])
                    except ValueError:
                        raise Exception("The value of {} is not a number".format(key))
                    add += i[element][key]
                if abs(1 - add) > 0.0001:
                    raise Exception("The sum of the probabilities of {} in the transition "
                                    "{} is not 1".format(element, j))

    def assign_general_values(self):
        """
        Assign the values of the cost of each of the actions and the tolerance of the configuration
        file to the variables of the class
        :return: None
        """
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
        """
        The two dictionaries are created to have the values states for the iterations we have to do,
        until the tolerance is met and another one when we want to calculate the cost of the states.
        We have to check these are acceptable values, which are numbers, floats.
        We also have to check that the minimum temperature is lower than the maximum temperature.

        To generate these dictionaries, we loop through the range of temperatures, from the minimum
        to the maximum, with the step defined in the configuration file. We also check that the desired
        temperature is in the range of temperatures, which can be obtained from the arguments or from
        the configuration file or the command line.
        :return: None
        """
        # Check the values of the temperature, the step and the desired temperature
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
        if self.min_temp > self.max_temp:
            raise Exception("The minimum temperature is higher than the maximum temperature")

        # Create the dictionaries with the states
        self.states_values = {}
        self.states = {}
        for i in np.arange(self.min_temp, self.max_temp + self.temp_step, self.temp_step):
            self.states[i] = 0
            self.states_values[i] = 0
        if self.desired not in self.states.keys():
            raise ValueError("The desired temperature is not in the range of temperatures")

    def solve(self):
        """
        Solve the Markov Decision Process by iterating until the tolerance is met
        Then, we assign for each state, the optimal action to take and the cost of that state to
        reach the goal destination
        :return: None
        """
        # Iterate until the tolerance is met
        self._iterations()
        for i in np.arange(self.min_temp, self.max_temp + self.temp_step, self.temp_step):
            self.actions_to_take[i] = self._bellman(i)

    def _bellman(self, temperature):
        """
        Calculate the optimal action to take and the cost of that action using the bellman equation
        knowing the cost of each state and the transition probabilities
        :param temperature:
        :return: action, cost
        """
        # If the temperature is the desired, the value of that state is 0
        if temperature == self.desired:
            return "Cooling", 0

        # Calculate the cost of each action by doing the possible transitions and multiplying the
        # probability of that transition by the value of the state to where you are going
        # Then, we choose the action with the lowest cost and return it
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
        """
        Iterate until the tolerance is met, doing the bellman equation for each of the states, getting
        the optimal action to take and the cost of that action. We are only interested in this case
        in the cost of the action, so we only save that value in the dictionary of the states values
        :return: None
        """
        # Iterate indefinitely until the tolerance is met, which will exit the function
        while True:
            # For each of the states, we calculate the cost of each action, choosing the one with
            # the lowest cost
            for temperature in self.states_values:
                if temperature == self.desired:
                    continue
                else:
                    actions = {"heating": self.c_on, "cooling": self.c_off}
                    # Iterate through the two actions, heating and cooling, and calculate the cost
                    for i in actions.keys():
                        for k in self.transitions_dict[i][f'dict_{temperature}'].keys():
                            # If the probability of the transition is 0, we don't do anything special
                            # as the multiplication will be 0, so we can leave the transition there
                            actions[i] += self.transitions_dict[i][f'dict_{temperature}'][k] * self.states_values[k]
                    self.states_values[temperature] = min(actions.values())

            # Check the tolerance is met for all the states, if it is, we exit the function
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

# If there is no config file, we use the default one
if args.file is None:
    args.file = "config.ini"

mk = Markov(args.file, args.goal)
mk.solve()
print(mk)
