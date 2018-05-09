import sqlite3
import time
import pprint as pp
import datetime


def createTable(c, conn, tableName):
    # sets up tables
    if tableName == 'posts':
        c.execute("""CREATE TABLE IF NOT EXISTS posts
        (suggested_sort TEXT, secure_media_embed TEXT, ups INTEGER, gilded INTEGER,
        spoiler TEXT, contest_mode TEXT, subreddit_id BLOB, stickied TEXT, author BLOB, name BLOB, media_embed TEXT, approved_by BLOB,
        link_flair_css_class BLOB, quarantine TEXT, is_self TEXT, url BLOB, id BLOB PRIMARY KEY NOT NULL, distinguished TEXT,
        created INTEGER, _orphaned TEXT, removal_reason TEXT, over_18 TEXT, author_flair_css_class BLOB,
        subreddit BLOB, link_flair_text BLOB, selftext BLOB, hidden TEXT, user_reports TEXT,
        num_reports BLOB, score INTEGER, title BLOB, locked TEXT, mod_reports BLOB, media TEXT, created_utc INTEGER,
        edited BLOB, num_comments INTEGER, domain BLOB, secure_media TEXT, author_flair_text BLOB, banned_by BLOB,
        media_attached TEXT, mature TEXT, new_score INTEGER, cal_date INTEGER, hour INTEGER, minute INTEGER, weekday INTEGER,
        FOREIGN KEY(subreddit_id) REFERENCES subreddits(subreddit_id))""")
        conn.commit()

    elif tableName == 'subreddits':
        c.execute("""CREATE TABLE IF NOT EXISTS subreddits
        (show_media TEXT, _path BLOB, over_18 TEXT, created_utc INTEGER, suggested_comment_sort TEXT, hide_ads TEXT, submission_type TEXT,
        public_traffic TEXT, quarantine TEXT, submit_text_label TEXT, submit_text BLOB, subreddit_id BLOB PRIMARY KEY NOT NULL, created INTEGER,
        spoilers_enabled TEXT, lang TEXT, banner_size TEXT, _wiki TEXT, url TEXT, collapse_deleted_comments TEXT, whitelist_status TEXT,
        header_size TEXT, subscribers INTEGER, show_media_preview TEXT, header_title TEXT, id TEXT, submit_link_label TEXT, icon_size TEXT,
        title TEXT, display_name_prefixed TEXT, description BLOB, comment_score_hide_mins INTEGER, user_is_subscriber TEXT, wiki_enabled TEXT,
        accounts_active INTEGER, subreddit_type TEXT, advertiser_category TEXT, accounts_active_is_fuzzed TEXT, display_name TEXT,
        public_description BLOB)""")
        conn.commit()


def populateTable(c, tableName, row):
    # Insert items into tables
    if tableName == 'posts':
        c.executemany("""INSERT INTO """ + tableName + """ VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (convertUnixTimeStamp(tableName, removeSpuriousCols(tableName, row)),))

    elif tableName == 'subreddits':
        variables = removeSpuriousCols(tableName, row)
        # empty string defaults to false, replace empty with None
        variables = [(x if x else 'None') for x in variables]
        if variables[21] == 'None':
            variables[21] = 0

        if variables[33] == 'None':
            variables[33] = 0

        c.executemany("""INSERT INTO """ + tableName + """ VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (variables, ))


def convertUnixTimeStamp(tableName, row):
    if tableName == 'posts':
        time = float(row[34])
        row.append(datetime.datetime.utcfromtimestamp(time).strftime('%d'))
        row.append(datetime.datetime.utcfromtimestamp(time).strftime('%H'))
        row.append(datetime.datetime.utcfromtimestamp(time).strftime('%M'))
        row.append(datetime.datetime.utcfromtimestamp(time).isoweekday())

    return row


def removeSpuriousCols(tableName, row):
    # Remove unwanted coloums from list passed in
    if tableName == 'posts':
        removeSet = set([63, 60, 59, 51, 48, 42, 41, 40, 37, 35, 29, 28, 26,
                        19, 18, 13, 12, 9, 8, 7, 2, 1, 0])

    else:
        removeSet = set([61, 58, 52, 45, 43, 41, 40, 38, 37, 36, 34, 33, 32,
                        29, 26, 23, 22, 21, 18, 17, 16, 15, 13, 11, 6])

    # List comprehension to reomve selected indices
    return [v for i, v in enumerate(row) if i not in removeSet]


