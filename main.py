from thermostat import Thermostat
from constants import *

temperatures_list = []
i = MIN_TEMP
while i < MAX_TEMP+TEMPERATURE_STEP:
    temperatures_list.append(float(i))
    i += TEMPERATURE_STEP



temperature = input("Enter the actual temperature: ")
thermostat = Thermostat(temperature)
initial_state = MIN_TEMP
objective = DESIRED_TEMP




def BellmanEquation():
    pass