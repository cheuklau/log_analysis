#!/usr/bin/env python3
#
# Log_Analysis.py
# Author: Cheuk Lau
# Project: Log Analysis
# Date: 5/16/2018

import psycopg2

# Set the database name
DBNAME = "news"

# Define function for answering question number one:
# What are the most popular three articles of all time?
def question_1():
  ''' Returns the three most popular articles of all time.

  Connect to news database, execute SQL command to find the
  three most popular articles of all time.

  Args:
      None

  Returns:
      The three most popular articles of all time.
  '''

  # Connect to data base
  db = psycopg2.connect(database=DBNAME)

  # Get database cursor
  c = db.cursor()

  # Execute SQL query
  # Strategy:
  # 1) Join articles and log tables on articles.slug contained in log.path.
  # 2) Count the occurrences of each title, and order titles by count.
  # 3) Return the top three articles with the most counts.
  c.execute("select title, count(*) as tot_count \
    from ( select title \
    from articles join log \
    on log.path like '%' || articles.slug || '%') as art_log \
    group by title \
    order by tot_count desc \
    limit 3;")

  # Return cursor results
  return c.fetchall()

  # Close the database
  db.close()

# Define function for answering question number two:
# Who are the most popular article authors of all time?
def question_2():
  ''' Returns a sorted list of authors based on their view count.

  Connect to news database, execute SQL command to create a sorted
  list of authors based on their view count.

  Args:
      None

  Returns:
      Sorted list of authors based on their view count.
  '''

  # Connect to data base
  db = psycopg2.connect(database=DBNAME)

  # Get database cursor
  c = db.cursor()

  # Execute SQL query
  # Strategy:
  # 1) Join articles and log tables on articles.slug contained in log.path.
  # 2) Join author with the result of step 1 on author id.
  # 3) Count the occurrence of each author, and order authors by count.
  # 4) Return the list of authors sorted by count in descending order.
  c.execute("select name, count(*) as tot_count \
    from \
    (( select author \
    from articles join log \
    on log.path like '%' || articles.slug || '%') as art_log \
    join authors \
    on art_log.author = authors.id) as art_log_auth \
    group by name \
    order by tot_count desc;")

  # Return cursor results
  return c.fetchall()

  # Close the database
  db.close()

# Define function for answering question number three:
# On which days did more than 1% of requests lead to errors?
def question_3():
  ''' Returns a sorted list of the error percentage for each day.

  Connect to news database, execute SQL command to create a sorted
  list of the error percentage for each day.

  Args:
      None

  Returns:
      Sorted list of error percentage for each day.
  '''

  # Connect to data base
  db = psycopg2.connect(database=DBNAME)

  # Get database cursor
  c = db.cursor()

  # Execute SQL query
  # Strategy:
  # 1) Join articles and log tables on articles.slug contained in log.path.
  # 2) Join author with the result of step 1 on author id.
  # 3) Count the occurrence of each author, and order authors by count.
  # 4) Return the list of authors sorted by count in descending order.
  c.execute("select date, \
    100.0 * cast(err_cts as float) / cast(tot_cts as float) as per_err \
    from \
    (select date_tot_cts.date, tot_cts, err_cts \
    from \
    (select date, count(*) as tot_cts \
    from (select time::DATE as date, status \
    from log) \
    as date_stat \
    group by date) \
    as date_tot_cts \
    join \
    (select date, count(*) as err_cts \
    from (select time::DATE as date, status \
    from log \
    where status = '404 NOT FOUND') \
    as date_staterr \
    group by date) \
    as date_err_cts \
    on date_tot_cts.date = date_err_cts.date) as date_err_tot_cts \
    order by per_err desc;") 

  # Return cursor results
  return c.fetchall()

  # Close the database
  db.close()

# Main code

# Execute the function to answer the first question
result_1 = question_1()

# Print the results to the first question
print('###################################################################')
print('The three most popular articles of all time are:')
for i in range(0, 3):
  print(result_1[i][0] + ' with ' + str(result_1[i][1]) + ' views')
print('###################################################################\n')

# Execute the function to answer the second question
result_2 = question_2()

# Print the results to the second question
print('###################################################################')
print('The list of authors in descending order based on view counts: ')
for result in result_2:
  print(result[0] + ' with ' + str(result[1]) + ' views')
print('###################################################################\n')

# Execute the function to answer the third question
result_3 = question_3()

# Print the results to the third question
print('###################################################################')
print('The list of error percentage in descending order for each day: ')
for result in result_3:
  print(str(result[0]) + ' had ' + str(result[1]) + '% errors')
print('###################################################################\n')