def dropTable(c, conn, tableName):
    c.execute('DROP TABLE IF EXISTS ' + tableName + ';')
    conn.commit()


def enterData(c, tableName, r):
    # skip csv header
    next(r)
    for line in r:
        populateTable(c, tableName, line.split('\t'))



def insertAverageScore(c):
    # get average score per subreddit
	c.execute('''SELECT ROUND(AVG(ft.score), 2), st.subreddit_id
				 FROM posts as ft JOIN subreddits as st ON st.subreddit_id == ft.subreddit_id
				 GROUP BY 2
				 ORDER BY 2 desc
				 ''')
	average = []

	for rows in c.fetchall():
		average.append(rows)

	start = time.time()
	# Create the new column
	c.execute('''ALTER TABLE subreddits ADD COLUMN %s INTEGER;''' % 'average_score')
	print('adding averages column took : {}'.format(time.time() - start))
	i = 0
	for index in average:
		start = time.time()
		try:
			c.execute('''UPDATE subreddits SET average_score = ? WHERE ? = subreddit_id;''', (index[0],index[1]))
		except sqlite3.OperationalError:
			print('{} not found'.format(index[2]))
			i+=1
	start = time.time()
	conn.commit()
	print('commit took : {}'.format(time.time() - start))


def binning_data(numeric):
	# Takes the value at the 90th percent and uses
	# that value as a splitting point
	# Keeps doing that until 1000 items left
	if len(numeric) < 1000:
		return [numeric[int(len(numeric) * 0.9)]]
	else:
		return [numeric[int(len(numeric) * 0.9)]] + binning_data(numeric[int(len(numeric) * 0.9)+1:])


def categoriseData(c, var, tableName):
	print("working")
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
		# Create the new column
		c.execute('''ALTER TABLE ''' + tableName + ''' ADD COLUMN %s INTEGER;''' % colName)
		print('adding column took : {}'.format(time.time() - start))

		for index in range(0, len(agg)):
			start = time.time()
            # Updates appropriate column with index if it is greater than the value within
			c.execute('''UPDATE ''' + tableName + ''' SET ''' + colName + ''' = ''' + str(index) + ''' WHERE ''' + var + ''' > ''' + str(agg[index]) + ";")
			print('adding bin {} took : {}'.format(index, time.time() - start))
		start = time.time()
		conn.commit()
		print('commit took : {}'.format(time.time() - start))
	except KeyboardInterrupt:
		c.close()
		conn.close()
	print('{} was added successfully'.format(colName))


def categorise(c):
	#numeric variables to be categorised
	variables = ['score', 'num_comments', 'gilded' ]
    # Table they are associated with
	table = 'posts'

	for var in variables:
		categoriseData(c, var, table)


	variables = ['subscribers', 'accounts_active', 'comment_score_hide_mins' ]
	table = 'subreddits'

	for var in variables:
		categoriseData(c, var, table)


def print_categories(c):
    # Debug
    # Prints out categorised columns
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


def addWeekendColumn(c, conn):
    c.execute('''ALTER TABLE posts ADD COLUMN weekend INTEGER;''')
    c.execute('''UPDATE posts SET weekend = 1 WHERE weekday > 5;''')
    c.execute('''UPDATE posts SET weekend = 0 WHERE weekday <= 5;''')
    conn.commit()


conn = sqlite3.connect('../../data/datatest.db', timeout=10)
c = conn.cursor()

tableName = 'subreddits'
filePath = '../../data/subreddits/cleanedSubs.csv'

start = time.time()

dropTable(c, conn, tableName)
createTable(c, conn, tableName)


with open(filePath, 'r') as r:
    enterData(c, tableName, r)

print(tableName + " created successfully")

tableName = 'posts'
filePath = '../../data/submissions/newPosts.csv'

dropTable(c, conn, tableName)
createTable(c, conn, tableName)

with open(filePath, 'r') as r:
    start = time.time()
    enterData(c, tableName, r)

print(tableName + " created successfully")
insertAverageScore(c)
categorise(c)
addWeekendColumn(c, conn)

end = time.time()
print('It took ' + str(end - start) + ' to input ' + str(conn.total_changes) + ' into posts')

conn.commit()
c.close()
conn.close()
