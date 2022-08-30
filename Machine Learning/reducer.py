'''
Jason Ketterer

'''

from operator import itemgetter
import sys
from statistics import mode
'''
f = open("results.csv", 'w')

for line in sys.stdin:
    line = line.strip()
    datapoint1, datapoint2, label = line.split(',')
    # print(datapoint1, datapoint2, label)
    print(datapoint1 + ',' + datapoint2 + ',' + label, file=f)

f.close()
'''
# collate results from mapper(s)
results = dict()
for line in sys.stdin:
    line = line.strip()
    dp, label = line.split('\t')
    # print(dp,label)
    l = int(label)
    if dp not in results.keys():
        results[dp] = []
    results[dp].append(l)

# determine most frequent label and send results to a csv file
f = open("results.csv", 'w')

for k,v in results.items():
    freq_label = mode(results[k])
    datapoints = k.strip('()')
    datapoint1, datapoint2 = datapoints.split(',')
    # print(datapoint1, datapoint2, freq_label)
    print(datapoint1 + ',' + datapoint2 + ',' + str(freq_label), file=f)

f.close()