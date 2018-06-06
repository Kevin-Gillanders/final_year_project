# Time series data

* As per my functional spec I pulled time series data
* I pulled 5000 new posts and recorded their score every five minutes for 6 hours, I then pulled 5000 more new posts and started again
* Originally in my functional spec I discussed doing this over the course of several weeks, however due to time and storage constraints I wasn't able to do this for as long as intended
* I was able to scrape data for around two days however, leaving me 25000 unique posts which scores I had tracked and is somewhat similar to a method proposed by [second paper](https://www.aaai.org/ocs/index.php/ICWSM/ICWSM15/paper/view/10598)
* The aim of doing this was to try and find was there a critical point, where if aa post has x score by y minute it would get popular
* I believe that this method could work and could be quite predictive however I was unable to obtain enough data to conclusively say one way or another on the issue
* If I were to further investigate this problem I would definitely pursue this line of enquiry, by collecting more data

# What did this show?

![time series graph](https://gitlab.computing.dcu.ie/gillank3/2017-ca400-gillank3/raw/master/docs/blog/images/time_series_plot_grid_all.png)

* From the graph above we can very clearly see that some of the posts spike up in popularity over a very short amount of time, then all of a sudden they no longer rise, I believe this spike in popularity is caused by making it to the front page
where the post is at its most visible. The sudden drop in popularity is caused by dropping off the front page, no clear cut time could be established for the post to have gained traction by
* Majority are still very low however