# "Database code" for the DB News.

import datetime
import psycopg2

DBNAME = "news"

# Function to retrieve full report
# Each query runs againt a previous created view
# The commands to create the views can be find inside the README file


def get_report():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    c.execute("SELECT * from question_1 limit 3")
    most_viwed_articles = c.fetchall()
    c.execute("SELECT * from question_2")
    most_read_authors = c.fetchall()
    c.execute("SELECT * from question_3")
    days_with_erros = c.fetchall()

    db.close()

    # Priting the report to console
    print("The most popular three articles of all time:")
    for article in most_viwed_articles:
        print("* " + article[0] + " - " + str(article[1]) + " views:")
    print("")
    print("The most popular article authors of all time")
    for author in most_read_authors:
        print("* " + author[0] + " - " + str(author[1]) + " views")
    print("")
    print("Days in which more than 1% of requests lead to errors:")
    for day in days_with_erros:
        print("* " + day[0].strftime("%b %d, %Y") +
              " - " + str(round(day[3], 2)) + "% error")


get_report()
