import praw
import pprint as pp
from prawcore.exceptions import RequestException, Redirect, Forbidden, NotFound
import time

# Gets time series data
# Pulls 5000 new posts and records their score for
# Several hours tracking their progress


reddit = praw.Reddit(client_id='Bc7mSjZ3qrApww',
                     client_secret='36i3uR7WIPD5qwLg_UNdBB3K6is',
                     password='*****',
                     user_agent='testscript by /u/fakebot3',
                     username='kopo222')


t1 = time.time()
i = 0
waitingCount = 0
start = time.time()
ids = []
hours = 1
variables = ['submission_id', 'time_stamp', 'batch', 'time_obtained', 'created_utc', 'subreddit_id', 'score', 'title', 'title_length', 'domain',
             'num_comments', 'over_18', 'subreddit_name', 'is_self', 'author']
with open('test.csv', 'w') as w:
    w.write('\t'.join(variables) + '\n')
    try:
        while hours < 6:
            waitingCount = 0
            ids = []
            scrapedAt = int(time.time())
            for submission in reddit.subreddit('all').stream.submissions():
            # for submission in reddit.subreddit('all').new():
                try:
                    ids.append(submission.name)
                    variables = [submission.id, 0, hours, scrapedAt, submission.created_utc, submission.subreddit_id, submission.score, submission.title, len(submission.title),
                    submission.domain, submission.num_comments, submission.over_18, submission.subreddit_name_prefixed[2:], submission.is_self, submission.author]
                    w.write('\t'.join([str(var).replace('\t', '').replace('\n', '') for var in variables]) + '\n')
                    if len(ids) > 5000:
                        break
                    waitingCount += 1
                except RequestException:
                    print("RequestException")
                    time.sleep(30)
                except Redirect:
                    print("RedirectException")
                    time.sleep(30)
            print("New batch {} long".format(len(ids)))
            # Follow posts for six hours, checking every 5 minutes and incrementing
            # waitingCount
            # 5/60 = 12  ---> 72/12 == 6
            waitingCount = 1
            while waitingCount < 73:
                try:
                    s = int(time.time())
                    for submission in reddit.info(ids):
			# collect variables to be recorded
                        variables = [submission.id, waitingCount, hours, s, submission.created_utc, submission.subreddit_id, submission.score, submission.title, len(submission.title),
                        submission.domain, submission.num_comments, submission.over_18, submission.subreddit_name_prefixed[2:], submission.is_self, submission.author]
                        w.write('\t'.join([str(var).replace('\t', '').replace('\n', '') for var in variables]) + '\n')

                    # Wait five minutes
                    print("takes : {} -- minute : {}".format(time.time() - s, waitingCount) )
                    time.sleep(300)
                    waitingCount += 1
                except RequestException:
                    print("RequestException")
                    time.sleep(30)
                except Redirect:
                    print("RedirectException")
                    time.sleep(30)
            hours += 1


    except KeyboardInterrupt:
        print('Exception received, terminating')

print("worked for {}".format(hours*6))
print('took : {}'.format(time.time()-start))