# Regression

* I began using regression techniques to predict my scores.
* I used several predictors, the key ones being:
    * Subscribers: This is the number of users who subscribe to this particular subreddit meaning it is more vissbible to them
    * media_attached: This is a category which I made, it has ten differnt options including if the post contains an image, video, is over 18 of is just text
    * hour: what hour EST the post was posted
    * is_self: This says wheter the post contains any media or not
    * advertiser_category: what type of advertisments appear on this subreddit
    * lang: This is the language of the subreddit

## Ridge regression

* I started by using ridge regression
* I began using ridge regression as it aims to reduce collinearity among the predictive variables by introducing a bias factor to the variables. 
This is called shrinkage and it is used to reduce the impact predictors have on each other
* It has an adjustable lambda parameter which controls how much the predictors get zeroed out. Researching this it appears that there is no real way to discover the optimal lambda value except through experimentation. I will graph this and try and find what my optimal value is


