import praw
import time
import pprint as pp
import sqlite3
from threading import Thread
from prawcore.exceptions import PrawcoreException

reddit = praw.Reddit(client_id='Bc7mSjZ3qrApww',
                     client_secret='36i3uR7WIPD5qwLg_UNdBB3K6is',
                     password='****',
                     user_agent='testscript by /u/fakebot3',
                     username='kopo222')

conn = sqlite3.connect('data.db')
c = conn.cursor()


subreddit = reddit.subreddit('all')

for x in reddit.info(['t3_2ydqij']):
    sub = x
    pp.pprint(vars(x))

#Get the updated scores from the site


start = time.time()
inner = 0
count = 0
start = time.time()
endDate = int(sub.created_utc) +1
startDate = 1425273649
with open('newScores1.txt', 'w') as w:
	print(int(sub.created))
        while startDate < endDate or not(startDate == endDate):
            try:
                for submission in subreddit.submissions(end = endDate, start = startDate):
                    count += 1
                    w.write(str(submission.id)+','+str(submission.score)+'\n')
                    endDate = int(submission.created_utc) + 1
                print('Retrieved all posts')
                break
            except PrawcoreException:
                print('Praw exception received, waiting')
                time.sleep(5)
            except KeyboardInterrupt:
                print('Exception received, terminating')
                startDate = 0
                endDate = 0
                break



c.close()
conn.close()
print('\nIt took : ' + str(time.time() - start) + ' to process ' + str(count))