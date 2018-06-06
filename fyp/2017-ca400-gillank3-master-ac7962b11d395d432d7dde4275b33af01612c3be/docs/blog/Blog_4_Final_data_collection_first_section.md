# Collected Scores and subreddits 21/02/2017

## New Scores

* Reddit, in the time between scraping my first month of data and now, have [updated](https://www.reddit.com/r/announcements/comments/5gvd6b/scores_on_posts_are_about_to_start_going_up/) their scoring algorithm. I feel that this could lead to some interesing analysis. This could have an effect on how my model works and it will be interesting to see if this would have had a large impact or any impact at all.

* I collected the new scores, Reddits server was dropping my connection so I added in some error handling

* I have the new scores and need to add the scores to the database

## Subreddits

* I also think that there is good data to be had on the subreddits. So I also scraped these too as was part of my functional spec.

* I got all the unqiue subs which users had posted on in my database. They totalled ~55000. Some of the subreddits have since been deleted or made private so I had to catch a lot of errors which came from this.
I will have to figure out how to deal with the posts which now no longer have information. I may remove these posts but I am not sure yet.
    * I kept track of all of these missing subs so I will know which will cause problems in the future

