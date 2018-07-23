# -*- coding: utf-8 -*-
import praw
import time
#This version of praw(3.6) is now out of date
#I am planning to use the more modern version from now on


# This was a very early version of scraping, the output of which was not cleaned
# at all. Just placed into a file. I am keeping this file here as the output of 
# this program was used as reddit updated their scoring system and I had to clean it

start = time.time()
r = praw.Reddit('Scraping data')
submissions = praw.helpers.submissions_between(r, 'all',lowest_timestamp=1420070400, highest_timestamp=1427846400, verbosity = 0)
count = 0
with open('posts.csv', 'w') as f:
    for post in submissions:
        post = str(vars(post)).encode('utf-8')
        if count == 0:
            end = time.time()
            print('it took : ' + str(end - start ))
            start = time.time()
        elif count % 100000 == 0:
            end = time.time()
            print('it took : ' + str(end - start ))
            print('to process : ' + str(count))
        count += 1
        f.write(str(post) + '\n\n\n')
end = time.time()
print('\n\n\n\n\n\n::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n\n\n\n\n')
print('Processed : ' + str(count) + '\n')
print('It took : ' + str(end - start ) + 'to complete')
