-- This is a comment
-- Before running this script, run:
-- sqlite3 nba-insight.db
-- This will put you in sqlite cli
-- Now, run this script as:
-- .read query.sql
-- Based on:
-- https://stackoverflow.com/a/6077039/
-- and:
-- https://stackoverflow.com/a/11643733/
.mode csv
.output data.csv
select * from timecapsuleview;
.output stdout
