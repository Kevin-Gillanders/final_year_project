import sqlite3
import time
import pprint as pp
import datetime
import numpy as np
import scipy.stats as sp
import math
import itertools
from multiprocessing import Pool
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, HPacker, VPacker
import pandas as pd
import operator
from nltk.corpus import stopwords
from scipy.stats import mannwhitneyu

def getCountOfUniqueSubs(c):
	# count of distinct subs
	c.execute('''SELECT COUNT(*)
				FROM (SELECT  count(distinct subreddit), count(subreddit), subreddit
				FROM posts
				GROUP BY 3
				HAVING COUNT(subreddit) > 1
				ORDER BY 2)
				''')


def usersWhere(c):
	# Where do the users posts
	c.execute('''SELECT author, subreddit, score, num_comments
				 FROM posts
				 ORDER BY  author, subreddit, score
				''')


def uniqueSubs(c):
	# List of distinct subreddits
	# Used to in obtaining the subreddit data
	c.execute('''SELECT  DISTINCT subreddit
				FROM posts''')


def amountOfPostsCatagorised(c):
	# Count which posts have been posted
	# In a subreddit which has an advertiser category
    c.execute('''SELECT count(*)
                 FROM (SELECT s.advertiser_category,s._path, s.subscribers
                 FROM posts as p INNER JOIN subreddits as s
                 ON s.name == p.subreddit_id
                 WHERE s.advertiser_category != "None"
                 )
                 ''')


def colNamewithItem(c, tableName):
    c.execute('''SELECT * FROM ''' + tableName + ''' LIMIT 1''')
    l = []
    for rows in c.fetchall():
        for r in rows:
            l.append(r)
    c.execute('PRAGMA table_info(' + tableName + ');')
    k = []
    for rows in c.fetchall():
        k.append(rows[1])
    for r in zip(k, l):
        print(r)


def freedman_diaconis(numeric):
	# A method for deciding one how may bins
	# data should be split into
	# http://link.springer.com/article/10.1007%2FBF01025868
	numeric = sorted(numeric)
	first = numeric[int(len(numeric) / 4)]
	second = numeric[int(len(numeric) / 2)]
	third = numeric[int(len(numeric) * .75)]
	sampleSize = len(numeric)

	print("first : {}  third : {}  sample  {}".format(first, third, sampleSize))

	IQR = third - first
	print("iqr : {}    -sqr  {}".format(IQR, math.pow(sampleSize, -(1 / 3))))

	h = 2 * (IQR) * math.pow(sampleSize, -(1 / 3))
	print("h : {}".format(h))

	minimum = numeric[0]
	maximum = numeric[-1]


	print("Max {}    Min {}".format(maximum, minimum))
	return int((maximum - minimum) / h)


def bins(seq, width):
	seq = sorted(seq)
	step = seq[len(seq)-1] / width
	count = 0
	out = []
	for val in seq:
		if val < step:
			out.append(count)
		else:
			step += seq[len(seq)-1] / width
			count += 1
			out.append(count)
	return out


def binning_data(numeric):
	# Takes the value at the 90th percent and uses
	# that value as a splitting point
	# Keeps doing that until 1000 items left
	if len(numeric) < 1000:
		return [numeric[int(len(numeric) * 0.9)]]
	else:
		return [numeric[int(len(numeric) * 0.9)]] + binning_data(numeric[int(len(numeric) * 0.9)+1:])


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
		# Create the new column
		c.execute('''ALTER TABLE ''' + tableName + ''' ADD COLUMN %s INTEGER;''' % colName)
		print('adding coloumn took : {}'.format(time.time() - start))

		for index in range(0, len(agg)):
			start = time.time()
			# Sets Aggregated coloumn equal to correct index
			# Update posts SET agg_score = 1 WHERE score > 47
			c.execute('''UPDATE ''' + tableName + ''' SET ''' + colName + ''' = ''' + str(index) + ''' WHERE ''' + var + ''' > ''' + str(agg[index]) + ";")
			print('adding {} took : {}'.format(index, time.time() - start))
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
	table = 'posts'

	for var in variables:
		categoriseData(c, var, table)


	variables = ['subscribers', 'accounts_active', 'comment_score_hide_mins' ]
	table = 'subreddits'

	for var in variables:
		categoriseData(c, var, table)


def print_categories(c):
	# Prints all category bands
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


