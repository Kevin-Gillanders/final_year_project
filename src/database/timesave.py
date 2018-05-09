from sklearn.linear_model import Ridge, LinearRegression
import numpy as np
import sqlite3
import time
import pprint as pp
import datetime
import numpy as np
import scipy.stats as sp
import math
import itertools
from multiprocessing import Pool
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import pandas as pd

conn = sqlite3.connect('../../data/data.db')
c = conn.cursor()
startTime = time.time()

scores = []
setData = []

# c.execute('''SELECT st.lang
#              FROM subreddits AS st
#              GROUP BY 1
#              ''')
#
X_int = LabelEncoder()



# ft.score, ft.suggested_sort, ft.secure_media_embed, ft.ups, ft.gilded, ft.spoiler, ft.contest_mode, ft.subreddit_id,
#                     ft.stickied, ft.author, ft.name, ft.media_embed, ft.approved_by, ft.link_flair_css_class, ft.quarantine,
#                     ft.is_self, ft.url, ft.id, ft.distinguished, ft.created, ft._orphaned, ft.removal_reason, ft.over_18,
#                     ft.author_flair_css_class, ft.subreddit, ft.link_flair_text, ft.selftext, ft.hidden, ft.user_reports,
#                     ft.num_reports, ft.title, ft.locked, ft.mod_reports, ft.media, ft.created_utc, ft.edited, ft.num_comments,
#                     ft.domain, ft.secure_media, ft.author_flair_text, ft.banned_by, ft.media_attached, ft.mature, ft.new_score,
#                     ft.cal_date, ft.hour, ft.minute, ft.weekday, ft.agg_score, ft.agg_num_comments, ft.agg_gilded,
#                     st.show_media, st._path, st.over_18, st.created_utc, st.suggested_comment_sort, st.hide_ads, st.submission_type,
#                     st.public_traffic, st.quarantine, st.submit_text_label, st.submit_text, st.subreddit_id, st.created,
#                     st.spoilers_enabled, st.lang, st.banner_size, st._wiki, st.url, st.collapse_deleted_comments, st.whitelist_status,
#                     st.header_size, st.subscribers, st.show_media_preview, st.header_title, st.id, st.submit_link_label, st.icon_size,
#                     st.title, st.display_name_prefixed, st.description, st.comment_score_hide_mins, st.user_is_subscriber, st.wiki_enabled,
#                     st.accounts_active, st.subreddit_type, st.advertiser_category, st.accounts_active_is_fuzzed, st.display_name,
#                     st.public_description, st.agg_subscribers, st.agg_accounts_active, st.agg_comment_score_hide_mins
#
#categories = "ft.score, st.subscribers, ft.is_self, ft.over_18, ft.media_attached, st.agg_accounts_active, ft.weekday, ft.hour, st.submission_type, st.over_18"

categories = "ft.score, ft.gilded, ft.media_embed,  ft.is_self,  ft.over_18, ft.subreddit, ft.media_attached, ft.mature, ft.weekday, ft.hour"

c.execute('''SELECT '''+categories+'''
             FROM posts as ft JOIN subreddits AS st ON st.subreddit_id == ft.subreddit_id
             WHERE ft.score > 10 AND ft.score < 8000
             ''')


for rows in c.fetchall():
    # temp = []
    # for index in range(len(rows)):
    #     if index == 0:
    #         scores.append(rows[index])
    #     else:
    #         temp.append(rows[index])
    setData.append([rows[1], rows[2], rows[3], rows[4], rows[5], rows[6], rows[7], rows[8], rows[9]])
    scores.append(rows[0])

conn.rollback()
c.close()
conn.close()
#print(setData)
labels = np.array(setData)

print("going in")
s = pd.DataFrame(setData, columns = ["ft.gilded", "ft.media_embed","ft.is_self",
"ft.over_18", "ft.subreddit", "ft.media_attached", "ft.mature",
"ft.weekday", "ft.hour"])

setData = pd.get_dummies(s, sparse=True).astype(np.int8)

with open('test.csv', 'w') as w:
    setData.head(20).to_csv('test.csv', sep='\t', encoding='utf-8')





#X_int = LabelEncoder().fit_transform(labels.ravel()).reshape(*labels.shape)
#setData = OneHotEncoder().fit_transform(X_int).toarray()


# training = setData[int(len(scores)*.9):]
# score = scores[int(len(scores)*.9):]
#
# testing = setData[:int(len(scores)*.1)]
# testScore = scores[:int(len(scores)*.1)]    setDat
#
# clf = Ridge(alpha=1.0)
# # clf = LinearRegression()
# clf.fit(training, score)
#
# test = list(clf.predict(testing))
# convert = []
#
#
# print(np.mean((clf.predict(testing) - testScore) ** 2))
#
# for x in test:
#     convert.append(int(x))
#
# #print(convert)
# print("Varience score : {} ".format(clf.score(testing,testScore)))
#
#
# plt.scatter(convert,testScore)
# plt.xlabel('guess')
# plt.ylabel('actual score')
# plt.show()
#
# # for x in zip(test, testScore):
# #     print("{:>7}     |    {}".format(int(x[0]),int(x[1])))
