#!/usr/bin/env python3
#
# Log_Analysis.py
# Author: Cheuk Lau
# Project: Log Analysis
# Date: 5/16/2018

import psycopg2

# Set the database name
DBNAME = "news"


def connect(database_name="news"):
    ''' Returns database connection and cursor

    Sets up connection with the database and cursor.

    Args:
        Database name

    Returns:

        database connection and cursor
    '''

    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Error connecting to the database")


def question_1():
    ''' Returns the three most popular articles of all time.

    Connect to news database, execute SQL command to find the
    three most popular articles of all time.

    Args:
        None

    Returns:
        The three most popular articles of all time.
    '''

    # Connect to data base and set up cursor
    db, c = connect()

    # Execute SQL query
    c.execute("SELECT title, count(*) AS tot_count \
    FROM ( SELECT title \
    FROM articles JOIN log \
    ON log.path LIKE '%' || articles.slug || '%') AS art_log \
    GROUP BY title \
    ORDER BY tot_count DESC \
    LIMIT 3;")

    # Return cursor results
    return c.fetchall()

    # Close the database
    db.close()


def question_2():
    ''' Returns a sorted list of authors based on their view count.

    Connect to news database, execute SQL command to create a sorted
    list of authors based on their view count.

    Args:
        None

    Returns:
        Sorted list of authors based on their view count.
    '''

    # Connect to data base and set up cursor
    db, c = connect()

    # Execute SQL query
    c.execute("SELECT name, count(*) AS tot_count \
    FROM \
    (( SELECT author \
    FROM articles JOIN log \
    ON log.path LIKE '%' || articles.slug || '%') AS art_log \
    JOIN authors \
    ON art_log.author = authors.id) AS art_log_auth \
    GROUP BY name \
    ORDER BY tot_count DESC;")

    # Return cursor results
    return c.fetchall()

    # Close the database
    db.close()


def question_3():
    ''' Returns a sorted list of the error percentage for each day.

    Connect to news database, execute SQL command to create a sorted
    list of the error percentage for each day.

    Args:
        None

    Returns:
        Sorted list of error percentage for each day.
    '''

    # Connect to data base and set up cursor
    db, c = connect()

    # Execute SQL query
    c.execute("SELECT date, \
    100.0 * cast(err_cts AS float) / cast(tot_cts AS float) AS per_err \
    FROM \
    (SELECT date_tot_cts.date, tot_cts, err_cts \
    FROM \
    (SELECT date, count(*) AS tot_cts \
    FROM (SELECT time::DATE AS date, status \
    FROM log) \
    AS date_stat \
    GROUP BY date) \
    AS date_tot_cts \
    JOIN \
    (SELECT date, count(*) AS err_cts \
    FROM (SELECT time::DATE AS date, status \
    FROM log \
    WHERE status = '404 NOT FOUND') \
    AS date_staterr \
    GROUP BY date) \
    AS date_err_cts \
    ON date_tot_cts.date = date_err_cts.date) AS date_err_tot_cts \
    ORDER BY per_err DESC;")

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
    print(str(result[0]) + ' had ' + str(round(result[1], 2)) + '% errors')
print('###################################################################\n')
