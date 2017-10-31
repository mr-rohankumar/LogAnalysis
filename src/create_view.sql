CREATE OR REPLACE VIEW log_view AS
  SELECT
    title AS article_title,
    name  AS author_name,
    views
  FROM articles, authors,
    (SELECT
       path,
       count(*) AS views
     FROM log
     GROUP BY log.path
    ) AS log
  WHERE articles.author = authors.id
        AND '/article/' || slug = path;

ALTER VIEW log_view OWNER TO vagrant;
