# Data analysis
* I have begun analysing the data, as my project is going to be dealing with regression I must identify any collinearity within my data set.
* Independent variables can be described as collinear if they are highly correlated.
* Different variable types need different types of test to determine their independance
    * As I have many categorical variables I have began working with them first.
    * Catagorical variables, specifically nominal variables(variables with no natural ordering, eg. language), require a Chi-Squared test
    * The Chi-Squared test requires the calculation of a expected value matrix.
        * The expected value of a observed variable x is equal to:
        
            `expected_x = (sum(currentCol)/total) * sum(currentRow)`

        * This is then fed into the equation :
        
            `(observed_x - expected_x)^2 / expected_x`
        
        * From here this is done for all x and this produces the Chi-Squared value, if this value is over a certain threshold it can be considered significant
    * As this is quite a time consuming process I want to develop a generic method which can be given two coloumn names and will do this as a time saving measure
    * Once the Chi-Squared is done I will move on to Numeric data
* Once I know which variables are independent i will be able to start building the regression model