import praw
import time
import pprint as pp
import sqlite3
import multiprocessing as mp

def getData(submission):
    #q.put((str(submission.id)+','+str(submission.score)+'\n'))
    return str(submission.id)+','+str(submission.score)+'\n'

def getData_init(q):
    getData.q = q

reddit = praw.Reddit(client_id='Bc7mSjZ3qrApww',
                     client_secret='36i3uR7WIPD5qwLg_UNdBB3K6is',
                     password='grandtheftauto',
                     user_agent='testscript by /u/fakebot3',
                     username='kopo222')

conn = sqlite3.connect('data.db')
c = conn.cursor()

manager = mp.Manager()
q = mp.Queue()
p = mp.Pool()#(None, getData_init, [q]))

subreddit = reddit.subreddit('all')
#Get the earlist and latest post
c.execute("SELECT min(created), max(created) FROM post")
rows = c.fetchone()
#.submissions takes two unix timestamps(early, oldest)
submissions = subreddit.submissions(rows[0], rows[1])
start = time.time()
count = 0
with open('newScores1.txt', 'w') as w:
    #try process
    for result in p.imap(getData, submissions):
        count += 1
        w.write(result)
        if count > 2000:
            break


'''p.map(getData, submissions)
    p.close()
    p.join()
    w.write(q.get())'''



print('it took : ' + str(time.time() - start))
