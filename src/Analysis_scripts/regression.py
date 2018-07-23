from sklearn.linear_model import Ridge
import numpy as np
import sqlite3
import time
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import KFold,  cross_val_score
from sklearn.neighbors import KNeighborsClassifier
import math
import random
import operator
import pprint as pp


def insertData(c, setData, scores, baseline):
    # Inserts data into correct lists
    for rows in c.fetchall():
        temp = []
        for x in range(1, len(variables) - 1):
            temp.append(rows[x])
        setData.append(temp)
        scores.append(rows[0])
        baseline.append(rows[-2])
        ids.append(rows[-1])
    return setData, scores, baseline


def shuffleData(setData, scores, baseline, count):
    # Puts all items in a single list and randomly shuffles it
    # The list is then unpacked and all elements are placed back
    # now shuffled
    temp = list(zip(setData, scores, baseline))
    random.shuffle(temp)
    setData, scores, baseline = zip(*temp)
    setData = list(setData)
    scores = list(scores)
    baseline = list(baseline)
    if count == 0:
        # Test set is now added to the end of set data
        c.execute('''SELECT ''' + ','.join(variables) + '''
                     FROM posts as ft JOIN subreddits AS st ON st.subreddit_id == ft.subreddit_id
                     WHERE ft.id not in (%s)
                     LIMIT 100000
                     ''' % ','.join('?'*len(ids)), ids)
        for rows in c.fetchall():
            temp = []
            for x in range(1, len(variables) - 1):
                temp.append(rows[x])
            setData.append(temp)
            scores.append(rows[0])
            baseline.append(rows[-2])
        count += 1

    return setData, scores, baseline


def underSamplingData(c, variables, count):
    # proportionally under sampling of data
    scores = []
    setData = []
    baseline = []
    lim = 6000
    for cat in range(0, 6):
        c.execute('''SELECT ''' + ','.join(variables) + '''
                     FROM posts as ft JOIN subreddits AS st ON st.subreddit_id == ft.subreddit_id
                     WHERE agg_score == ?
                     LIMIT ?
                     ''', (cat, lim))
        lim -= 1000
        insertData(c, setData, scores, baseline)
    return shuffleData(setData, scores, baseline, count)


def noFilterOnData(c, variables, count):
    # No filter, have to limit how many are used as computer runs
    # out of memory past a certain threshold
    scores = []
    setData = []
    baseline = []
    c.execute('''SELECT ''' + ','.join(variables) + '''
                 FROM posts as ft JOIN subreddits AS st ON st.subreddit_id == ft.subreddit_id
                 LIMIT 200000
                 ''')
    insertData(c, setData, scores, baseline)
    return shuffleData(setData, scores, baseline, count)


def filterOnScore(c, variables, count):
    # Due to the skew in the score
    # variable I thought that removing some of the weight
    # would provide a better result
    scores = []
    setData = []
    baseline = []
    c.execute('''SELECT ''' + ','.join(variables) + '''
                 FROM posts as ft JOIN subreddits AS st ON st.subreddit_id == ft.subreddit_id
                 WHERE score > 100
                 LIMIT 200000
                 ''')
    insertData(c, setData, scores, baseline)
    return shuffleData(setData, scores, baseline, count)


def filterOnComments(c, variables, count):
    # I also tried fitering the data based on the number
    # Of comments it recieved, this was a lot more accurate than
    # filter in score
    scores = []
    setData = []
    baseline = []
    c.execute('''SELECT ''' + ','.join(variables) + '''
                 FROM posts as ft JOIN subreddits AS st ON st.subreddit_id == ft.subreddit_id
                 WHERE num_comments > 50
                 LIMIT 200000
                 ''')
    insertData(c, setData, scores, baseline)
    return shuffleData(setData, scores, baseline, count)


