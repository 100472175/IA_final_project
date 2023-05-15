from constants import *
import numpy as np
import configparser
import os
import matplotlib.pyplot as plt
from markov import Markov




# Aquí va el parsing de los argumentos, para hacer el init de Markov

mk = Markov("new/config.ini")
mk.solve()
print(mk)

x = mk.states_values.keys()
y_def = mk.states_values.values()
plt.title("Cost of the states")
plt.plot(x, y_def, color='blue', label="Default")

mk = Markov("new/config.ini")
mk.c_on = 1
mk.c_off = 1
mk.solve()
y_time = mk.states_values.values()
plt.plot(x, y_time, color='red', label="Time")

mk = Markov("new/config.ini")
mk.c_on = 40
mk.c_off = 5
mk.solve()
y_eff = mk.states_values.values()
plt.plot(x, y_eff, color='green', label="Efficiency")

mk = Markov("new/config.ini")
mk.c_on = 10
mk.c_off = 0
mk.solve()
y_off_0 = mk.states_values.values()
plt.plot(x, y_off_0, color='black', label="Cost cooling 0")
mk.solve()

plt.legend()
plt.show()
