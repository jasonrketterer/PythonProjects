'''
Jason Ketterer

'''

import matplotlib.pyplot as plt
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

# store the responses(answers) in a separate dataframe
y = pd.DataFrame(digits.target)
y.columns = ['Targets']

# build the machine learning model and run the algorithm on the dataset
model = KMeans(n_clusters=10)
model.fit(X)

# plot the results as two subplots
plt.figure(figsize=(14, 7))
colormap = np.array(['red', 'blue', 'yellow', 'black', 'green', 'cyan', 'magenta', 'gray', 'orange', 'purple'])

plt.subplot(1, 2, 1)
plt.scatter(X[:, 0], X[:, 1], c=colormap[y.Targets], s=40)
plt.title('Real Classification')

plt.subplot(1, 2, 2)
plt.scatter(X[:, 0], X[:, 1], c=colormap[model.labels_], s=40)
plt.title('K Means Classification')

plt.show()






