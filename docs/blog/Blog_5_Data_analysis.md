# Data analysis 21/2/2017

* I have started looking into how I will analyse my data. I need to start getting correlations between data points. I have roughly nine possibly useful variables and one variable \(scores\) which is my dependant variable.
* There are 3 numeric variables, 5 categorical variables and 2 binary variables in my dataset. This is just on the submissions, I have not got around to looking at the subreddit data yet, but I imagine that that will have more useful
 information.
*  [Different variable types require different types of correlation analysis](http://www-users.cs.umn.edu/~ludford/stat_overview.htm):
    * Numeric vs. Numeric: correlation coefficient 
    * Categorical variables are broken into two seperate classes:
        * Nominal: Variables which are just labels and have no natural ordering eg. (Media_attached)
        * Ordinal: A variable which has a natural ordering eg. Time of day
    * Nominal vs Nominal: This requires a [Chi-Squared test](https://en.wikipedia.org/wiki/Chi-squared_test), which will give me a p-value
        * A p-value is the probability that two variables are NOT related given the data observed, a p-value under 0.05 \(p-value < 0.05\) is the typical cut off for significance
    * Nominal vs Numeric: I believe that this will require an [ANOVA](https://en.wikipedia.org/wiki/F-test) test (I should discuss this with Marija). Which is an analysis of variance 
    * Ordinal vs Ordinal: I beleive that this requires a [Wilcoxon Test](https://en.wikipedia.org/wiki/Wilcoxon_signed-rank_test)\(Data must be paired\) or a [Mann Whitney test](https://en.wikipedia.org/wiki/Mann%E2%80%93Whitney_U_test)
    * Binary categorical variables can be taken as 1 and 0, they can then bee assumed to be numeric
* Finding correlations between independant variables lets me know that both shouldn't be included in the analysis as they can skew results
    * Independant variables with a high correlation may uncover some interesting dependancies which I can follow up on
* Variables which have a high correlation with the score \(My predictor\) will be more useful when it comes to trying to predict the score
* **What I need to do?** 
    * I must work out what variables are associated with the score but are independent of each other.
    * These variables will be included in my model for the popularity prediction
    * I should also look for interesting associations between my variables eg. (do posts with media attached get more comments? Are mature posts generally posted at night?)
    * These insights I get can be used to for the data analytics side of my project