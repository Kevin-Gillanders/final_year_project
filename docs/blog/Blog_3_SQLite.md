# What version of SQL am I going to use?
* After reviewing the [Official SQLite documentaion](http://www.sqlite.org/whentouse.html) I have decided that it is the most approiate choice
for my project. It is a light weight library, which has all of the functionality which I require.

* I  briefly considered using MySQL. However after reviewing the [documentation](https://dev.mysql.com/doc/connector-python/en/) I feel that a lot of the functionality was unecessary for my project. For example I don't require
any of the server side functionality, which would most likely end up getting in the way.

* As my data is under 6 gigs I can easily accomodate it on my laptop. Portability is a secondary consideration, but as SQLite keeps the .db file
to a single file I can move it to an external drive if necessary, which is good for keeping backups.
