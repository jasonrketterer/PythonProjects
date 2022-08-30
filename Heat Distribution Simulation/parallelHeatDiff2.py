# Jason Ketterer
# FSUID; jrk08j

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import time
import math
import multiprocessing as mp

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

def jacobi(arr, start, end, T, step, rem):
    if end > T:
        end = end - rem
    new_arr = np.zeros((T+1,end-start+2))
    for r in range(1, T+1):
        for c in range(start, end+1):
            new_arr[r][c%step] = 0.25 * (arr[r - 1, c] + arr[r + 1, c] + arr[r, c-1] + arr[r, c+1])
    return start, end, new_arr

def run_simulation(temp, T):
    max_iterations = 3000
    iterations = 0
    cpus = mp.cpu_count()
    step, rem = divmod(T, cpus)

    if step == 0:
        step = 1

    # create pool of Processes
    pool = mp.Pool(cpus)

    while iterations < max_iterations:
        prev_temp = np.copy(temp)
        # process calculations using async multiprocessing
        results = [pool.apply_async(jacobi, args=(prev_temp, c, c+step, T, step, rem)) for c in range(1, T+rem+1, step)]
        output = [p.get() for p in results]

        # copy results back to master grid(cur_temp)
        for start, stop, arr in output:
            for r in range(1, T+1):
                for c in range(start, stop+1):
                    temp[r][c] = res[r][c%step]

        if (temp == prev_temp).all():  # convergence
            pool.close()
            pool.join()
            break
        iterations += 1
    pool.close()
    pool.join()


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

    for x in range(0, T + 2):
        for y in range(0, T + 2):
            t = math.floor(np.interp(cur_temp[(T + 1 - y), x], [0, T], [0, 7]))
            plt.scatter(x, y, c=cmap([t]))
    plt.show()