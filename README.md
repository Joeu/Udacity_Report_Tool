# Database Report Tool

A tool written in Python to retrieve information about a database using SQL statements aiming to andswer Udacity`s project questions.

## Getting Started

The following instructions will get you a copy of the project and, as long as you have the newsdata.sql file, running on your local machine.

### Prerequisites

You will need to have Python and PostgreSQL installed

```
Python 2.7.12
psql (PostgreSQL) 9.5.12
```

And also the database file from Udacity

* [newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

## Installation

>Clone the repository and move to the project folder:

    $ git clone https://github.com/Joeu/Udacity_Report_Tool

## Creating the views

As the Python code queries against views, you will need to recreate the views to get the report correctly

>Within the newsdata.sql container directory, import the database and connect to it:

    $ psql -d news -f newsdata.sql
    $ psql news

> Connected to the news database, the following commands are strictly necessary

    =>  CREATE VIEW question_1 AS
            SELECT articles.title, articles.author, count(*)
                FROM articles JOIN log ON '/article/'||articles.slug LIKE log.path
            GROUP BY articles.title, articles.author
            ORDER BY count DESC;

    =>  CREATE VIEW question_2 AS
            SELECT authors.name, SUM(question_1.count) 
                FROM question_1 JOIN authors ON question_1.author = authors.id 
            GROUP BY authors.name 
            ORDER BY SUM(question_1.count) DESC;

    =>  CREATE VIEW question_3 AS
            SELECT TO_CHAR(result.day,'Mon DD, YYYY'), result.not_ok, result.total,
            (result.not_ok * 100) / result.total::float AS error_perc
            FROM 
                (SELECT date_trunc('day', log."time") AS day,
                sum(CASE WHEN log.status NOT LIKE '%200%' 
                        THEN 1 ELSE 0 END) AS not_ok,
                sum(CASE WHEN log.status LIKE '%200%'
                        THEN 1 ELSE 0 END) AS ok,
                count(*) AS total
                FROM log
                GROUP BY (date_trunc('day', log."time"))
                ORDER BY (date_trunc('day', log."time"))
                ) result
            WHERE (result.not_ok * 100) / result.total::float > 1;

>After creating the views, you can exit the psql

    =>  \q


### Getting the results

>To get the full report, just run the following line, which will executes the python file

    $ python newsdb.py


* The results will be displayed on your terminal
