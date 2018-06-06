# Calulating R-values for numeric data
* This is easily enough done and provides a good representation of how likely two sets of numeric variables are to be related
* One annoyance is that most of my data os categorical which can't easily be compared to numerical data

# Comparing numerical and categorical data
* Following consideration of this issue, two methods were investigated:
    * To assign a categorical variable dummy numeric values for example - 
        * The values ('Green', 'Blue', 'Red') could be assigned instead (0, 1, 2)
        * The values can then be assumed numeric and compared to the the actual numeric array
        * The r-value and permutation recorded
        * This is repeated until all permutations have been tested
    * The second method is to try and categorise the numeric variables according to some measure so that they can be placed into categories for comparison to categorical data
* I wrote the former method first it worked well for categories with under 5 options, however past 5 it became very slow and after 8 was essentially unusable.
* This was due to how the program has to work, all possible permutations must be considered, meaning the 
algorithm must do n! permutations; this is impractical. This method may also be unreliable as it involves artifically placing an order on nominal variables. 
So I decided to not rely on this method.
* I began looking into categorising the numeric vales in my dataset so I could compare to the categorical variables using the chi square test.
* Due to the way my data was skewed (Over 1/3 of the data was 0 or one, while the highest value in the set is 18,000), the quartile ranges were a bad way to split the set.
* Looking into the best way to categorise numeric data, a few ways became apparent: making  categories of equal width and frequency binning or using the [freedman-diaconis rule](http://link.springer.com/article/10.1007%2FBF01025868) to decide on what the optimal number of bins was 
* However I still ran into trouble due to the severe skew in the data. Freedman-Diaconis gave back a value 500,000, this was not a realistic number of categories to place the data in.
* Abandoning the freedman-diaconis, I looked at how the data was skewed and decided that I should take the value at the 90th percentile and use that value as a splitting point and repeat this on the remaining data until 1000 items left; this is somewhat similar to logarithmic binning
* With the posts categorised I was able to compare the remainder of my variables to score and my other numeric variables