import sqlite3
import time
import pprint as pp
import datetime
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import Ridge
import pandas as pd
from sklearn.model_selection import KFold,  cross_val_score
from sklearn.metrics import accuracy_score, mean_absolute_error


# showed very poor accuracy with regression, I believe this is because of a
# small sample size

def plotAllPostsAccordingToTime(c):
    c.execute('''SELECT time_stamp, score
                 FROM posts
                 GROUP BY id, time_stamp''')

    timeInterval = []
    score = []
    for rows in c.fetchall():
        timeInterval.append(rows[0] * 5)
        score.append(rows[1])
        if rows[0] == 72:
            plt.plot(timeInterval, score)
            timeInterval = []
            score = []


    plt.title('Votes at 5 minute intervals')
    plt.xlabel('time - minutes')
    plt.ylabel('Score')

    plt.grid()
    plt.show()


conn = sqlite3.connect('../../data/timeData.db', timeout=10)
c = conn.cursor()

start = time.time()



setData = []
scores = []
variables = ['score']
predictors = ['hour', 'over_18', 'is_self']

variables = variables + predictors


c.execute('''SELECT '''+ ','.join(variables) + ''', (SELECT score
                                                     FROM posts as st
                                                     WHERE time_stamp == 72 AND st.id = ft.id) AS score, (SELECT score
                                                                                                         FROM posts as st
                                                                                                         WHERE time_stamp == 72 AND st.id = ft.id) AS num_comments
             FROM posts AS ft
             WHERE time_stamp == 72 AND score > 100
             GROUP BY id
             ''')

for rows in c.fetchall():
    print(rows)
    temp = []
    for x in range(1, len(variables)):
        temp.append(rows[x])
    setData.append(temp)
    scores.append(rows[0])


print('amount of scores : {}'.format(len(scores)))
setData = pd.DataFrame(setData, columns = variables[1:])
start = time.time()
print("going in")
setData = pd.get_dummies(setData, sparse = True)
print('Dummies took {}'.format(time.time() - start))



scores = np.array(scores)
kf = KFold(n_splits=5)


words = {}

for train_index, test_index in kf.split(setData):
    print(len(train_index))
    print(len(test_index))

    training = setData.iloc[train_index]
    score = scores[train_index]

    testing = setData.iloc[test_index]
    testScore = scores[test_index]


    start = time.time()
    clf = Ridge(alpha = 1.0)
    test = clf.predict(testing)
    convert = []
    print(np.mean((clf.predict(testing) - testScore) ** 2))

    print('\n\nfitting took {}'.format(time.time() - start))



    for x in test:
        convert.append(int(x) )

    print("Varience score : {} ".format(clf.score(testing,testScore)))
    print("Cross val score : {} ".format(cross_val_score(clf, testing, testScore, cv=2)))
    print("mean absolute error : {}\n".format(mean_absolute_error(testScore, convert)))


    plt.scatter(convert,testScore)
    plt.title('Ridge regression on time data')
    plt.xlabel('guess')
    plt.ylabel('actual score')

plt.show()

# Orders by average score
# Batch 2 which started at 9am EST is a lot better than the others
c.execute('''SELECT time_stamp, batch, ROUND(avg(score), 2), hour
             FROM posts
             GROUP BY time_stamp, batch
             ORDER BY 3''')

for rows in c.fetchall():
    print(rows)



end = time.time()
print('It took ' + str(end - start) )

conn.commit()
c.close()
conn.close()
