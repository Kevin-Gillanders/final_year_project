import praw
import pprint as pp
with open('./password') as f:
    content = f.read()
reddit = praw.Reddit(user_agent='Submission reader',
                      client_id='9yByWqxWzTUd4Q',
                      client_secret='HEFZR_HnywPPssTIViydDUIeoBw')
'''username='kopo222',
                      password=content,
                      app_uri = 'http://www.example.com/unused/redirect/uri'''
#pp.pprint(vars(comment))
subreddit = reddit.submission(id = '5c9uhm')
pp.pprint(vars(subreddit))
print('\n\n\n')
for submission in reddit.subreddit('all').stream.submissions():
        pp.pprint(vars(submission))
        break;
#for submission in subreddit.stream.submissions():
#    pp.pprint(submission)
#
