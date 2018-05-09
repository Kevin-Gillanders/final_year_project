import sqlite3
import time
import pprint as pp
import datetime
import numpy as np
import scipy.stats as sp
import math


# I implemented the chi square test and cramers V tests myself, as the scipy
# Chi square doese not have the functionaliy I require and cramers v is not
# implemented in the library

# The scipy chi assumes that the data is normally disttributed and makes an
# appropriate expected values. My value is not normally distributed and as such
# I need to make my own expected values 

# My methods are implemented for one or both tables

def ChiSquared(c, var1, var2, tableName):
    # Gets all variable types for example lang : en, es, ko... etc
    c.execute('''SELECT ''' + var1 + ''', count(*)
                 FROM ''' + tableName + '''
                 GROUP BY 1''')
    # puts variables into a List
    # tallies up the total
    col = []
    total = 0
    for rows in c.fetchall():
        total += rows[1]
        col.append(rows)

    # Same as above
    c.execute('''SELECT ''' + var2 + ''', count(*)
                 FROM ''' + tableName + '''
                 GROUP BY 1''')
    row = []
    for rows in c.fetchall():
        row.append(rows)

    # Chi-square needs both the observed values
    # and expected values which is given by:
    # (coloumnTotal/total)*rowTotal
    observed = []
    expected = []
    chi = 0.0
    print("\nvar1 : {}    var2 : {}".format(var1, var2))
    # Step through coloumns filling up both observed and expected lists
    for x in col:
        for y in row:
            c.execute('''SELECT count(*)
                         FROM ''' + tableName + '''
                         WHERE ''' + var1 + ''' = ? AND ''' + var2 + ''' = ?;''', (x[0], y[0],))
            # Calculate corresponding expected value
            expected.append((x[1] / total) * y[1])
            for rows in c.fetchall():
                # Chi value given by:
                # sum(((observed[i]-expected[i])^2)/expected[i])
                chi += math.pow((rows[0] - expected[len(expected) - 1]), 2) / expected[len(expected) - 1]
                observed.append(rows[0])
    print('chi : {} '.format(chi))
    print('total : {}    len(rows)-1 : {}   len(col)-1 :  {}'.format(total, str(len(row) - 1), str(len(col) - 1)))
    # Chi-square is very senstive to large sample size, carmer V(based on chi)
    # gives the stength of the association between two variables
    cramerV = math.sqrt((chi / total) / min(len(row) - 1, len(col) - 1))
    print('Cramer V : {}'.format(str(cramerV)))

    # The scipy chisquare is used as It does provide me with the p value
    x = sp.chisquare(observed, expected)
    print(x)
    return ([x[1], cramerV])


def MultipleTableChiSquared(c, var1, var2, tableName, secondTable):
    # Values must be passed in with var1 belonging to tableName and
    # var2 belonging to secondTable

    # Same as above method except this joins the two tables together
    # So catagorical variables from one table can be compared to the other
    c.execute('''SELECT ft.''' + var1 + ''', count(*)
    FROM ''' + tableName + ''' as ft JOIN ''' + secondTable + ''' AS st ON st.subreddit_id == ft.subreddit_id
    GROUP BY 1''')

    col = []
    total = 0
    for rows in c.fetchall():
        total += rows[1]
        col.append(rows)

    c.execute('''SELECT st.''' + var2 + ''', count(*)
                 FROM ''' + tableName + ''' as ft JOIN ''' + secondTable + ''' AS st ON st.subreddit_id == ft.subreddit_id
                 GROUP BY 1''')

    row = []
    for rows in c.fetchall():
        row.append(rows)

    observed = []
    expected = []
    chi = 0.0
    print("\nvar1 : {}    var2 : {}".format(var1, var2))
    for x in col:
        for y in row:
            c.execute('''SELECT count(*)
                         FROM ''' + tableName + ''' AS ft JOIN ''' + secondTable + ''' AS st ON st.subreddit_id == ft.subreddit_id
                         WHERE  ft.''' + var1 + ''' = ? AND st.''' + var2 + ''' = ?;''', (x[0], y[0], ))
            expected.append((x[1] / total) * y[1])
            for rows in c.fetchall():
                chi += math.pow((rows[0] - expected[len(expected) - 1]), 2) / expected[len(expected) - 1]
                observed.append(rows[0])

    print('chi : {} '.format(chi))
    print('total : {}    len(rows)-1 : {}   len(col)-1 :  {}'.format(total, str(len(row) - 1), str(len(col) - 1)))
    cramerV = math.sqrt((chi / total) / min(len(row) - 1, len(col) - 1))
    print('Cramer V : {}'.format(str(cramerV)))

    x = sp.chisquare(observed, expected)
    print(x)
    return ([x[1], cramerV])


def makeChiMatrix(tableName):
    # Puts all chi square associations in csv
    if tableName == 'subreddits':
        catagoricalVariables = ['agg_subscribers', 'agg_accounts_active', 'agg_comment_score_hide_mins','show_media', 'over_18', 'submission_type', 'lang',
                                'subreddit_type', 'advertiser_category', 'accounts_active_is_fuzzed']
    elif tableName == 'posts':
        catagoricalVariables = ['agg_score', 'agg_num_comments', 'agg_gilded','media_attached',
                                'weekday', 'hour', 'cal_date', 'over_18', 'is_self']

    row = []
    with open(tableName + "chi.csv", 'w') as w:
        w.write('\t' + '\t'.join(catagoricalVariables) + '\n')
        for var1 in catagoricalVariables:
            row = [var1]
            for var2 in catagoricalVariables:
                if var1 == var2:
                    row.append('null')
                    continue
                row.append(str((ChiSquared(c, var1, var2, tableName))))
            w.write('\t'.join(row) + '\n')
    row = []


def makeMultipleTableChiMatrix():
    # Puts all chi square associations in csv
    subredditsCatagoricalVariables = ['agg_subscribers', 'agg_accounts_active', 'agg_comment_score_hide_mins','show_media', 'over_18', 'submission_type', 'lang', 'subreddit_type', 'advertiser_category', 'accounts_active_is_fuzzed']
    postsCatagoricalVariables = ['agg_score', 'agg_num_comments', 'agg_gilded', 'media_attached', 'weekday', 'hour', 'cal_date', 'over_18', 'is_self']
    row = []
    with open("multitablechi.csv", 'w') as w:
        w.write('\t' + '\t'.join(subredditsCatagoricalVariables) + '\n')
        w.flush()
        try:
            for var1 in postsCatagoricalVariables:
                row = [var1]
                for var2 in subredditsCatagoricalVariables:
                    if var1 == var2:
                        row.append('null')
                        continue
                    row.append(str((MultipleTableChiSquared(c, var1, var2, 'posts', 'subreddits'))))
                w.write('\t'.join(row) + '\n')
                w.flush()
        except KeyboardInterrupt:
            w.flush()
    row = []


conn = sqlite3.connect('../../data/data.db')
c = conn.cursor()
start = time.time()


makeChiMatrix('posts')
makeMultipleTableChiMatrix()
makeChiMatrix('subreddits')


end = time.time()
print('It took ' + str(end - start))
c.close()
conn.close()
