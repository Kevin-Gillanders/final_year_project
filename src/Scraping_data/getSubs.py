import praw
import pprint as pp
from threading import Thread
from prawcore.exceptions import RequestException, Redirect, Forbidden, NotFound
import time

# Goes through csv of data and looks up every subreddit that was mentioned
# The subreddit data is then scraped and put into a seperate csv

reddit = praw.Reddit(client_id='Bc7mSjZ3qrApww',
                     client_secret='36i3uR7WIPD5qwLg_UNdBB3K6is',
                     password='****',
                     user_agent='testscript by /u/fakebot3',
                     username='kopo222')

read = True
t1 = time.time()
i = 0
waitingCount = 0
with open('subs.txt', 'r') as r:
    with open('subDetails.txt', 'w') as w:
        with open('unavailableSubs.txt', 'w') as f:
            subreddits = r.readlines()
            for i in range(0, len(subreddits)):
                try:
		    # Done this way to stop request excetions from skipping
		    # over any item in the list
		    # Once data collected with no issue, read is flipped to false
                    if read:
                        read = False
                        sub = subreddits[i]
                        i += 1
                    sub = sub.strip()
                    subreddit = reddit.subreddit(sub)
                    subreddit.description
                    x = vars(subreddit)
                    #pp.pprint(type(x))
                    for key, value in x.items() :
                    	# Delimiting characters are added inbetween content to make it easier to split them later
                        if value is None:
                            val = str(key).replace(str(chr(3)), '').replace(str(chr(4)), '').replace('\n', '') + str(chr(3)) + 'None' + str(chr(4))
                        else:
                            val = str(key).replace(str(chr(3)), '').replace(str(chr(4)), '').replace('\n', '') + str(chr(3)) + str(value).replace(str(chr(3)), '').replace(str(chr(4)), '').replace('\n', '') + str(chr(4))
                        w.write(val)
                    read = True
                    w.write('\n' + str(chr(3))+'::'+str(chr(4))+'\n')
                except Redirect:
                    #Catch subreddits which have been deleted
                    #which are no longer available
                    read = True
                    f.write('Redirect: ' + str(sub))
                    print('Redirect: {}'.format(subreddit.display_name))

                except Forbidden:
                    #Catch subreddits which have been made private
                    #which are no longer available
                    read = True
                    f.write('Forbidden: ' + str(sub))
                    print('Forbidden: {}'.format(subreddit.display_name))

                except NotFound:
                    #Catch subreddits which have been deleted
                    #which are no longer available
                    read = True
                    f.write('NotFound: ' + str(sub))
                    print('NotFound: {}'.format(subreddit.display_name))

                except RequestException:
                    # Decrement i so the for loop goes back to read the same item again
                    # not missing anything
                    i -= 1
                    read = False
                    waitingCount += 1
                    print('Praw exception: {} received, waiting'.format(waitingCount), end = '')
                    print(subreddit.display_name)
                    time.sleep(5)

                except KeyboardInterrupt:
                    print('Exception received, terminating')
                    break

t2 = int(time.time() - t1)
print('it took {} to process {}  up to {}'.format(t2, i,subreddit.display_name) )