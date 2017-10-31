#!/usr/bin/env python

"""
Project: Log Analysis
Author:  Rohan Kumar
Date:    Oct 28, 2017

---

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
"""

import psycopg2


def main():
    con = None

    try:
        con = psycopg2.connect(host='localhost', dbname='news',
                               user='vagrant', password='udacity')

        cur = con.cursor()

        cur.execute('''SELECT
                          article_title,
                          sum(views) AS views
                        FROM log_view
                        GROUP BY article_title
                        ORDER BY views DESC
                        LIMIT 3;
                     ''')

        print '(1) What are the most popular three articles of all time?'

        for article_title, views in cur.fetchall():
            print '    * "' + article_title + '" - ' + str(views) + ' views'

        cur.execute('''SELECT
                          author_name,
                          sum(views) AS views
                        FROM log_view
                        GROUP BY author_name
                        ORDER BY views DESC;
                     ''')

        print '\n(2) Who are the most popular article authors of all time?'

        for author_name, views in cur.fetchall():
            print '    * ' + author_name + ' - ' + str(views) + ' views'

        cur.execute('''SELECT
                          time :: DATE             AS date,
                          count(nullif(status, '200 OK')) 
                               / count(*) :: FLOAT AS errors
                        FROM log
                        GROUP BY date
                        HAVING count(nullif(status, '200 OK')) 
                               / count(*) :: FLOAT > 0.01;
                     ''')

        print '\n(3) On which days did more than 1% of requests lead to errors?'

        for date, errors in cur.fetchall():
            print('    * {0:%B %d, %Y} - {1:.1%} errors'.format(date, errors))

    except psycopg2.DatabaseError as e:
        print(e)

    finally:
        if con is not None:
            con.close()


if __name__ == "__main__":
    main()
