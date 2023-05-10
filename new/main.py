from constants import *
import numpy as np

global states
global states_final_values
states_final_values = {}
states = {}
for i in np.arange(MIN_TEMP, MAX_TEMP + TEMPERATURE_STEP, TEMPERATURE_STEP):
    states[i] = 0
    states_final_values[i] = 0


class Markov:
    def __init__(self):
        self.c_on = 10
        self.c_off = 5
        self.tolerance = 0.000001
        self.objective = 22
        for i in np.arange(MIN_TEMP, MAX_TEMP+TEMPERATURE_STEP, TEMPERATURE_STEP):
            print(i, self.bellman(i))


    def bellman(self, temperature):
        # Get the values of all the states
        self.iterations()

        # Actions is ON and OFF
        actions = [0, 0]
        if temperature == 16:
            actions[0] = (self.c_on + 0.3 * states_final_values[temperature] +
                          0.5 * states_final_values[temperature + TEMPERATURE_STEP] +
                          0.2 * states_final_values[temperature + 2 * TEMPERATURE_STEP])
            actions[1] = (self.c_off + 0.1 * states_final_values[temperature + TEMPERATURE_STEP] +
                          0.9 * states_final_values[temperature])
        elif temperature == 25:
            actions[0] = (self.c_on + 0.1 * states_final_values[temperature - TEMPERATURE_STEP] +
                          0.9 * states_final_values[temperature])
            actions[1] = (self.c_off + 0.3 * states_final_values[temperature] +
                          0.7 * states_final_values[temperature - TEMPERATURE_STEP])
        elif temperature == 24.5:
            actions[0] = (self.c_on + 0.7 * states_final_values[temperature + TEMPERATURE_STEP] +
                          0.2 * states_final_values[temperature] +
                          0.1 * states_final_values[temperature - TEMPERATURE_STEP])
            actions[1] = (self.c_off + 0.7 * states_final_values[temperature - TEMPERATURE_STEP]
                          + 0.1 * states_final_values[temperature + TEMPERATURE_STEP]
                          + 0.2 * states_final_values[temperature])
        else:
            actions[0] = (self.c_on + 0.5 * states_final_values[temperature + TEMPERATURE_STEP] +
                          0.2 * states_final_values[temperature + 2 * TEMPERATURE_STEP] +
                          0.2 * states_final_values[temperature] +
                          0.1 * states_final_values[temperature - TEMPERATURE_STEP])
            actions[1] = (self.c_off + 0.7 * states_final_values[temperature - TEMPERATURE_STEP] +
                          0.1 * states_final_values[temperature + TEMPERATURE_STEP] +
                          0.2 * states_final_values[temperature])
        if actions[0] < actions[1]:
            return "Heating", actions[0]
        else:
            return "Cooling", actions[1]

    def iterations(self):
        while True:
            for temperature in states_final_values:
                if temperature == self.objective:
                    states[temperature] = 0
                    continue
                else:
                    working_temp = 0
                    if temperature == 16:
                        states_final_values[temperature] = min(self.c_on + 0.3 * states[temperature] +
                                           0.5 * states[temperature + TEMPERATURE_STEP] +
                                           0.2 * states[temperature + 2 * TEMPERATURE_STEP],
                                           self.c_off + 0.1 * states[temperature + TEMPERATURE_STEP] +
                                           0.9 * states[temperature])
                    elif temperature == 25:
                        states_final_values[temperature] = min(self.c_on + 0.1 * states[temperature - TEMPERATURE_STEP] +
                                           0.9 * states[temperature],
                                           self.c_off + 0.3 * states[temperature] +
                                           0.7 * states[temperature - TEMPERATURE_STEP])
                    elif temperature == 24.5:
                        states_final_values[temperature] = min(self.c_on + 0.7 * states[temperature + TEMPERATURE_STEP] +
                                           0.2 * states[temperature] +
                                           0.1 * states[temperature - TEMPERATURE_STEP],
                                           self.c_off + 0.7 * states[temperature - TEMPERATURE_STEP] +
                                           0.1 * states[temperature + TEMPERATURE_STEP] +
                                           0.2 * states[temperature])
                    else:
                        states_final_values[temperature] = min(self.c_on + 0.5 * states[temperature + TEMPERATURE_STEP] +
                                           0.2 * states[temperature + 2 * TEMPERATURE_STEP] +
                                           0.2 * states[temperature] +
                                           0.1 * states[temperature - TEMPERATURE_STEP],
                                           self.c_off + 0.7 * states[temperature - TEMPERATURE_STEP] +
                                           0.1 * states[temperature + TEMPERATURE_STEP] +
                                           0.2 * states[temperature])
                valids = 0
                for j in states_final_values.keys():
                    if abs(states_final_values[j] - states[j]) < self.tolerance:
                        valids += 1
                    else:
                        states[j] = states_final_values[j]
                if valids == len(states_final_values):
                    return


mk = Markov()
#print(states)
#import pprint
#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(states)