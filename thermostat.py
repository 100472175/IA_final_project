import random
from random import randint


class Thermostat():
    def __init__(self, temperature):
        self.temperature = temperature
        self.state = "off"

    def heat(self):
        self.state = "heat"
        activity = get_number()
        if self.temperature == 16:
            if activity in [0, 1, 2]:
                self.temperature = self.temperature
            elif activity in [3, 4, 5, 6, 7]:
                self.temperature += 0.5
            else:
                self.temperature += 1
        elif self.temperature == 25:
            if activity == 0:
                self.temperature -= 0.5
            else:
                self.temperature = self.temperature
        elif self.temperature == 24.5:
            if activity == 0:
                self.temperature -= 0.5
            elif activity in [1, 2, 3, 4, 5, 6]:
                self.temperature = self.temperature
            else:
                self.temperature += 0.5
        else:
            if activity == 0:
                self.temperature -= 0.5
            elif activity in [1, 2]:
                self.temperature = self.temperature
            elif activity in [3, 4]:
                self.temperature += 1
            else:
                self.temperature += 0.5

    def cool(self):
        self.state = "resting"
        activity = get_number()
        if self.temperature == 16:
            if activity == 0:
                self.temperature += 0.5
            else:
                self.temperature = self.temperature
        elif self.temperature == 25:
            if activity in [0, 1, 2]:
                self.temperature = self.temperature
            else:
                self.temperature -= 0.5
        else:
            if activity == 0:
                self.temperature += 0.5
            elif activity in [1, 2]:
                self.temperature = self.temperature
            else:
                self.temperature -= 0.5



def get_number():
    return random.randint(0, 9)
