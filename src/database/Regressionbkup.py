from sklearn.linear_model import Ridge, LinearRegression, Lasso, ElasticNet, SGDRegressor, BayesianRidge
import numpy as np
import sqlite3
import time
import numpy as np
from multiprocessing import Pool
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.svm import LinearSVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.model_selection import KFold,  cross_val_score
from sklearn.neighbors import KNeighborsClassifier
import math
import random
import operator
import pprint as pp


conn = sqlite3.connect('../../data/data.db')
c = conn.cursor()
startTime = time.time()

scores = []
setData = []
baseline = []
# c.execute('''SELECT st.lang
#              FROM subreddits AS st
#              GROUP BY 1
#              ''')
#
X_int = LabelEncoder()
labels = []


# Aggregate bands:
# Score [47, 625, 4017, 5677, 8717]
# num_comments [21, 148, 806, 3074, 11766]
# Score must always be first
variables = ['ft.agg_score']
predictors = ['st.subscribers', 'ft.optimal_time', 'ft.is_self', 'ft.over_18', 'ft.media_attached', 'st.agg_accounts_active',
                    'ft.weekday', 'ft.hour', 'ft.minute', 'st.submission_type', 'st.over_18', 'st.advertiser_category', 'st.lang', 'st.average_score']

variables = variables + predictors


# under sampling of data
for cat in range(0, 6):
    c.execute('''SELECT '''+ ','.join(variables) +'''
                 FROM posts as ft JOIN subreddits AS st ON st.subreddit_id == ft.subreddit_id
                 WHERE agg_score == ''' + str(cat) + '''
                 LIMIT 15000
                 ''')
    for rows in c.fetchall():
         temp = []
         #num = int(any(char.isdigit() for char in rows[len(variables)-1]))
         for x in range(1, len(variables)):
             temp.append(rows[x])
             #temp.append(num)
         setData.append(temp)
         scores.append(rows[0])
         baseline.append(rows[-1])

# c.execute('''SELECT '''+ ','.join(variables) +'''
#              FROM posts as ft JOIN subreddits AS st ON st.subreddit_id == ft.subreddit_id
#              WHERE ft.subreddit IN (SELECT subreddit
#                                     FROM posts
#                                     GROUP BY 1
#                                     HAVING COUNT(subreddit) > 10)
#              LIMIT 800000
#              ''')
#
#
# for rows in c.fetchall():
#      temp = []
#      #num = int(any(char.isdigit() for char in rows[len(variables)-1]))
#      for x in range(1, len(variables)):
#          temp.append(rows[x])
#          #temp.append(num)
#      setData.append(temp)
#      scores.append(rows[0])
#      baseline.append(rows[-1])



temp = list(zip(setData, scores, baseline))
random.seed(14)
random.shuffle(temp)
setData, scores, baseline = zip(*temp)

setData = list(setData)

labels = np.array(setData)

conn.rollback()
c.close()
conn.close()

print('amount of scores : {}'.format(len(scores)))
setData = pd.DataFrame(setData, columns = variables[1:])
start = time.time()
print("going in")
setData = pd.get_dummies(setData, sparse = True)
# print(setData)

print('Dummies took {}'.format(time.time() - start))
# with open('test.csv', 'w') as w:
#     setData.head(5).to_csv('test.csv', sep='\t', encoding='utf-8')
#




# X_int = LabelEncoder().fit_transform(labels.ravel()).reshape(*labels.shape)
# setData = OneHotEncoder().fit_transform(X_int).toarray()

# TODO K-fold
scores = np.array(scores)
baseline = np.array(baseline)
kf = KFold(n_splits=10)

words = {}

alpha = [0.0, 0.001, 0.1, 1.0, 5.0, 10.0, 25.0, 50.0, 70.0, 100.0]
for train_index, test_index in kf.split(setData):
    print(len(train_index))
    print(len(test_index))

    training = setData.iloc[train_index]
    score = scores[train_index]

    testing = setData.iloc[test_index]
    testScore = scores[test_index]
    testBaseline = baseline[test_index]

    # print('train {}'.format(len(training)))
    # print('trainscore {}'.format(len(score)))
    # print('test {}'.format(len(testing)))
    # print('testscore {}'.format(len(testScore)))
    start = time.time()
    # clf = LinearRegression()

    # Bad
    # clf = LinearSVR()

    # clf = BayesianRidge(alpha_1 = 1.1, lambda_1 = 1.05)
    # guesses heavy on zero
    # clf = RandomForestRegressor(n_estimators=12)

    # Weird
    #clf = MLPRegressor(warm_start=True, hidden_layer_sizes=(100,))

    # 0.21 MAE =
    # clf = Ridge(alpha = 0.10)
    # Run over night
    #clf = SVR(kernel='rbf', C=1e3, gamma=0.1)

    clf = KNeighborsClassifier(n_neighbors=3)
    #for x in range(4001):
    print('hree')
    clf.fit(training, score)
    print('hree')

    test = clf.predict(testing)
    convert = []
    print(np.mean((clf.predict(testing) - testScore) ** 2))

    print('\n\nfitting took {}'.format(time.time() - start))



    for x in test:
        convert.append(int(x) )

    # print("Baseline varience score : {} ".format(clf.score(testing,testScore)))
    #print("Varience score : {} ".format(clf.score(testing,testScore)))
    print("Baseline r^2 score : {} ".format(r2_score(testScore,testBaseline)))
    print("r^2 score : {} ".format(r2_score(testScore,convert)))
    # for a in range(25, 50):
    #     print('alpha : {}'.format(a))
    #     clf = Ridge(alpha = a)
    #     print("Cross val score : {} ".format(cross_val_score(clf, testing, testScore, cv=2)))
    print("mean absolute error : {}".format(mean_absolute_error(testScore, convert)))
    print("base mean absolute error : {}\n".format(mean_absolute_error(testScore, testBaseline)))


    # for guess, actual in zip(convert, testScore):
    #     word = (guess, actual)
    #     if word in words:
    #         words[word] += 1
    #     else:
    #         words[word] = 1
    # temp = sorted(words.items(), key=operator.itemgetter(1))
    # pp.pprint(temp)

    plt.scatter(convert, testBaseline)
    plt.xlabel('guess')
    plt.ylabel('actual score')

plt.show()



#
# # for x in zip(test, testScore):
# #     print("{:>7}     |    {}".format(int(x[0]),int(x[1])))
