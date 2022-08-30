import random
import multiprocessing as mp
from time import time

# Prepare data

data = [[random.randint(0, 9) for i in range(10)] for j in range(10)]
print("Generated Data:")
print(data)


# Solution Without Paralleization

# rangecount, one row at a time
def rangeCount(row, minimum, maximum):
    """Returns how many numbers lie within `maximum` and `minimum` in a given `row`"""
    count = 0
    for n in row:
        if minimum <= n <= maximum:
            count = count + 1
    return count


results = []
for row in data:
    results.append(rangeCount(row, minimum=3, maximum=8))

print("Without parallelization:")
print(results)

# With pool.apply, we can use the same function
# Initialize multiprocessing Pool
pool = mp.Pool(mp.cpu_count())

# apply the function
results = [pool.apply(rangeCount, args=(row, 3, 8)) for row in data]

# Don't forget to close
pool.close()

print("With pool.apply")
print(results)


# With pool.map
# Redefine the function, with only 1 mandatory argument.
def rangeCount2(row, minimum=3, maximum=8):
    count = 0
    for n in row:
        if minimum <= n <= maximum:
            count = count + 1
    return count


# Initialize the pool
pool = mp.Pool(mp.cpu_count())

# Use the map on the function
results = pool.map(rangeCount2, [row for row in data])

# Close
pool.close()

print("With pool.map")
print(results)


# With pool.apply_async
# Redefine, to accept `i`, the iteration number
# We will need this because processes may complete out of order
def rangeCount3(i, row, minimum, maximum):
    count = 0
    for n in row:
        if minimum <= n <= maximum:
            count = count + 1
    return (i, count)  # Return tuple with iteration or row number, and count


# Using a callback function is a way to get around using a queue of ApplyResult objects
# The callback function instead gets the value from the returned result and adds it
# to a global list (in this case) of our own making
def collect_result(result):
    global results
    results.append(result)


# create the process pool
pool = mp.Pool(mp.cpu_count())

results = []

# Use loop to parallelize
i = 0
for row in data:
    pool.apply_async(rangeCount3, args=(i, row, 3, 8), callback=collect_result)
    i += 1

# Close Pool and let all the processes complete
pool.close()
pool.join()  # postpones the execution of next line of code until all processes in the queue are done.

# Sort results
# We will need this since processes might have completed out of order
results.sort(key=lambda x: x[0])
results_final = [r for i, r in results]

print("With pool.applyasync")
print(results_final)