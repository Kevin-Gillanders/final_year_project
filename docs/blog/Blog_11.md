# Controls
* Wanting to validate the predictive power of my model, I created a control to base any possible improvements on
* My control was based off of a [previous papers control](http://cs229.stanford.edu/proj2012/ZamoshchinSegall-PredictingRedditPostPopularity.pdf) which suggested using the 'median score of all posts within the dataset' which was 3
* I felt that this was not granular enough, but agreed with the general idea. So I made my control the median score per subreddit. For example, funny has 15 and askreddit has 80. This gives the control more accuracy and a better chance of being correct.


# Filtering and sampling
* I used several different criteria to filter data from my database and depending on the method used I got vastly different reults
    * No filtering: 
        * I took posts from the database with no bias
        * This meant that the training/test set was mostly composed of posts with a low score
        * This produced a small but consistent improvement over guessing the average
    * Fitering on score:
        * I felt that there were too many unpopular posts (Below 50) in the dataset. 
        * So to get a better prediction of popularity I decided that fitering the score might be a good idea.
        * The idea was to allow the model the chance to learn what a good post is. 
    * Filtering on comments:
        * Based on the previous filtering which provided an increase in R^2 score I felt another way to filter on popularity was to look at the number of comments it recieved
        * This gave a faily good result
    * Under sampling my data, to produce a more balanced view:
        * I began reading into how to deal with the severe skew in the data 
        * Under Sampling is a technique to adjust the distribution of classes within a dataset, used when there is unbalanced amount of one class
        * Using my now aggregated score as a guide I selected 5000 posts at random from each section
        * This produced perhaps my most successful result, however it is hard to test due to the small number of posts with a high score and taking from the dataset without rrplacement. 
This meant that their were very actual high scoring test cases from the model to 
        * This method however, alters the prior probability of the the data and the model doesn't encorporate the correct probablities, that 0 and 1 is disproportionality represented in the data, into the model.
* The methods highlighted an issue with my dataset, a lack of testing data, for future work I should scrape an extra month and use it as the test set