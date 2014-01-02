import numpy as np
import pylab as pl
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.datasets import load_iris
from sklearn import datasets, svm
from sklearn.feature_selection import SelectPercentile, f_classif

###############################################################################
# import some data to play with

# The iris dataset
iris = datasets.load_iris()

x = iris.data
y = iris.target

clf = ExtraTreesClassifier()
X_new = clf.fit(x, y).feature_importances_  #.transform(x)
X_new_two = clf.fit(x, y).transform(x)
print(X_new)
print(X_new_two)