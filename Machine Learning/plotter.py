'''
Jason Ketterer

'''

import matplotlib.pyplot as plt
import numpy as np

f = open("results.csv", 'r')

colormap = np.array(['red', 'blue', 'yellow', 'black', 'green', 'cyan', 'magenta', 'gray', 'orange', 'purple'])

line = f.readline()
while line:
    datapoint1, datapoint2, label = line.split(',')
    dp1 = float(datapoint1)
    dp2 = float(datapoint2)
    l = int(label)
    plt.scatter(dp1, dp2, c=colormap[l], s=40)
    line = f.readline()

plt.title('K Means Classification of the digits dataset')
plt.show()