def getColumnNames():
	labels = []
	c.execute('PRAGMA table_info(posts);')
	for rows in c.fetchall():
	    labels.append('ft.'+rows[1])
	# remove predictor variable
	labels.remove('ft.score')
	print(', '.join(labels))
	print('\n\n')
	labels = []
	c.execute('PRAGMA table_info(subreddits);')
	for rows in c.fetchall():
	    labels.append('st.'+rows[1])
	print(', '.join(labels))
	print('\n\n')


def insertAverageScore(c):
	# Get average per subreddi
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
	print('adding coloumn took : {}'.format(time.time() - start))
	i = 0
	for index in average:
		start = time.time()
		print(index)
		# add average to correct sub
		c.execute('''UPDATE subreddits SET average_score = ? WHERE ? = subreddit_id;''', (index[0],index[1]))
		print(str(index[1]))

	start = time.time()
	conn.commit()
	print('commit took : {}'.format(time.time() - start))


def scoreOver100(c):
	counts = []
	counts100 = []
	hour = []
	# Counts of posts
	c.execute('''SELECT COUNT(*), hour, created_utc
				 FROM posts
				 GROUP BY weekday, hour''')

	for rows in c.fetchall():
		counts.append(rows[0])
		hour.append((rows[1], rows[2]))

	#count ofposts with over 100 points
	c.execute('''SELECT COUNT(*)
				 FROM posts
				 WHERE score > 100
				 GROUP BY weekday, hour''')

	for rows in c.fetchall():
		counts100.append(rows[0])

	percent = []
	count = 0
	for x, y, z in zip(counts100, counts, hour):
		percent.append(float(x/y)*100)
		count += 1
		print("the percent is : {:.4f}  for hour {}".format(float(x/y)*100, z))


	# Set date range to begin on a Monday at 12 AM as this is how my data is ordered
	# Periods is the length of the data and a tick happens every hour
	times = pd.date_range('2017-04-17 00:00', periods=count, freq='1H')

	fig, ax = plt.subplots(1)
	fig.autofmt_xdate()

	# Sets labels
	counts = [x  for x in counts]
	plt.xlabel('Time - EST')
	plt.ylabel('% score over 100')
	plot1 = ax.plot( times, percent, label= 'Posts over 100 votes' )

	# Sets x axis to correspond to time
	xfmt = mdates.DateFormatter('%a %H:%M')
	ax.xaxis.set_major_formatter(xfmt)

	# Second axis
	ax2 = ax.twinx()
	plot2 = ax2.plot( times, counts, 'r', label='Total no. of posts' )
	ax2.set_ylabel('Total posts')

	# Puts both legends in one box
	lines = plot1 + plot2
	labels = [l.get_label() for l in lines]
	ax.legend(lines, labels, loc='upper right', bbox_to_anchor=(0.90, 1.0))

	times = times.tolist()
	times = [times[i] for i in range(0, len(times)) if i % 5 == 0]

	plt.xticks(times)
	ax.xaxis.grid(True)
	plt.grid()
	plt.title("Posts with over 100 votes\nagainst total posts")
	plt.show()


def commentsOver100(c):
	counts = []
	counts100 = []
	hour = []
	# Total count of posts grouped by hour
	c.execute('''SELECT COUNT(*), hour, created_utc
				 FROM posts
				 GROUP BY weekday, hour''')

	for rows in c.fetchall():
		counts.append(rows[0])
		hour.append((rows[1], rows[2]))

	# Total count of posts over 100 comments
	c.execute('''SELECT COUNT(*)
				 FROM posts
				 WHERE num_comments > 100
				 GROUP BY weekday, hour''')

	for rows in c.fetchall():
		counts100.append(rows[0])

	percent = []
	count = 0
	for x, y, z in zip(counts100, counts, hour):
		#Figure out percent
		percent.append(float(x/y)*100)
		count += 1
		print("Percent of posts over 100 comments is : {:.4f}  for hour {}".format(float(x/y)*100, z))


	# Sets date ranage for x axis ticks
	times = pd.date_range('2017-04-17 00:00', periods=count, freq='1H')
	fig, ax = plt.subplots(1)
	fig.autofmt_xdate()



	# Sets labels
	plt.xlabel('Time - EST')
	plt.ylabel('% score over 100')
	plot1 = ax.plot( times, percent, label= 'posts over 100 comments' )

	#Set format of xaxis
	xfmt = mdates.DateFormatter('%a %H:%M')
	ax.xaxis.set_major_formatter(xfmt)

	# New axis
	ax2 = ax.twinx()
	plot2 = ax2.plot( times, counts, 'r', label='total no. of posts' )
	ax2.set_ylabel('Total comments')

	# Create legend
	lines = plot1 + plot2
	labels = [l.get_label() for l in lines]
	ax.legend(lines, labels, loc=0)


	times = times.tolist()
	# Set amount of ticks
	times = [times[i] for i in range(0, len(times)) if i % 5 == 0]

	plt.xticks(times)
	ax.xaxis.grid(True)
	plt.grid()
	plt.title("Posts with over 100 comments\nagainst total posts")
	plt.show()


