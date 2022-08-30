'''
Jason Ketterer

'''

from sklearn import datasets
from sklearn import decomposition
from sklearn.cluster import KMeans

import pandas as pd
import numpy as np

# load the Handwritten Digits Data Set
digits = datasets.load_digits()

# store the features in a Pandas dataframe
X = pd.DataFrame(digits.data)

# perform Principal Component Analysis on the data
pca = decomposition.PCA(n_components=2)
pca.fit(X)
X = pca.transform(X)

# build the machine learning model and run the algorithm on the dataset
model = KMeans(n_clusters=10)
model.fit(X)

'''
# turn result into a dictionary where the keys are the data points and the values are the cluster labels
'''
X.resize(len(X),2)
datapoints = list(map(tuple, X))

for idx, dp in enumerate(datapoints):
    # results[dp] = digits.target[idx]
    print(dp,digits.target[idx],sep='\t')

'''
# send results to stdout so that reducer can access them via stdin
for dp, label in results.items():
    print(dp[0],dp[1],label,sep=",")
'''
