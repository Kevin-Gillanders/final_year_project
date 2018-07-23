# Chi-Squared test
* Due to limitations of the Chi-Square test in pythons libraries I have coded most of the function myself.
* I have got the Chi-Square to work on my data set in a general way, such that, I can feed the method a list of coloumns names and it will calculate the score and print it to a csv file
* The p-values I am getting look okay for the subreddits table but are mostly 0 for the posts table. I must look into this

# Limitations of Chi-Square
* The Chi-Square test is [sensetive](https://learn.bu.edu/bbcswebdav/pid-826908-dt-content-rid-2073693_1/courses/13sprgmetcj702_ol/week05/metcj702_W05S02T05_limitations.html) to the the sample size, with the significance of even weak associations artifically inflated at large sample sizes. As my sample size for post is over three million this is likely the cause of the problem
* Upon further reading I found a [paper](https://www.ncbi.nlm.nih.gov/pubmed/23894860) detailing this problem. They recommend in addition to the Chi-Square test, to use 
 a method of identifying assocation, based on the Chi-Square test called [Cramer's V](https://en.wikipedia.org/wiki/Cram%C3%A9r%27s_V)
* This is not in a python library like numpy or scipy, so I will code it myself