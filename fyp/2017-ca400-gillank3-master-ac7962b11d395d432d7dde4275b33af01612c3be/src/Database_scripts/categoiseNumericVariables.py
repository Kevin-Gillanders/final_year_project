import sqlite3
import time


def categoriseData(c, var, tableName):
    c.execute('''SELECT ''' + var + '''
                 FROM ''' + tableName+ '''
                 ORDER BY 1
                    ''')
    numeric = []

    for rows in c.fetchall():
        numeric.append(rows[0])

    agg = binning_data(numeric)
    # insert value which all numbers will be less than to ensure
    # smallest values will be categorised
    agg.insert(0, -100)

    try:
        start = time.time()
        colName = 'agg_' + str(var)
        #insert new column for aggregation
        try:
            c.execute('''ALTER TABLE IF NOT EXISTS ''' + tableName + ''' ADD COLUMN %s INTEGER;''' % colName)
        except sqlite3.OperationalError:
            print('{} already exists'.format(colName))

        print('adding coloumn took : {}'.format(time.time() - start))

        for index in range(0, len(agg)):
            start = time.time()
            # UPDATE table SET newColumn = indexOfCategory WHERE variablePassed > agg[index]
            c.execute('''UPDATE ''' + tableName + ''' SET ''' + colName + ''' = ''' + str(index) + ''' WHERE ''' + var + ''' > ''' + str(agg[index]) + ";")
            print('adding {} took : {}'.format(index, time.time() - start))
        start = time.time()
        # Commit change to database
        conn.commit()
        print('commit took : {}'.format(time.time() - start))
    except KeyboardInterrupt:
        conn.rollback()
        c.close()
        conn.close()
    print('{} was added successfully'.format(colName))


def categorise(c):
    # numeric variables to be categorised
    variables = ['score', 'num_comments', 'gilded' ]
    table = 'posts'

    for var in variables:
        categoriseData(c, var, table)


    variables = ['subscribers', 'accounts_active', 'comment_score_hide_mins' ]
    table = 'subreddits'

    for var in variables:
        categoriseData(c, var, table)


def print_categories(c):
    # Prints out newly made categories for testing
    variables = ['score', 'num_comments', 'gilded' ]
    table = 'posts'
    for var in variables:
        c.execute('''SELECT agg_''' + var + ''' , COUNT(*)
                     FROM ''' + table +'''
                     GROUP BY 1''')

        print("agg_{} has".format(var))

        for rows in c.fetchall():
            print(rows)
        print('\n')
    print('\n==============================================\n')
    variables = ['subscribers', 'accounts_active', 'comment_score_hide_mins' ]
    table = 'subreddits'

    for var in variables:
        c.execute('''SELECT agg_''' + var + ''' , COUNT(*)
                     FROM ''' + table + '''
                     GROUP BY 1''')
        print("agg_{} has".format(var))
        for rows in c.fetchall():
            print(rows)
        print('\n')


def binning_data(numeric):
    # Takes 90% of a list away and records the 90% value
    # This is then used as the break point for a numeric
    # categorisation
    # This repeats until under 1000 items are left in the list
    if len(numeric) < 1000:
        return [numeric[int(len(numeric) * 0.9)]]
    else:
        return [numeric[int(len(numeric) * 0.9)]] + binning_data(numeric[int(len(numeric) * 0.9)+1:])


conn = sqlite3.connect('../../data/data.db')
c = conn.cursor()
startTime = time.time()

categorise(c)
print_categories(c)

end = time.time()
print('It took {} '.format(str(end - startTime)))
c.close()
conn.close()
