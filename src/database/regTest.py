from sklearn.linear_model import Ridge, LinearRegression
import numpy as np
import sqlite3
import time
import pprint as pp
import datetime
import numpy as np
import scipy.stats as sp
import math
import itertools
from multiprocessing import Pool
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, OneHotEncoder


conn = sqlite3.connect('../../data/data.db')
c = conn.cursor()
startTime = time.time()

scores = []
setData = []

# c.execute('''SELECT st.lang
#              FROM subreddits AS st
#              GROUP BY 1
#              ''')
#
# X_int = LabelEncoder()
# labels = []
# for rows in c.fetchall():
#     labels.append([rows[0]])
#
# labels = np.array(labels)
#
# X_int = LabelEncoder().fit_transform(labels.ravel()).reshape(*labels.shape)
#
#

c.execute('''SELECT ft.score, st.subscribers, st.lang
             FROM posts as ft JOIN subreddits AS st ON st.subreddit_id == ft.subreddit_id
             WHERE score > 1 AND score < 8000
             ''')


for rows in c.fetchall():
    scores.append(rows[0])
    setData.append([rows[1]])

score = scores[int(len(scores)*.9):]
X = setData[int(len(scores)*.9):]

testScore = scores[:int(len(scores)*.1)]
Y = setData[:int(len(scores)*.1)]

# clf = Ridge(alpha=0.03)
clf = LinearRegression()
clf.fit(X, score)

test = list(clf.predict(Y))
convert = []



print(clf.score(Y,testScore))
for x in test:
    convert.append(int(x))


plt.scatter(convert,testScore)
plt.xlabel('guess')
plt.ylabel('actual score')
plt.show()

# for x in zip(test, testScore):
#     print("{:>7}     |    {}".format(int(x[0]),int(x[1])))

print(accuracy_score(testScore, convert, normalize = True))

conn.rollback()
c.close()
conn.close()
