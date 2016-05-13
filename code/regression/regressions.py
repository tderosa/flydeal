import csv
import numpy as np
import scipy
from matplotlib import pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import BernoulliNB
from sklearn import cross_validation
from sklearn.svm import SVC




data = np.loadtxt(open('logreg3.csv', 'r'), delimiter=',', skiprows=1)

X = data[:, :2]
y = data[:, 4:]

train_index = int(len(data) * 0.7)
X_train = data[:train_index, :2]
y_train = data[:train_index, 4:]
X_test = data[train_index:, :2]
y_test = data[train_index:, 4:]

# folds= 4
# kf = cross_validation.KFold(len(X), n_folds=folds)
# for train, test in kf:
# 	X_train, X_test, y_train, y_test = X[train], X[test], np.squeeze(y[train]), np.squeeze(y[test])


	# Logistic Regression

	# logreg = LogisticRegression()
	# logreg.fit(X_train, y_train)
	# print(logreg.score(X_test, y_test))


	# Naive Bayes

	# nb = BernoulliNB()
	# nb.fit(X_train, y_train)
	# print(nb.score(X_test, y_test))


	# SVM
	# svm = SVC()
	# svm.fit(X_train, y_train)
	# print(svm.score(X_test, y_test))





# Logistic Regression

logreg = LogisticRegression()
logreg.fit(X_train, y_train)

# print(logreg.score(X_test, y_test))


def plot_decision_boundary(pred_func):
  # Set min and max values and give it some padding
  x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
  y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
  h = 0.01
  # Generate a grid of points with distance h between them
  xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
  # Predict the function value for the whole gid
  Z = pred_func(np.c_[xx.ravel(), yy.ravel()])
  Z = Z.reshape(xx.shape)
  # Plot the contour and training examples
  # plt.contourf(xx, yy, Z, cmap=plt.cm.bone)
  plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.winter, s=50)


plot_decision_boundary(logreg.predict)
plt.title("Error Tickets")
plt.xlabel('duration')
plt.ylabel('distance')
plt.legend(['regular ticket'])
plt.show()