def filterOnFrequentSubreddits(c, variables, count):
    # Fitering the data based on the number of
    # times the subreddit appeared in the database
    scores = []
    setData = []
    baseline = []
    c.execute('''SELECT '''+ ','.join(variables) +'''
                 FROM posts as ft JOIN subreddits AS st ON st.subreddit_id == ft.subreddit_id
                 WHERE ft.subreddit IN (SELECT subreddit
                                        FROM posts
                                        GROUP BY 1
                                        HAVING COUNT(subreddit) > 10)
                 LIMIT 200000
                 ''')
    insertData(c, setData, scores, baseline)
    return shuffleData(setData, scores, baseline, count)


conn = sqlite3.connect('../../data/data.db')
c = conn.cursor()
random.seed(14)
startTime = time.time()

ids = []
count = 0
scores = []
setData = []
baseline = []


labels = []
categories = True
fileName = ""

# Diffent types of methods
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


predictors = ['st.subscribers', 'ft.optimal_time', 'ft.is_self', 'ft.over_18', 'ft.media_attached', 'st.agg_accounts_active', 'st.accounts_active_is_fuzzed',
                    'ft.weekday', 'ft.hour', 'ft.minute', 'st.over_18', 'st.advertiser_category', 'st.lang', 'st.average_score', 'ft.id']

variables = variables + predictors


fig, ax = plt.subplots(1)


print("testScore len : {}  baseline len : {}".format(len(scores), len(baseline)))
lines = []
with open(fileName, 'w') as w:
    w.write("Type of filter, Base r^2 score, Base Mean Error, r^2 score, Mean Error\n")
    for method in typeFilter:

        rBase = 0
        rTest = 0
        maeBase = 0
        maeTest = 0

        count = 0
        ids = []
        words = {}

        # Populate lists with information
        setData, scores, baseline = method(c, variables, count)
        print('amount of scores : {}'.format(len(scores)))
        setData = pd.DataFrame(setData, columns = variables[1:len(variables)-1])

        start = time.time()
        print("going in")
        # one hot encode variables
        setData = pd.get_dummies(setData, sparse = True)
        print('Dummies took {}'.format(time.time() - start))

        scores = np.array(scores)
        baseline = np.array(baseline)


        testing = setData.iloc[-100000:]
        setData = setData.iloc[:-100000]
        testScore = scores[-100000:]
        scores = scores[:-100000]


        testBaseline = baseline[-100000:]
        baseline = baseline[:-100000]

        training = setData
        score = scores
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
            convert.append(int(x))

        # r^2 score of control and my models prediction
        print("Baseline r^2 score : {} ".format(r2_score(testScore,testBaseline)))
        print("r^2 score : {} ".format(r2_score(testScore,convert)))
        print("Cross val score : {} ".format(cross_val_score(clf, testing, testScore, cv=2)))
        print("mean absolute error : {}".format(mean_absolute_error(testScore, convert)))
        print("base mean absolute error : {}\n".format(mean_absolute_error(testScore, testBaseline)))

        # Prints a dictionary of what the actual value is along with what the programme guessed
        if categories:
            print(method.__name__)
            for guess, actual in zip(convert, testScore):
                word = (guess, actual)
                if word in words:
                    words[word] += 1
                else:
                    words[word] = 1
            temp = sorted(words.items(), key=operator.itemgetter(1))
            pp.pprint(temp)

        rBase += float(r2_score(testScore,testBaseline))
        rTest += float(r2_score(testScore,convert))

        maeBase += float(mean_absolute_error(testScore, testBaseline))
        maeTest += float(mean_absolute_error(testScore, convert))



        temp = ax.scatter(test, testScore, label = method.__name__)
        lines.append(temp)
        plt.xlabel('guess')
        plt.ylabel('actual score')
        if categories:
            plt.title('knn trained on\ndifferently filtered data')
        else:
            plt.title('Ridge regression trained on\ndifferently filtered data')

        row = [method.__name__, rBase, maeBase,  rTest, maeTest]
        w.write(",".join(str(r) for r in row) + '\n')


ax.legend(handles = [lines[0],lines[1],lines[2],lines[3],lines[4]], loc='upper right', bbox_to_anchor=(0.90, 1.0))
plt.show()


conn.rollback()
c.close()
conn.close()
