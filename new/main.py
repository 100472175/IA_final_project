from constants import *
import numpy as np

class Markov:
    def __init__(self, desired_temp=DESIRED_TEMP):
        self.c_on = 10
        self.c_off = 5
        self.tolerance = 0.000001
        self.objective = desired_temp
        self.define_states()

    def define_states(self):
        self.states_final_values = {}
        self.states = {}
        for i in np.arange(MIN_TEMP, MAX_TEMP + TEMPERATURE_STEP, TEMPERATURE_STEP):
            self.states[i] = 0
            self.states_final_values[i] = 0
            

    def solve(self):
        for i in np.arange(MIN_TEMP, MAX_TEMP+TEMPERATURE_STEP, TEMPERATURE_STEP):
            self.bellman(i)
        # Meter aqui los estados, y el otro diccionario, para luego hacer un __str__


    def bellman(self, temperature):
        # Get the values of all the states
        self.iterations()

        # Actions is ON and OFF
        actions = [0, 0]
        if temperature == self.objective:
            return "Cooling", 0
        elif temperature == 16:
            actions[0] = (self.c_on + 0.3 * self.states_final_values[temperature] +
                          0.5 * self.states_final_values[temperature + TEMPERATURE_STEP] +
                          0.2 * self.states_final_values[temperature + 2 * TEMPERATURE_STEP])
            actions[1] = (self.c_off + 0.1 * self.states_final_values[temperature + TEMPERATURE_STEP] +
                          0.9 * self.states_final_values[temperature])
        elif temperature == 25:
            actions[0] = (self.c_on + 0.1 * self.states_final_values[temperature - TEMPERATURE_STEP] +
                          0.9 * self.states_final_values[temperature])
            actions[1] = (self.c_off + 0.3 * self.states_final_values[temperature] +
                          0.7 * self.states_final_values[temperature - TEMPERATURE_STEP])
        elif temperature == 24.5:
            actions[0] = (self.c_on + 0.7 * self.states_final_values[temperature + TEMPERATURE_STEP] +
                          0.2 * self.states_final_values[temperature] +
                          0.1 * self.states_final_values[temperature - TEMPERATURE_STEP])
            actions[1] = (self.c_off + 0.7 * self.states_final_values[temperature - TEMPERATURE_STEP]
                          + 0.1 * self.states_final_values[temperature + TEMPERATURE_STEP]
                          + 0.2 * self.states_final_values[temperature])
        else:
            actions[0] = (self.c_on + 0.5 * self.states_final_values[temperature + TEMPERATURE_STEP] +
                          0.2 * self.states_final_values[temperature + 2 * TEMPERATURE_STEP] +
                          0.2 * self.states_final_values[temperature] +
                          0.1 * self.states_final_values[temperature - TEMPERATURE_STEP])
            actions[1] = (self.c_off + 0.7 * self.states_final_values[temperature - TEMPERATURE_STEP] +
                          0.1 * self.states_final_values[temperature + TEMPERATURE_STEP] +
                          0.2 * self.states_final_values[temperature])
        if actions[0] < actions[1]:
            return "Heating", actions[0]
        else:
            return "Cooling", actions[1]

    def iterations(self):
        while True:
            for temperature in self.states_final_values:
                if temperature == self.objective:
                    self.states[temperature] = 0
                    continue
                else:
                    working_temp = 0
                    if temperature == 16:
                        self.states_final_values[temperature] = min(self.c_on + 0.3 * self.states[temperature] +
                                           0.5 * self.states[temperature + TEMPERATURE_STEP] +
                                           0.2 * self.states[temperature + 2 * TEMPERATURE_STEP],
                                           self.c_off + 0.1 * self.states[temperature + TEMPERATURE_STEP] +
                                           0.9 * self.states[temperature])
                    elif temperature == 25:
                        self.states_final_values[temperature] = min(self.c_on + 0.1 * self.states[temperature - TEMPERATURE_STEP] +
                                           0.9 * self.states[temperature],
                                           self.c_off + 0.3 * self.states[temperature] +
                                           0.7 * self.states[temperature - TEMPERATURE_STEP])
                    elif temperature == 24.5:
                        self.states_final_values[temperature] = min(self.c_on + 0.7 * self.states[temperature + TEMPERATURE_STEP] +
                                           0.2 * self.states[temperature] +
                                           0.1 * self.states[temperature - TEMPERATURE_STEP],
                                           self.c_off + 0.7 * self.states[temperature - TEMPERATURE_STEP] +
                                           0.1 * self.states[temperature + TEMPERATURE_STEP] +
                                           0.2 * self.states[temperature])
                    else:
                        self.states_final_values[temperature] = min(self.c_on + 0.5 * self.states[temperature + TEMPERATURE_STEP] +
                                           0.2 * self.states[temperature + 2 * TEMPERATURE_STEP] +
                                           0.2 * self.states[temperature] +
                                           0.1 * self.states[temperature - TEMPERATURE_STEP],
                                           self.c_off + 0.7 * self.states[temperature - TEMPERATURE_STEP] +
                                           0.1 * self.states[temperature + TEMPERATURE_STEP] +
                                           0.2 * self.states[temperature])
                valids = 0
                for j in self.states_final_values.keys():
                    if abs(self.states_final_values[j] - self.states[j]) < self.tolerance:
                        valids += 1
                    else:
                        self.states[j] = self.states_final_values[j]
                if valids == len(self.states_final_values):
                    return


# Aquí va el parsing de los argumentos, para hacer el init de Markov

mk = Markov()
#print(states)
import pprint
pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(states)
pp.pprint(mk.states_final_values)

