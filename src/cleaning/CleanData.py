import string
import pprint as pp
import re
from enum import Enum
import time


class Media(Enum):
	#classify every post
	none = 1
	video = 2
	image = 3
	social_media = 4
	article = 5

	mature = 6
	mature_none = 7
	mature_video = 8
	mature_image = 9
	mature_social_media = 10

	def __lt__(self, other):#implementing a comparision method for the enumerator
		if self.__class__ is other.__class__:
			return self.value < other.value
		return NotImplemented

def cleanList(row):
	#removing slashes, single quotes, commas, etc
	row[0] = row[0].replace('\\','').replace('\'', '').replace('\"', '').replace('\t','').replace('b{','')
	row[1] = row[1].replace('\\','').replace('\'', '').replace('\"', '').replace('\t','').replace('{','').replace('}','').replace('[','').replace(']','').strip()

def oldmediaCheck(line):
	#This has been replaced
	if not('type\\\': \\\'video\\\'' in line or any("{\'images\': " in s for s in line) or any("{\\'images\\': " in s for s in line)):
		return Media.none
	#This line identifies videos
	#also takes gifs as being videos
	elif(( 'type\\\': \\\'video\\\'' in line) or any('\'https://youtu.be/' in s for s in line)):
		return Media.video
	#This finds if any post
	#has an image associated with it
	elif any("{\'images\': " in s for s in line) or any("http://imgur.com" in s for s in line):# and not ('type\\\': \\\'video\\\'' in line)):
		return Media.image
	elif any("{\\'images\\': " in s for s in line):# and not ('type\\\': \\\'video\\\'' in line)):
		return Media.article
	return Media.none


def mediaCheck(domainCell):
	# 1) If self in title then none
	# 2) The big video sites are matched using regular expressions
	# 3) Do the same for the big image sites, imgur, flickr etc
	# 4) Other social media sites are checked and put into their own catagory
	# 5) If above are comprehensive enough i can put stuff I don't know in articles
	domainCell = domainCell.lower()
	if media_attached == Media.none:
		if reg_self.match(domainCell):
			return Media.none
		#This line identifies videos
		#also takes gifs as being videos
		elif reg_vid.match(domainCell):
			return Media.video
		#This finds if any post
		#has an image associated with it
		elif reg_img.match(domainCell):
			return Media.image
		#If any post is from another social media site
		elif reg_soc_med.match(domainCell):
			return Media.social_media
		else:# and not ('type\\\': \\\'video\\\'' in line)):
			return Media.article

	elif media_attached == Media.mature:
		if reg_self.match(domainCell):
			return Media.mature_none
		#This line identifies videos
		#also takes gifs as being videos
		elif reg_vid.match(domainCell):
			return Media.mature_video
		#This finds if any post
		#has an image associated with it
		elif reg_img.match(domainCell):
			return Media.mature_image
		#If any post is from another social media site
		elif reg_soc_med.match(domainCell):
			return Media.mature_social_media
		else:# and not ('type\\\': \\\'video\\\'' in line)):
			return Media.mature
	else:
		return Media.none

reg_self = re.compile('self\..*$')#starts with self. follwed by anything, no media
reg_vid = re.compile('(m\.)?(youtu|vimeo|twitch|periscope|dailymotion|liveleak|vine).*$')#optional m. then youtube twitch vimeo etc
reg_img = re.compile('(i\.)?(imgur|flickr|gfycat|puu|imgflip|twitpic|picasa|photobucket).*$')# image sites
reg_soc_med = re.compile('.*(twitter|tumblr|instagram|facebook|linkedin|pinterest|vk).*$')#social media


# uses non consuming lookahead assertion, to match ", 'any_words': "
reg_split_no_esc = re.compile(', \'(?=\w*\': )')
reg_split_esc = re.compile(r", \'(.*\': )")

count = 0#keeps track of the amount of items added
innerCount = 0#Aligns the csv
attr = [] #Collects all lines before putting them in the CSV
media_attached = 0
with open('./data/posts.csv') as r:
	with open('./data/Cleaned.csv', 'w') as w:
		cols = ['reddit_session','_info_url','_uniq','suggested_sort','secure_media_embed',
		'ups','gilded','_comment_sort','likes','_replaced_more','spoiler','contest_mode',
		'report_reasons','_params','subreddit_id','stickied','author','name','selftext_html',
		'downs','media_embed','approved_by','link_flair_css_class','quarantine','is_self','url',
		'archived','id','_has_fetched','_comments_by_id','distinguished','created','_orphaned',
		'removal_reason','over_18','thumbnail','author_flair_css_class','clicked','subreddit',
		'link_flair_text','hide_score','_api_link','permalink','selftext','hidden','user_reports',
		'num_reports','score','_comments','title','locked','json_dict','mod_reports','media',
		'created_utc','edited','num_comments','domain','secure_media','visited','saved',
		'author_flair_text','banned_by','_underscore_names','media_attached','mature']

		w.write('\t'.join(cols) + '\n')
		start = time.time()
		for line in r:

			#Deletes all variables from memory
			del attr[:]

			#If loop is white space
			#Go to next iteration of loop
			if line.isspace():
				continue

			line = line.replace('\\n', '')
			#The ' are escaped when media eg images is attached
			#So need to different split conditions

			#comma space single quote aynting till first backslash which has to be followed by a colon
			#unreliable
			line = line.replace('\\', '')
			if ', \\\'' in line:#When no media is attached to the post
				line = re.split(reg_split_esc, line)

			elif ', \'' in line:#When media is attached
				line = re.split(reg_split_no_esc, line)


			media_attached = Media.none


			for x in line:
				if '\\\':' in x:
					x = x.split('\\\':')
				else:
					x = x.split('\':')

				#cleans list item
				cleanList(x)


				if x[0] == cols[innerCount]:
					innerCount += 1
					if len(x[1]) == 0:
						attr.append('None')
					else:
						attr.append(x[1])
				if x[0] == 'over_18':
					if x[1] == 'True':
						#maybe make this a different coloumn
						 media_attached = Media.mature
				if x[0] == 'domain':
					media_attached = mediaCheck(x[1])

			#Append media_attached to end of list
			attr.append(media_attached.name)
			#16 and 38 correspond to username and subreddit
			#Both have superflous information surrounding them removing this
			attr[16] = attr[16][19:-1]
			attr[38] = attr[38][25:-1]
			#media is mature or not
			if media_attached.value < 6:
				attr.append('Safe')
			else:
				attr.append('Mature')
			w.write('\t'.join(attr) + '\n')
			count += 1
			innerCount = 0
		end = time.time()
		print('It took : ' + str(end - start) + 'to run %d' % (count))
