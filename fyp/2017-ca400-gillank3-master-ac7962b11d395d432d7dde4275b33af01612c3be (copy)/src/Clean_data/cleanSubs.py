import time

# This cleans the subreddit data pulled

def insertSub(sub,header, w):
    #Take all of a subreddits information concatenated into a string
    #It is then split into a list of strings which are variables joined together with str(chr(3))
    #Then for every variable I split them apart on str(chr(3)) and am left with a list of lists of all variables and their corresponding value
    sub = cleanString(sub)
    attr = []
    headerCopy = []
    headerCopy = header[:]
    for head in headerCopy:
        for var in sub:
            #print(headerCopy)
            if var[0].strip() == head.strip():
                #Make sure that its only tabs and newlines I put in
                attr.append(var[1].replace('\t', '').replace('\n',''))
    w.write('\t'.join(attr))
    w.write('\n')

def cleanString(sub):
    sub = sub.split(str(chr(4)))
    newSub = []
    for var in sub:
        newSub.append(var.split(str(chr(3))))
    #To reduce memory requirements I remove all elements from the initial list and return the new one
    del sub[:]
    return newSub

t1 = time.time()
#Split condition between subreddits
split = str(chr(3))+'::'+str(chr(4))
#Insert header to csv
header = ['show_media','_path','over18','created_utc','suggested_comment_sort','hide_ads','description_html','submission_type','public_traffic',
          'quarantine','submit_text_label','key_color','submit_text','_contributor','name','public_description_html','user_sr_theme_enabled',
          '_muted','header_img','created','spoilers_enabled','user_is_banned','_reddit','user_is_contributor','lang','banner_size',
          'submit_text_html','_wiki','url','user_is_muted','collapse_deleted_comments','whitelist_status','_stylesheet',
          '_comments','icon_img','header_size','_banned','_mod','_flair','subscribers','_stream','_fetched',
          'show_media_preview','_quarantine','header_title','banner_img','id','submit_link_label','icon_size','title',
          'display_name_prefixed','description','_moderator','comment_score_hide_mins','user_is_subscriber',
          'wiki_enabled','accounts_active','subreddit_type','_filters','advertiser_category','accounts_active_is_fuzzed',
          'user_is_moderator','display_name','public_description']
with open('cleanedSubs.csv', 'w') as w:
    w.write('\t'.join(header) + '\n')
    count = 0
    with open('combinedSubs.txt', 'r') as r:
        sub = ''
        for variable in r:
            if variable.strip() == split:
                count += 1
                insertSub(sub,header, w)
                sub = ''
            sub= sub + variable

print('it took {} to clean {}'.format(time.time()-t1, count))