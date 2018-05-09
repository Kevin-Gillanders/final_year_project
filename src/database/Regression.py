from sklearn.linear_model import Ridge, LinearRegression, Lasso, ElasticNet, SGDRegressor, BayesianRidge
import numpy as np
import sqlite3
import time
import numpy as np
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.model_selection import KFold,  cross_val_score
from sklearn.neighbors import KNeighborsClassifier
import random
import operator
import pprint as pp


def insertData(c, setData, scores, baseline):
    for rows in c.fetchall():
        temp = []
        for x in range(1, len(variables)):
            temp.append(rows[x])
        setData.append(temp)
        scores.append(rows[0])
        baseline.append(rows[-1])
    return setData, scores, baseline


def shuffleData(setData, scores, baseline):
    temp = list(zip(setData, scores, baseline))
    random.shuffle(temp)
    setData, scores, baseline = zip(*temp)
    setData = list(setData)
    return setData, scores, baseline


def underSamplingData(c, variables):
    # under sampling of data
    scores = []
    setData = []
    baseline = []
    lim = 15000
    typeFilter = "underSamplingData"
    for cat in range(0, 6):
        c.execute('''SELECT ''' + ','.join(variables) + '''
                     FROM posts as ft JOIN subreddits AS st ON st.subreddit_id == ft.subreddit_id
                     WHERE agg_score == ?
                     LIMIT ?
                     ''', (cat, lim))
        lim -= 2000
        insertData(c, setData, scores, baseline)
    return shuffleData(setData, scores, baseline)


def noFilterOnData(c, variables):
    # No filter, have to limit how many are used as computer runs
    # out of memory past a certain threshold
    scores = []
    setData = []
    baseline = []
    typeFilter = "noFilterOnData"
    c.execute('''SELECT ''' + ','.join(variables) + '''
                 FROM posts as ft JOIN subreddits AS st ON st.subreddit_id == ft.subreddit_id
                 LIMIT 500000
                 ''')
    insertData(c, setData, scores, baseline)
    return shuffleData(setData, scores, baseline)


def filterOnScore(c, variables):
    # Due to the skew in the score
    # variable I thought that removing some of the weight
    # would provide a better result
    scores = []
    setData = []
    baseline = []
    typeFilter = "filterOnScore"
    c.execute('''SELECT ''' + ','.join(variables) + '''
                 FROM posts as ft JOIN subreddits AS st ON st.subreddit_id == ft.subreddit_id
                 WHERE score > 100
                 LIMIT 500000
                 ''')
    insertData(c, setData, scores, baseline)
    return shuffleData(setData, scores, baseline)


def filterOnComments(c, variables):
    # I also tried fitering the data based on the number
    #Of comments it recieved, this was a lot more accurate than
    # filter in score
    scores = []
    setData = []
    baseline = []
    typeFilter = "filterOnComments"
    c.execute('''SELECT ''' + ','.join(variables) + '''
                 FROM posts as ft JOIN subreddits AS st ON st.subreddit_id == ft.subreddit_id
                 WHERE num_comments > 50
                 LIMIT 500000
                 ''')
    insertData(c, setData, scores, baseline)
    return shuffleData(setData, scores, baseline)


def filterOnFrequentSubreddits(c, variables):
    # Fitering the data based on the number of
    # times the subreddit appeared in the database
    scores = []
    setData = []
    baseline = []
    typeFilter = "filterOnFrequentSubreddits"
    c.execute('''SELECT '''+ ','.join(variables) +'''
                 FROM posts as ft JOIN subreddits AS st ON st.subreddit_id == ft.subreddit_id
                 WHERE ft.subreddit IN (SELECT subreddit
                                        FROM posts
                                        GROUP BY 1
                                        HAVING COUNT(subreddit) > 10)
                 LIMIT 800000
                 ''')
    insertData(c, setData, scores, baseline)
    return shuffleData(setData, scores, baseline)


