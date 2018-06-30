# Log Analysis

Author: Cheuk Lau

Date: 5/16/2018

In this project, we are working with a newspaper site which consists of
the user-facing front-end, and the database behind it. We need to build 
an internal reporting tool that uses information from the database to 
discover certain trends about the site's readers.

The database contains newspaper articles and web server logs for the 
site. The log has a database row for each time a reader loaded a web 
page.

The python program we write will run from the command line. It will connect
to the database, use SQL queries to analyze the log data, and print
out the answers to the following questions:

1) What are the most popular three articles of all time?

2) Who are the most popular article authors of all time?

3) On which days did more than 1% of requests lead to errors?

# Software Dependencies
To run the program, you need Python and PostgreSQL. Information for obtaining
both are provided below:

-Python (https://www.python.org/downloads/)

-PostgreSQL (https://www.postgresql.org)

# Compilation Instructions
The site's data is provided in [newsdata.sql](https://tinyurl.com/y9p554lu). 

Run the following command:
```
psql -d news -f newsdata.sql
```
The above command executes PostgreSQL to run the SQL statements in 
newsdata.sql, which creates the news database. The news database
includes three tables:

- authors: information about authors of articles

- articles: articles themselves

- log: one entry for each time a user accessed the site

After creating the news database, run the python code:
```
python log_analysis.py
```
The python code will connect to the news database, use SQL queries to 
analyze the data, and display the requested trends.