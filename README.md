# Log Analysis (UDACITY FULL STACK WEB DEV)

![Icon](https://i.imgur.com/KfXf5jj.png)

## Purpose
A reporting tool (Python 2.x) that prints out reports (in plain text) based on the data in the database. 

The database includes three tables:
1. The articles table includes the articles themselves.
2. The authors table includes information about the authors of articles.
3. The log table includes one entry for each time a user has accessed the site.

The questions the reporting tool answers:
1. What are the most popular three articles of all time? 
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Implementation
For the first and second questions, create view that joins all three tables and projects article title and author name. For your convenience, the reporting tool does this for you.
```
CREATE OR REPLACE VIEW log_view AS
 SELECT
   title AS article_title,
   name  AS author_name
 FROM articles, authors, log
 WHERE articles.author = authors.id
       AND '/article/' || slug = path;
```

After view creation, group by article title and count the number of rows.
```
SELECT
 article_title,
 count(*) AS views
FROM log_view
GROUP BY article_title
ORDER BY views DESC;
```

Likewise, the same can be done for author name. 
```
SELECT
 author_name,
 count(*) AS views
FROM log_view
GROUP BY author_name
ORDER BY views DESC;
```

For the third question, group by date and divide the number of failed HTTP requests by the total number of HTTP requests. The ```count(expression)``` function returns the number of input rows for which the value of expression is not null. The ```nullif(first value, second value)``` function returns a null value if the first value equals the second value; otherwise it returns the first value. By combining two aforementioned functions, we can obtain the number of input rows that does not equals a specified value.

```
SELECT
 time :: DATE                                        AS date,
 count(nullif(status, '200 OK')) / count(*) :: FLOAT AS errors
FROM log
GROUP BY date
HAVING count(nullif(status, '200 OK')) / count(*) :: FLOAT > 0.01;
```

## Instructions
For Ubuntu or similar (e.g. Linux Mint).

### Install PostgresSQL
1. Open terminal
2. Update Repository:   ```sudo apt-get update```
3. Install PostgresSQL: ```sudo apt-get install postgresql postgresql-contrib```

### Configure PostgresSQL
1. Open terminal
2. PostgresSQL CLI: ```sudo -u postgres psql```
3. Create database: ```create database news;```
4. Create user:     ```create user vagrant password 'udacity';```
5. Quit CLI:        ```\q```

### Import Data to Database
1. Open terminal and navigate to a working directory.
2. Download data: ```wget https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip```
3. Unpack data:   ```unzip newsdata.zip```
4. Import data:   ```sudo -u postgres psql -d news -f newsdata.sql```

### Run Reporting Tool
1. Open terminal and navigate to a working directory.
2. Download tool: ```wget https://raw.githubusercontent.com/mr-rohankumar/LogAnalysis/master/src/log_analysis.py```
3. Run tool:      ```python log_analysis.py```

## Output
```
(1) What are the most popular three articles of all time?
    * "Candidate is jerk, alleges rival" - 338647 views
    * "Bears love berries, alleges bear" - 253801 views
    * "Bad things gone, say good people" - 170098 views
    * "Goats eat Google's lawn" - 84906 views
    * "Trouble for troubled troublemakers" - 84810 views
    * "Balloon goons doomed" - 84557 views
    * "There are a lot of bears" - 84504 views
    * "Media obsessed with bears" - 84383 views

(2) Who are the most popular article authors of all time?
    * Ursula La Multa - 507594 views
    * Rudolf von Treppenwitz - 423457 views
    * Anonymous Contributor - 170098 views
    * Markoff Chaney - 84557 views

(3) On which days did more than 1% of requests lead to errors?
    * July 17, 2016 - 2.3% errors
```

## License
```
MIT License

Copyright (c) 2017 Rohan Kumar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
