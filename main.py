import numpy as np

from thermostat import Thermostat
from constants import *

temperatures_list = []
state_cost = {}
i = MIN_TEMP
while i < MAX_TEMP + TEMPERATURE_STEP:
    temperatures_list.append(float(i))
    state_cost[float(i)] = 0
    i += TEMPERATURE_STEP

temperature = input("Enter the actual temperature: ")
thermostat = Thermostat(int(temperature))
temperature = int(temperature)
initial_state = MIN_TEMP
objective = DESIRED_TEMP

iterated_states = []
actions_taken = []


def bellmanEquation(state):
    iterated_states.append([])
    min_list = []
    if state == MIN_TEMP:
        pass
    elif state == MAX_TEMP:
        pass
    elif state == MAX_TEMP - TEMPERATURE_STEP:
        pass
    else:
        min_list.append(1 + TEMPERATURE_STEP * state_cost[state + TEMPERATURE_STEP] +
                        0.2 * state_cost[state + 2 * TEMPERATURE_STEP] +
                        0.2 * state_cost[state] +
                        0.1 * state_cost[state - TEMPERATURE_STEP])

        min_list.append(0 + 0.7 * state_cost[state - TEMPERATURE_STEP] +
                        0.1 * state_cost[state + TEMPERATURE_STEP] +
                        0.2 * state_cost[state])
        min_choice = min(min_list)
        if min_choice == min_list[0]:
            actions_taken.append(("heat", 0))

        else:
            actions_taken.append(("off", 1))
        state_cost[state] = min_choice

    return actions_taken, state_cost

def bellmanEquation_base(state):
    return bellmanEquation(state)

if temperature > objective:
    print("The optimal action is to not heat the room")
    exit()

for i in np.arange(temperature, objective, TEMPERATURE_STEP):
    actions, state_cost = bellmanEquation_base(i)
    print(actions)
print(actions_taken)
