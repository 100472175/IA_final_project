"""
# Artificial Intelligence - Final Project Assignment
# Coded by Eduardo Alarcón and Alfonso Pineda
Module to generate the graph of the states and the optimal policy
"""

import time
import matplotlib.pyplot as plt
from markov import Markov


def simple_graph():
    """Generates the graph of the states"""
    markov = Markov("config.ini")
    x_axis = markov.states_values.keys()
    y_def = markov.states_values.values()
    plt.title("Cost of the states")
    plt.plot(x_axis, y_def, color='blue', label="Elaborated costs")
    plt.legend()
    plt.show()

def optimal_policy():
    """Generates the graph of the optimal policy"""
    markov = Markov("config.ini")
    x_axis = markov.states_values.keys()
    markov.solve()
    y_axis = []
    for i in x_axis:
        y_axis.append(markov.actions_to_take[i][0])
    plt.title("Optimal Policy")
    plt.plot(x_axis, y_axis, color='red', label="Optimal Policy")
    plt.legend()
    plt.show()


def big_graph():
    """Generates the graph of the states with different heating and cooling costs"""
    markov = Markov("config.ini")
    x_axis = markov.states_values.keys()
    y_def = markov.states_values.values()
    plt.title("Cost of the states")
    plt.plot(x_axis, y_def, color='blue', label="Elaborated costs")
    plt.legend()
    plt.show()

    markov.c_on = 1
    markov.c_off = 1
    markov.solve()
    y_time = markov.states_values.values()
    plt.plot(x_axis, y_time, color='red', label="Time")

    markov.c_on = 40
    markov.c_off = 5
    markov.solve()
    y_eff = markov.states_values.values()
    plt.plot(x_axis, y_eff, color='green', label="Efficiency")

    markov.c_on = 10
    markov.c_off = 0
    markov.solve()
    y_off_0 = markov.states_values.values()
    plt.plot(x_axis, y_off_0, color='black', label="Cost cooling 0")
    markov.solve()

    plt.legend()
    plt.show()


a = time.time()
markov_dp = Markov("config.ini")
markov_dp.solve()
print(markov_dp)
print(time.time() - a)
simple_graph()
optimal_policy()
big_graph()
