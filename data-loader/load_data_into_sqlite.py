from __future__ import print_function
import os
import json
import sqlite3

# Open the database connection
conn = sqlite3.connect('nba-insight.db')

# Get a cursor to execute statements
curr = conn.cursor()

# Drop table if it exists
curr.execute('DROP TABLE IF EXISTS playerstats')

# Create a table if it does not exist for player statistics
create_player_statistics_table = '''
CREATE TABLE IF NOT EXISTS playerstats
(
"playerId" INTEGER PRIMARY KEY,
"playerName" TEXT,
"teamId" INTEGER,
"teamAbbreviation" TEXT,
"age" INTEGER,
"gp" INTEGER,
"w" INTEGER,
"l" INTEGER,
"wPct" REAL,
"min" REAL,
"fgm" REAL,
"fga" REAL,
"fgPct" REAL,
"fG3M" INTEGER,
"fG3A" INTEGER,
"fg3Pct" INTEGER,
"ftm" REAL,
"fta" REAL,
"ftPct" REAL,
"oreb" REAL,
"dreb" REAL,
"reb" REAL,
"ast" REAL,
"tov" REAL,
"stl" REAL,
"blk" REAL,
"blka" REAL,
"pf" REAL,
"pfd" REAL,
"pts" REAL,
"plusMinus" REAL,
"nbaFantasyPts" REAL,
"dD2" INTEGER,
"tD3" INTEGER,
"gpRank" INTEGER,
"wRank" INTEGER,
"lRank" INTEGER,
"wPctRank" INTEGER,
"minRank" INTEGER,
"fgmRank" INTEGER,
"fgaRank" INTEGER,
"fgPctRank" INTEGER,
"fg3mRank" INTEGER,
"fg3aRank" INTEGER,
"fg3PctRank" INTEGER,
"ftmRank" INTEGER,
"ftaRank" INTEGER,
"ftPctRank" INTEGER,
"orebRank" INTEGER,
"drebRank" INTEGER,
"rebRank" INTEGER,
"astRank" INTEGER,
"tovRank" INTEGER,
"stlRank" INTEGER,
"blkRank" INTEGER,
"blkaRank" INTEGER,
"pfRank" INTEGER,
"pfdRank" INTEGER,
"ptsRank" INTEGER,
"plusMinusRank" INTEGER,
"nbaFantasyPtsRank" INTEGER,
"dd2Rank" INTEGER,
"td3Rank" INTEGER,
"cfid" INTEGER,
"cfparams" TEXT,
"position" TEXT);
'''

curr.execute(create_player_statistics_table)

with open('output/player-stats.json','r') as f:
    data = json.load(f)
    # Using the dictionaries key names as column
    # names and the values as values and inserting
    # data into the database
    # See: https://stackoverflow.com/a/14108554/
    if data:
        # Make the assumption that every JSON object has
        # list of all the columns
        columns      = ', '.join(data[0].keys())
        placeholders = ', '.join('?' * len(data[0]))
        insertsql    = '''INSERT INTO {}  ({}) VALUES ({})'''.format("playerstats", columns, placeholders)

        for row in data:
            curr.execute(insertsql, row.values())

conn.commit()



conn.close()
