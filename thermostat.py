import random
from constants import *


class Thermostat():
    def __init__(self, temperature):
        self.temperature = temperature
        self.desired_temperature = DESIRED_TEMP
        self.state = "off"

    def heat(self):
        self.state = "on"
        activity = random.randint(0, 9)
        if self.temperature == MIN_TEMP:
            if activity in [0, 1, 2]:
                self.temperature = self.temperature
            elif activity in [3, 4, 5, 6, 7]:
                self.temperature += TEMPERATURE_STEP
            else:
                self.temperature += 2*TEMPERATURE_STEP
        elif self.temperature == MAX_TEMP:
            if activity == 0:
                self.temperature -= TEMPERATURE_STEP
            else:
                self.temperature = self.temperature
        elif self.temperature == MAX_TEMP-TEMPERATURE_STEP:
            if activity == 0:
                self.temperature -= TEMPERATURE_STEP
            elif activity in [1, 2, 3, 4, 5, 6]:
                self.temperature = self.temperature
            else:
                self.temperature += TEMPERATURE_STEP
        else:
            if activity == 0:
                self.temperature -= TEMPERATURE_STEP
            elif activity in [1, 2]:
                self.temperature = self.temperature
            elif activity in [3, 4]:
                self.temperature += 2*TEMPERATURE_STEP
            else:
                self.temperature += TEMPERATURE_STEP

    def cool(self):
        self.state = "off"
        activity = random.randint(0, 9)
        if self.temperature == MIN_TEMP:
            if activity == 0:
                self.temperature += TEMPERATURE_STEP
            else:
                self.temperature = self.temperature
        elif self.temperature == MAX_TEMP:
            if activity in [0, 1, 2]:
                self.temperature = self.temperature
            else:
                self.temperature -= TEMPERATURE_STEP
        else:
            if activity == 0:
                self.temperature += TEMPERATURE_STEP
            elif activity in [1, 2]:
                self.temperature = self.temperature
            else:
                self.temperature -= TEMPERATURE_STEP
