# Blog 2 15-12-16

## What have I done so far?

1. I pulled ten gigabytes of data from reddit
2. Planned my databases for data storage
3. Looked into which models to use and what other types of analysis I can perform

### 1. I pulled ten gigabytes of data from reddit
* This data was taken over the course of a day.
* It was in a raw format and requires a lot of cleaning 
* Several fairly important things need to be taken from it EG. What type of media accompanies each post, if any
* I am planning on putting the data into a CSV before putting it into a database

### 2. Planned my databases for data storage
* I created a preliminary schema for my database
* This was for my functional spec
* I need to look into how to actually impllement the database
* I plan on using the python 3 module [sqlite3](https://docs.python.org/3/library/sqlite3.html#module-sqlite3)

### 3. Looked into what models to use and what other types of analysis I can preform
* Having discussed this with my supervisor and researched it independently, I believe that my data requires a multivariable regression model
* So I belive ridge regression or lasso might be best suited
