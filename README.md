# NBA Insight

A machine learning tool for predicting which team will win an NBA game and which
players give the best chance of winning.

## Data Loader

The data loader is written in Node.js and utilizes the
[nba](https://www.npmjs.com/package/nba) package to access NBA stats.  You will
need to download the latest version of Node to get started.  Once installed,
navigate to the `data-loader` directory and execute the following commands.

```shell
$ npm install
$ npm run load-player-stats
$ npm run load-game-stats
```

## Database Generator

Once the data has been loaded into data-loader/output, running the script
data-generator/load_data_into_sqlite.py will read all the data and create
a sqlite database with Player Matchup and Player Statistics table and
corresponding views.

```shell
$ python load_data_into_sqlite.py
```

A CSV file containing all the data for all time capsules can be next created
by running query.sql inside sqlite cli.

```shell
$ sqlite3 nba-insight.db
sqlite> .read query.sql
```

You can exit from sqlite3 by pressing `CTRL + C` and the data should be
saved in data.csv file. Each row is an example (timecapsule) with the last
column being the label (plus/minus per minute).


## Team 

* Chidubem Arachie
* Mahesh Narayanamurthi
* Steven Roberts
* Patrick Sullivan