def setOptimalTime(c, conn):
	# orders the times by the highest average, the times are then broken
	# into bands and assigned a value from 1 to 3
	counts = []
	counts100 = []
	hour = []
	c.execute('''SELECT COUNT(*), hour, created_utc
				 FROM posts
				 GROUP BY hour''')

	for rows in c.fetchall():
		# Total count
		counts.append(rows[0])
		# What hour it was posted
		hour.append(rows[1])

	c.execute('''SELECT COUNT(*)
				 FROM posts
				 WHERE score > 100
				 GROUP BY hour''')

	for rows in c.fetchall():
		# count of posts over 100
		counts100.append(rows[0])

	percent = []
	for x, y, z in zip(counts100, counts, hour):
		# get percentge and hour
		percent.append((float(x/y)*100, z))

	# Sorts list and then breaks it into bands
	# Of eight and these go from least optimal
	# to most optimal
	percent = sorted(percent)
	percent = [percent[i:i+8] for i in range(0, len(percent), 8)]

	# Adds optimal_time coloumn
	c.execute('''ALTER TABLE posts ADD COLUMN optimal_time INTEGER;''')
	pp.pprint(percent)
	group = 1
	for x in percent:
		for y in x:
			print("Y : {}".format(y[1]))
			# Adds what band a particular hour is in, into database
			c.execute('''UPDATE posts SET optimal_time = ? WHERE hour == ?;''', (str(group), str(y[1])))
			pp.pprint("the percent is : {:.4f}  for hour {}.  In group : {}".format(y[0], y[1], group))
		group += 1
	conn.commit()


def getAverageWithMedia(c):
	# Average score of media
	c.execute('''SELECT media_attached, ROUND(AVG(score), 2), SUM(score), COUNT(score)
				 FROM posts
				 GROUP BY media_attached
				 ORDER BY 2''')

	for rows in c.fetchall():
		print(rows)


	c.execute('''SELECT score
				 FROM posts
				 WHERE media_attached = 'image'
				 ''')
	imageVal = []
	for rows in c.fetchall():
		imageVal.append(rows[0])
	c.execute('''SELECT score
				 FROM posts
				 WHERE media_attached != 'image'
				 ''')

	notImageVal = []
	for rows in c.fetchall():
		notImageVal.append(rows[0])

	# Test for signifigance difference between the two sets of numbers
	print(mannwhitneyu(imageVal, notImageVal, alternative = 'greater'))


def percentOver100(c):
	# Gives back the percentage of posts over 100 for every sub which has a post over 100
	counts = []
	counts100 = []
	hour = []
	c.execute('''SELECT COUNT(*), subreddit
				 FROM posts
				 WHERE subreddit IN (SELECT subreddit
						 			 FROM posts
						 			 WHERE score > 100)
				 GROUP BY subreddit
				 ORDER BY subreddit''')

	for rows in c.fetchall():
		counts.append(rows)


	c.execute('''SELECT COUNT(*), subreddit
				 FROM posts
				 WHERE score > 100
				 GROUP BY subreddit
				 ORDER BY subreddit''')

	for rows in c.fetchall():
		counts100.append(rows)

	test = []

	for x, y in zip(counts100, counts):
		# print(x, y)
		test.append((float(x[0]/y[0])*100, y[1], y[0]))


	for x in sorted(test):
		print("total count {} percent {} in {}".format(x[2], x[0], x[1]) )


def frequentWords(c):
	# Gets most common words in posts over 100
	c.execute('''SELECT title
				 FROM posts
				 WHERE score > 100''')

	words = {}
	for rows in c.fetchall():
		rows = rows[0].lower().split(' ')
		rows = [word for word in rows if word not in stopwords.words('english')]
		for word in rows:
			if word in words:
			    words[word] += 1
			else:
			    words[word] = 1

	words = sorted(words.items(), key=operator.itemgetter(1))
	pp.pprint(words)


conn = sqlite3.connect('../../data/data.db')
c = conn.cursor()
startTime = time.time()

scoreOver100(c)
commentsOver100(c)
getAverageWithMedia(c)
percentOver100(c)
frequentWords(c)

end = time.time()
print('It took {} '.format(str(end - startTime)))
c.close()
conn.close()
