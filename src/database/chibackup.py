import sqlite3
import time
import pprint as pp
import datetime
import numpy as np
import scipy.stats as sp
import math
def getCountOfUniqueSubs(c):
    #count of distinct subs
    c.execute('''SELECT COUNT(*)
                 FROM (SELECT  count(distinct subreddit), count(subreddit), subreddit
                 FROM posts
                 GROUP BY 3
                 HAVING COUNT(subreddit) > 1
                 ORDER BY 2)
               ''')


def usersWhere(c):
    #Where do the users posts
    c.execute('''SELECT author, subreddit, score, num_comments
                 FROM posts
                 ORDER BY  author, subreddit, score
               ''')

def uniqueSubs(c):
    #List of distinct subreddits
    #Used to in obtaining the subreddit data
    c.execute('''SELECT  DISTINCT subreddit
                 FROM posts''')

def amountOfPostsCatagorised(c):
    c.execute('''SELECT count(*)
                 FROM (SELECT s.advertiser_category,s._path, s.subscribers
                 FROM posts as p INNER JOIN subreddits as s
                 ON s.name == p.subreddit_id
                 WHERE s.advertiser_category != "None"
                 )
                 ''')

def colNamewithItem(c, tableName):
    c.execute('''SELECT * FROM '''+ tableName+''' LIMIT 1''')
    l = []
    for rows in c.fetchall():
        for r in rows:
            l.append(r)
    c.execute('PRAGMA table_info('+subreddits+');')
    k = []
    for rows in c.fetchall():
        k.append(rows[1])
    for r in zip(k, l):
        print(r)

def ChiSquared(c, var1, var2, tableName):
    #TODO Chi-squared
    c.execute('''SELECT '''+var1+''', count(*)
                 FROM '''+tableName+'''
                 GROUP BY 1''')

    col = []
    total = 0
    for rows in c.fetchall():
        total += rows[1]
        col.append(rows)
    print(col)
    c.execute('''SELECT '''+var2+''', count(*)
                 FROM '''+tableName+'''
                 GROUP BY 1''')

    row = []
    for rows in c.fetchall():
        row.append(rows)
    print(row)
    #print("Total : " + str(total))
    observed = []
    expected = []
    chi = 0.0
    print("\nvar1 : {}    var2 : {}".format(var1, var2))
    for x in col:
        for y in row:
            c.execute('''SELECT count(*)
                         FROM '''+tableName+'''
                         WHERE  '''+var1+''' = ? AND '''+var2+''' = ?;''', (x[0], y[0],))
            #print((x[1]/total)*y[1])
            expected.append((x[1]/total)*y[1])
            for rows in c.fetchall():
                #print('cell : {} , {} ,  {} , {}, {}'.format(rows, x, y , total, expected[len(expected)-1]))
                #print('chi : {}'.format(math.pow((rows[0]-expected[len(expected)-1]),2)/expected[len(expected)-1]))
                chi += math.pow((rows[0]-expected[len(expected)-1]),2)/expected[len(expected)-1]
                observed.append(rows[0])
                print('varibles :  {}  , {}    observed : {}    expected : {}'.format(x[0], y[0],rows[0], str(expected[len(expected)-1])))
            #print(x,y)
    # for x in zip(observed, expected):
    #     print('observed : '+ str(x[0])+ '  expected : ' + str(x[1]))
    print('chi : {} '.format(chi))
    for r in zip(observed, expected):
        print(r)
    x = sp.chisquare(observed, expected)
    print(x)
    print('\n\n\n\n')
    return x

def makeChiMatrix(tableName):
    if tableName == 'subreddits':
        catagoricalVariables = ['show_media','over_18','submission_type','lang','subreddit_type','advertiser_category','accounts_active_is_fuzzed']
    elif tableName == 'posts':
        catagoricalVariables = ['over_18','weekday']

    row = []
    with open(tableName+"chi.csv", 'w') as w:
        w.write(','+ ','.join(catagoricalVariables)+'\n')
        for var1 in catagoricalVariables:
            row = [var1]
            for var2 in catagoricalVariables:
                if var1 == var2:
                    row.append('null')
                    continue
                row.append(str((ChiSquared(c, var1, var2,  tableName)[1])))
            w.write(','.join(row)+'\n')
    row = []
    print('done\nStarting domain \n')
    # with open("domanincChi.csv", 'w') as w:
    #     w.write(','+ ','.join(catagoricalVariables)+'\n')
    #     var1 = 'domain'
    #     for var2 in catagoricalVariables:
    #         if var1 == var2:
    #             row.append('null')
    #             continue
    #         row.append(str((ChiSquared(c, var1, var2,  tableName)[1])))
    #     w.write(','.join(row)+'\n')

conn = sqlite3.connect('../../data/data.db')
c = conn.cursor()
start = time.time()
#c.execute("SELECT ups, count(*) FROM posts GROUP BY ups ORDER BY 2")
#c.execute("SELECT min(created), max(created) FROM posts")
#for rows in c.fetchall():
#    print('min : ' + str(time.strftime("%a, %d %b %Y %H:%M:%S",time.gmtime(rows[0]))))
#    print('max : ' + str(time.strftime("%a, %d %b %Y %H:%M:%S",time.gmtime(rows[1]))))

#c.execute('''SELECT ROUND(AVG(ups),2),MAX(ups), COUNT(subreddit), subreddit
#            FROM posts
#            GROUP BY 4
#            HAVING count(subreddit) > 25
#            ORDER BY 1''')



#getCountOfUniqueSubs(c)
#usersWhere(c)
#c.execute('''SELECT s.over_18, p.over_18 ,s.advertiser_category,s._path, count(*)
#             FROM subreddits as s, posts as p
#             WHERE S.name == p.subreddit_id AND s.over_18 != p.over_18 AND s.over_18 == 'False'
#             GROUP BY 4
#             ORDER BY 1
#           ''')

#c.execute('''SELECT p.accounts_active_is_fuzzed , count(*)
#             FROM subreddits as p
#             group by 1
#             ORDER BY 2
#             ''')
#ROUND(AVG(score), 2), ROUND(AVG(num_comments), 2),
#c.execute('''SELECT COUNT(weekday) ,weekday, COUNT(hour), hour, round(avg(score),2)
#             FROM posts
#             GROUP BY 4
#             ORDER BY 5''')




#uniqueSubs(c)
#usersWhere(c)


makeChiMatrix('subreddits')


print('\n')
for rows in c.fetchall():
    print(rows)

with open('subs.txt' , 'w') as f:
    for rows in c.fetchall():
        f.write(str(rows[0]) + '\n')

end = time.time()
print('It took '+ str(end - start))
c.close()
conn.close()

'''
unique subs
(55633,)
It took 57.799784660339355
kevin@kevin-HP-EliteBook-8470p:~/4thYearProject$ python3 data.py
unique users
(1052511,)

'''