conn = sqlite3.connect('../../data/data.db')
c = conn.cursor()
random.seed(14)
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

categories = True
fileName = ""
typeFilter = [noFilterOnData, filterOnScore, filterOnComments, filterOnFrequentSubreddits, underSamplingData]



# Aggregate bands:
# Score [47, 625, 4017, 5677, 8717]
# num_comments [21, 148, 806, 3074, 11766]
# Score must always be first

if categories:
    variables = ['ft.agg_score']
    fileName = "knnResults.csv"
else:
    variables = ['ft.score']
    fileName = "ridgeResults.csv"

predictors = ['st.subscribers', 'ft.optimal_time', 'ft.is_self', 'ft.over_18', 'ft.media_attached', 'st.agg_accounts_active',
                    'ft.weekday', 'ft.hour', 'ft.minute', 'st.submission_type', 'st.over_18', 'st.advertiser_category', 'st.lang', 'st.average_score']

variables = variables + predictors







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









kf = KFold(n_splits=10)

words = {}

alpha = [0.0, 0.001, 0.1, 1.0, 5.0, 10.0, 25.0, 50.0, 70.0, 100.0]




with open(fileName, 'w') as w:
    w.write("Type of filter, Base r^2 score, Base Mean Error, r^2 score, Mean Error\n")
    for method in typeFilter:
        rBase = 0
        rTest = 0

        maeBase = 0
        maeTest = 0
        setData, scores, baseline = method(c, variables)

        print('amount of scores : {}'.format(len(scores)))
        setData = pd.DataFrame(setData, columns = variables[1:])
        start = time.time()


        setData = pd.get_dummies(setData, sparse = True)
        print('Dummies took {}'.format(time.time() - start))


        scores = np.array(scores)
        baseline = np.array(baseline)

        for train_index, test_index in kf.split(setData):
            print(len(train_index))
            print(len(test_index))

            training = setData.iloc[train_index]
            score = scores[train_index]

            testing = setData.iloc[test_index]
            testScore = scores[test_index]
            testBaseline = baseline[test_index]
            start = time.time()

            if categories:
                clf = KNeighborsClassifier(n_neighbors=3)
            else:
                clf = Ridge(alpha = 0.10)

            clf.fit(training, score)
            test = clf.predict(testing)
            convert = []
            print(np.mean((clf.predict(testing) - testScore) ** 2))

            print('\n\nfitting took {}'.format(time.time() - start))



            for x in test:
                convert.append(int(x) )

            # r^2 score for baseline and  
            print("Baseline r^2 score : {} ".format(r2_score(testScore,testBaseline)))
            print("r^2 score : {} ".format(r2_score(testScore,convert)))
            print("Cross val score : {} ".format(cross_val_score(clf, testing, testScore, cv=2)))
            print("mean absolute error : {}".format(mean_absolute_error(testScore, convert)))
            print("base mean absolute error : {}\n".format(mean_absolute_error(testScore, testBaseline)))

            rBase += float(r2_score(testScore,testBaseline))
            rTest += float(r2_score(testScore,convert))

            maeBase += float(mean_absolute_error(testScore, convert))
            maeTest += float(mean_absolute_error(testScore, testBaseline))

            if categories:
                for guess, actual in zip(convert, testScore):
                    word = (guess, actual)
                    if word in words:
                        words[word] += 1
                    else:
                        words[word] = 1
                temp = sorted(words.items(), key=operator.itemgetter(1))
                pp.pprint(temp)

            plt.scatter(convert, testScore)
            plt.xlabel('guess')
            plt.ylabel('actual score')

        row = [method.__name__, rBase / 10.0, maeBase / 10.0,  rTest / 10.0, maeTest / 10.0]
        w.write(",".join(str(r) for r in row) + '\n')

plt.show()

conn.rollback()
c.close()
conn.close()

#
# # for x in zip(test, testScore):
# #     print("{:>7}     |    {}".format(int(x[0]),int(x[1])))
