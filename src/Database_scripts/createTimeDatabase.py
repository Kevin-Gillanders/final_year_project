import sqlite3
import time
import pprint as pp
import datetime


def createTable(c, conn, tableName):
    # create table
    if tableName == 'posts':
        c.execute("""CREATE TABLE IF NOT EXISTS posts
        (id TEXT NOT NULL, time_stamp INTEGER NOT NULL, batch INTEGER, time_obtained INTEGER,
        created_utc INTEGER, subreddit_id TEXT, score INTEGER, title BLOB, title_length INTEGER,
        domain TEXT, num_comments INTEGER, over_18 TEXT, subreddit_name TEXT, is_self TEXT,
        author TEXT, cal_date INTEGER, hour INTEGER, minute INTEGER, weekday INTEGER,
        PRIMARY KEY (id, time_stamp))""")
        conn.commit()


def populateTable(c, tableName, row):
    # insert data
    if tableName == 'posts':
        c.executemany("""INSERT INTO posts VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (convertUnixTimeStamp(tableName, row),) )


def convertUnixTimeStamp(tableName, row):
    #convert the time stamp to date, hour, minute and weekday
    if tableName == 'posts':
        time = float(row[4])
        row.append(datetime.datetime.utcfromtimestamp(time).strftime('%d'))
        row.append(datetime.datetime.utcfromtimestamp(time).strftime('%H'))
        row.append(datetime.datetime.utcfromtimestamp(time).strftime('%M'))
        row.append(datetime.datetime.utcfromtimestamp(time).isoweekday())

    return row


def dropTable(c, conn, tableName):
    c.execute('DROP TABLE IF EXISTS ' + tableName + ';')
    conn.commit()


def enterData(c, tableName, r):
    # skip csv header
    next(r)
    for line in r:
        populateTable(c, tableName, line.replace('\n', '').split('\t'))



conn = sqlite3.connect('../../data/timeData.db', timeout=10)
c = conn.cursor()

tableName = 'posts'
filePath = '../../data/timeSubs/time.csv'

start = time.time()

dropTable(c, conn, tableName)
createTable(c, conn, tableName)


with open(filePath, 'r') as r:
    enterData(c, tableName, r)

print(tableName + " created successfully")


end = time.time()
print('It took ' + str(end - start) + ' to input ' + str(conn.total_changes) + ' into posts')

conn.commit()
c.close()
conn.close()
