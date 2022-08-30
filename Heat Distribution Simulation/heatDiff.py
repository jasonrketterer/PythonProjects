# Jason Ketterer
#
# Simulate the heat distribution in 2-D
# Uses numpy, matplotlib, and multiprocessing

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import time
import math

def getIntInput(prompt):
    """Helper function to display prompt and get and validate an integer input from user"""
    i = 0
    while True:
        try:
            i = int(input(prompt))
            break
        except ValueError:
            print("Input not an integer.")
            continue
    return i

def run_simulation(temp, T):
    '''Simulates Jacobi method for heat distribution in 2-d material'''
    max_iterations = 3000
    iterations = 0
    while iterations < max_iterations:
        prev_temp = np.copy(temp)
        for i in range(1, T+1):
            for j in range(1, T+1):
                temp[i,j] = 0.25 * (prev_temp[i-1,j] + prev_temp[i+1,j] + prev_temp[i,j-1] + prev_temp[i,j+1])

        if (temp == prev_temp).all(): # convergence
            break
        iterations += 1

if __name__ == "__main__":
    T = getIntInput("Enter starting temperature: ")

    # initialize the material
    cur_temp = np.zeros((T + 2, T + 2))
    cur_temp[:, 0] = T

    # run and time the simulation
    start_time = time.time()
    run_simulation(cur_temp, T)
    run_time = time.time() - start_time
    print(f"{run_time:.3f} seconds")

   # plot the heatmap
    colors = ('darkblue', 'blue', 'aqua', 'lawngreen', 'yellow', 'orange', 'red', 'darkred')
    cmap = ListedColormap(colors)

    for x in range(0, T+2):
        for y in range(0, T+2):
            t = math.floor( np.interp(cur_temp[(T+1-y),x], [0,T], [0,7]) )
            plt.scatter(x, y, c=cmap([t]))
    plt.show()