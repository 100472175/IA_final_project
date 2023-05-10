import numpy as np

from thermostat import Thermostat
from constants import *

"""temperatures_list = []
state_value = {}
i = MIN_TEMP
while i < MAX_TEMP + TEMPERATURE_STEP:
    temperatures_list.append(float(i))
    state_value[float(i)] = 0
    i += TEMPERATURE_STEP

initial_state = MIN_TEMP
objective = DESIRED_TEMP
"""
iterated_states = []
global actions_taken
actions_taken = []


class MarkovModel:
    def __init__(self):
        self.c_on = 10
        self.c_off = 5
        self.user_temperature = 22
        self.heater = True
        self.cooler = False
        self.tolerance = 0.001
        self.states = {}
        for i in np.arange(MIN_TEMP, MAX_TEMP+TEMPERATURE_STEP, TEMPERATURE_STEP):
            self.states[i] = 0


    def markov_model(self, temperature):
        # Actions is ON and OFF
        actions = [0, 0]
        if temperature == 16:
            actions[0] = (self.c_on + 0.3 * self.value(temperature) +
                          0.5 * self.value(temperature + 0.5) +
                          0.2 * self.value(temperature + 1))
            actions[1] = (self.c_off + 0.1 * self.value(temperature + 0.5) +
                          0.9 * self.value(temperature))
        elif temperature == 25:
            actions[0] = (self.c_on + 0.1 * self.value(temperature - 0.5) +
                          0.9 * self.value(temperature))
            actions[1] = (self.c_off + 0.3 * self.value(temperature) +
                          0.7 * self.value(temperature - 0.5))
        elif temperature == 24.5:
            actions[0] = (self.c_on + 0.7 * self.value(temperature + 0.5) +
                          0.2 * self.value(temperature) +
                          0.1 * self.value(temperature - 0.5))
            actions[1] = (self.c_off + 0.7 * self.value(temperature - 0.5)
                          + 0.1 * self.value(temperature + 0.5)
                          + 0.2 * self.value(temperature))
        else:
            actions[0] = (self.c_on + 0.5 * self.value(temperature + 0.5) +
                          0.2 * self.value(temperature + 1) +
                          0.2 * self.value(temperature) +
                          0.1 * self.value(temperature - 0.5))
            actions[1] = (self.c_off + 0.7 * self.value(temperature - 0.5) +
                          0.1 * self.value(temperature + 0.5) +
                          0.2 * self.value(temperature))
        if min(actions) == actions[0]:
            actions_taken.append("heating")
        else:
            actions_taken.append("cooling")

    def value(self, element):
        states = {}
        for i in np.arange(MIN_TEMP, MAX_TEMP+TEMPERATURE_STEP, TEMPERATURE_STEP):
            states[i] = 0
        while True:
            for element in states:
                if element != self.user_temperature:
                    if element == 16:
                        V_next = min(self.c_on + 0.3 * states[element] +
                                     0.5 * states[element + 0.5] +
                                     0.2 * states[element + 1],
                                     self.c_off + 0.1 * states[element + 0.5]
                                     + 0.9 * states[element])
                    elif element == 25:
                        V_next = min(self.c_on + 0.1 * states[element - 0.5] +
                                     0.9 * states[element],
                                     self.c_off + 0.3 * states[element] +
                                     0.7 * states[element - 0.5])
                    elif element == 24.5:
                        V_next = min(self.c_on + 0.7 * states[element + 0.5] +
                                     0.2 * states[element] +
                                     0.1 * states[element - 0.5],
                                     self.c_off + 0.7 * states[element - 0.5] +
                                     0.1 * states[element + 0.5] +
                                     0.2 * states[element])
                    else:
                        V_next = min(self.c_on + 0.5 * states[element + 0.5] +
                                     0.2 * states[element + 1] +
                                     0.2 * states[element] +
                                     0.1 * states[element - 0.5],
                                     self.c_off + 0.7 * states[element - 0.5] +
                                     0.1 * states[element + 0.5] +
                                     0.2 * states[element])
                else:
                    V_next = 0

                self.states[element] = V_next
            if abs(self.states[element] - states[element]) < self.tolerance:
                return self.states[element]
            else:
                for element in states:
                    states[element] = self.states[element]

for i in range(1000):
    my = MarkovModel()
    my.markov_model(22)
    print(my.states)


