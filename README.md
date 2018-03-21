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

```
newsdata.sql
```

## Installation

>Clone the repository and move to the project folder:

    $ git clone https://github.com/Joeu/Udacity_Report_Tool

## Creating the views

As the Python code queries against views, you will need to recreate the views to get the report correctly

>Within the newsdata.sql container directory, connect to the database:

    $ psql news

> Connected to the news database, the following commands are strictly necessary

    =>  CREATE VIEW question_1 AS
            SELECT fulltitle.title, views.count
            FROM 
                (SELECT substring(log.path, 10, 10) AS path, count(*) AS count
                FROM log
                WHERE log.method = 'GET' AND log.path LIKE '%/article/%'
                    GROUP BY substring(log.path, 10, 10)
                    ORDER BY count(*) DESC) views
            JOIN 
                (SELECT articles.title,
                replace(lower(replace(replace(articles.title, ' ', '-'), ',', '')), 'there-are-a-lot-of-bears', 'so-many-bears') AS concat_path
                FROM articles) fulltitle
            ON fulltitle.concat_path LIKE (('%' || views.path) || '%');

    =>  CREATE VIEW question_2 AS
            SELECT works.name AS author, sum(question_1.count) AS total_views
            FROM 
                (SELECT authors.name, articles.title
                FROM authors 
                JOIN articles 
                ON authors.id = articles.author) works
            JOIN question_1 
            ON works.title = question_1.title
            GROUP BY works.name
            ORDER BY (sum(question_1.count)) DESC;

    =>  CREATE VIEW question_3 AS
            SELECT result.day, result.not_ok, result.total,
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
