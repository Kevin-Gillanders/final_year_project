import sqlite3
import time
import pprint as pp
import datetime
import numpy as np
import scipy.stats as sp
import math
import itertools
from multiprocessing import Pool


def calculateRval(perm):
    permutation = {}
    valSwap = []
    # swap out category with number
    for val in range(0,len(perm)):
        permutation[perm[val]] = val
    for val in value:
        valSwap.append(permutation.get(val))
    # R value of two lists
    x = sp.pearsonr(valSwap, score)
    print([x,permutation])
    return [x,permutation]


def rval(c, catagoricalVariable, numericVariable, tableName, value, score):
    # This encodes all categorical variables with a numeric value
    # The encoding is then compared to a numeric variable
    start = time.time()
    categories = getCategoricalData(c, catagoricalVariable, tableName)
    c.execute('''SELECT ''' + catagoricalVariable + ''', ''' + numericVariable + '''
                 FROM ''' + tableName + '''
                 ORDER BY 2''')

    for rows in c.fetchall():
        value.append(rows[0])
        score.append(rows[1])

    vals = processData(categories)

    with open('rvaluesMultiTable.txt', 'w') as w:
        for value in vals:
            w.write(str(value) + ' \n')

    end = time.time()
    print('It took ' + str(end - start))
    return vals


def multipleTableRval(c, catagoricalVariable, numericVariable, tableName, secondTable, value, score):
    # Select a catagorical variable to
    # assign a numeric value to
    start = time.time()
    categories = getCategoricalData(c, catagoricalVariable, tableName)

    c.execute('''SELECT ft.''' + catagoricalVariable + ''', st.''' + numericVariable +
              ''' FROM ''' + tableName + ''' AS ft JOIN ''' + secondTable + ''' AS st ON st.subreddit_id == ft.subreddit_id''')

    for rows in c.fetchall():
        value.append(rows[0])
        score.append(rows[1])

    vals = processData(categories)

    with open('rvalues.txt', 'w') as w:
        for value in vals:
            w.write(str(value) + ' \n')

    end = time.time()
    print('It took ' + str(end - start))
    return vals


def getCategoricalData(c, catagoricalVariable, tableName):
    # Select a catagorical variable to
    # assign a numeric value
    c.execute('''SELECT ''' + catagoricalVariable + ''', count(*)
                 FROM ''' + tableName + '''
                 GROUP BY 1
                 ORDER BY 2''')

    categories = []
    for rows in c.fetchall():
        categories.append(rows[0])
    return categories

def processData(categories):
    #use multiprocessing to speed up the process
    vals = []
    try:
        p = Pool(4)
        vals = p.map(calculateRval, itertools.permutations(categories))

    except KeyboardInterrupt:
        print('KeyboardInterrupt')

    return vals

def multi_table_numeric_rval(c, var1, var2, tableName, secondTable):
    c.execute('''SELECT ft.''' + var1 + ''', st.''' + var2 +'''
                 FROM ''' + tableName + ''' AS ft JOIN ''' + secondTable + ''' AS st ON st.subreddit_id == ft.subreddit_id''')
    x = []
    y = []
    for rows in c.fetchall():
        x.append(rows[0])
        y.append(rows[1])

    print('{} and {} have an r-value of {}'.format(var1, var2, sp.pearsonr(x, y)))

def numeric_rval(c, var1, var2, tableName):
        c.execute('''SELECT ''' + var1 + ''', ''' + var2 +'''
                     FROM ''' + tableName )
        x = []
        y = []
        for rows in c.fetchall():
            x.append(int(rows[0]))
            y.append(int(rows[1]))

        print('{} and {} have an r-value of {}'.format(var1, var2, sp.pearsonr(x, y)))

conn = sqlite3.connect('../../data/data.db')
c = conn.cursor()
start = time.time()


value = []
score = []

rval(c, 'media_attached', 'score', 'posts', value, score)

# Compare numeric variables in each table
postVariables = ['score', 'optimal_time', 'num_comments', 'gilded', 'weekend']
subVariables = ['subscribers', 'accounts_active', 'comment_score_hide_mins' ]

for var1 in postVariables:
    for var2 in postVariables:
        if var1 == var2:
            continue
        else:
            numeric_rval(c, var1, var2, 'posts')



for var1 in subVariables:
    for var2 in subVariables:
        if var1 == var2:
            continue
        else:
            numeric_rval(c, var1, var2, 'subreddits')

for var1 in postVariables:
    for var2 in subVariables:
        multi_table_numeric_rval(c, var1, var2, 'posts', 'subreddits')

pp.pprint(multipleTableRval(c, 'submission_type', 'score', 'subreddits', 'posts', value, score))
pp.pprint(rval(c, 'submission_type', 'accounts_active', 'subreddits', value, score))

end = time.time()
print('It took {} '.format(str(end - start)))
c.close()
conn.close()
