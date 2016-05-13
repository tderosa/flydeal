import csv
import numpy as np
import scipy
from sklearn.linear_model import LogisticRegression, LinearRegression, ElasticNet
from sklearn import cross_validation
import matplotlib.pyplot as plt



data = np.loadtxt(open('../../data/outputs/regressions.csv', 'r'), delimiter=',', skiprows=1)

# NORMALIZATION
data = data/data.max(axis=0)


# SHUFFLE THE DATA
# np.random.shuffle(data)

# cross validation

# X = data[:1000, 2:3]
# y = data[:1000, 3:]

# final_score = []
# final_coef = np.array([0.,0.,0.])
# final_intercept = []


# K FOLD CROSS VALIDATION

# folds= 10
# kf = cross_validation.KFold(len(X), n_folds=folds)
# for train, test in kf:
# 	X_train, X_test, y_train, y_test = X[train], X[test], y[train], y[test]


train_index = int(len(data) * 0.7)
X_train = data[:train_index, :3]
y_train = data[:train_index, 3:]
X_test = data[train_index:, :3]
y_test = data[train_index:, 3:]

data_sm = data[train_index:, :]

# X_train, X_test, y_train, y_test = cross_validation.train_test_split(data[:,:3], data[:,3:], test_size=0.13, random_state=40)


# print (X_train, y_train)

	# results = np.array(results)
	# plt.plot(results[:,0], results[:,1], color='black')
	# plt.ylabel('price')
	# plt.xlabel('nth week of the year')
	# plt.xticks()
	# plt.yticks()
	# plt.show()



# FIT LINEAR REGRESSION MODEL USING ELASTICNET
print('Fitting linear regression model...')

lin_reg = ElasticNet(alpha=0.00001, l1_ratio=0.2)
lin_reg.fit(X_train, y_train)

# print ('score: ' + str(lin_reg.score(X_test, y_test)))
# print(lin_reg.coef_)
# print(lin_reg.intercept_)
# final_score.append(lin_reg.score(X_test, y_test))
# final_coef += lin_reg.coef_
# final_intercept.append(lin_reg.intercept_)

# print ('final score: ' + str(np.mean(final_score)))

# mean_coef = final_coef/10
# mean_intercept = np.mean(final_intercept)


# lin_reg.coef_ = mean_coef
# lin_reg.intercept_ = mean_intercept


# LABEL NEW ERROR TICKET LABELS ON EXISTING DATA

y_new = lin_reg.predict(X_test)

# print(lin_reg.coef_)
print('final score for linear Elastic Net: ' + str(lin_reg.score(X_test, y_test)))


# DEFINITION FOR ERROR TICKET

rate = 0.7
lower = y_new * (1-rate)
result = np.expand_dims((np.squeeze(y_test) - lower) < 0, axis=1)


# results = np.array(results)
# plt.scatter(X_test, y_test, color='black', s=1)
# plt.plot(X_test, y_new, color='blue')
# plt.ylabel('price (USD)')
# plt.xlabel('week score')
# plt.xticks()
# plt.yticks()
# plt.show()


# print(result)

# result = np.subtract(y_test, lower)
# print(result.shape)

# WRITE OUT NEW LABELED DATASET

new_result = np.concatenate((data_sm, result), axis=1)
# print(new_result)

with open('../../data/outputs/logreg.csv', 'w') as f:
	writer = csv.writer(f)
	writer.writerow(['duration', 'distance', 'week score', 'price', 'error ticket'])
	writer.writerows(new_result)


# y = y[:20000]

# print(y_sm - y)


# plt.scatter(new_result[0], new_result[1], color='black')
# plt.plot(new_result[0], lin_reg.predict(new_result[0]), color='blue', linewidth=1)

# plt.xticks(())
# plt.yticks(())

# plt.ylabel('price')
# plt.xlabel('week_score')

# plt.show()
# print(lin_reg.coef_)
# print(lin_reg.intercept_)
# print('prediction: ' + str(lin_reg.predict([1000, 2800, 100])))


# print(len(data))



# PLOT price vs duration with Linear regression line
X_train = data[:train_index, :1]
y_train = data[:train_index, 3:]
X_test = data[train_index:, :1]
y_test = data[train_index:, 3:]
lin_reg.fit(X_train, y_train)
plt.scatter(X_test, y_test, color='black', s=1)
plt.plot(X_test, lin_reg.predict(X_test), color='blue')
plt.ylabel('price (USD)')
plt.xlabel('duration')
plt.xticks()
plt.yticks()
plt.show()

# PLOT price vs distance with Linear regression line
X_train = data[:train_index, 1:2]
y_train = data[:train_index, 3:]
X_test = data[train_index:, 1:2]
y_test = data[train_index:, 3:]
lin_reg.fit(X_train, y_train)
plt.scatter(X_test, y_test, color='black', s=1)
plt.plot(X_test, lin_reg.predict(X_test), color='blue')
plt.ylabel('price (USD)')
plt.xlabel('distance')
plt.xticks()
plt.yticks()
plt.show()