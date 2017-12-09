import os
import re
import json
import sqlite3
import bball
import datetime

# big SQL queries are now in their own file: createTables.sql
start = datetime.datetime.now()
print("Getting SQL commands...")
sqlCommands = list()
with open('./createTables.sql', 'r') as f:
    sqlCommands.extend(f.read().split(';'))
sqlCommands.reverse()


print("Opening sqlite3 connection... ")
# Open the database connection
conn = sqlite3.connect('nba-insight.db')

def exeSQL(sql, optCommand=None):
    shortened = ' '.join(sql[:60].split())
    print("    SQL:", shortened, "...")
    if optCommand is None:
        return conn.execute(sql)
    else:
        return conn.execute(sql, optCommand)


def exeNextSQL():
    sql = sqlCommands.pop()
    return exeSQL(sql)


# The createPlayerStats table
exeNextSQL()
exeNextSQL()
conn.commit()

with open('../data-loader/output/2016-17/player-stats.json', 'r') as f:
    data = json.load(f)
    # Using the dictionaries key names as column names and the 
    # values as values and inserting data into the database
    # See: https://stackoverflow.com/a/14108554/
    if data:
        # Assume that every JSON object is a list of all the columns
        columns = ', '.join(data[0])
        placeholders = ', '.join('?' * len(data[0]))
        insertsql = '''INSERT INTO playerstats ({}) VALUES ({})'''.format(columns, placeholders)

        for row in data:
            conn.execute(insertsql, list(row.values()))

conn.commit()

uniquePositions = []
for row in exeSQL("SELECT DISTINCT(position) from playerstats"):
    uniquePositions.append(row[0])
print("\tUnique Positions:", len(uniquePositions))

# The playermatchup table
exeNextSQL()
exeNextSQL()
conn.commit()

# RegEx to match timecapsule filenames
timecapsule_filename_regex = re.compile('[0-9]+-[0-9]+-[0-9]+-data\.json')

for filename in os.listdir('../data-loader/output/2016-17/RegularSeason/'):
    if timecapsule_filename_regex.match(filename):
        with open('../data-loader/output/2016-17/RegularSeason/' + filename, 'r') as f:
            data = json.load(f)
            insertVals = dict()
            insertVals["gameId"] = data["gameId"]
            insertVals["startTime"] = data["startTime"]
            insertVals["endTime"] = data["endTime"]
            insertVals["plusMinusPerMinute"] = data["pmPerMinute"]

            # Make sure that IDs are not repeating
            assert len(set(data["homePlayers"])) == 5
            assert len(data["homePlayers"]) == 5
            assert len(set(data["awayPlayers"])) == 5
            assert len(data["awayPlayers"]) == 5
            assert len(set(data["homePlayers"] + data["awayPlayers"])) == 10

            sides = ['home', 'away']
            for side in sides:
                playerPositions = {posName: [] for posName in uniquePositions}

                teamPlayerIds = data[side + "Players"]
                placeholders = ', '.join(["?"] * len(teamPlayerIds))
                whereClause = " WHERE playerId IN ({})".format(placeholders)
                positionSql = "SELECT playerId, position FROM playerstats" + whereClause
                # get the positions of the players...
                for row in conn.execute(positionSql, teamPlayerIds):
                    playerId = row[0]
                    position = row[1]
                    playerPositions[position].append(playerId)

                # Now solve the constraint satisfaction problem
                fixedPositions = bball.getFixedPlayers(playerPositions)

                # Fill the dict now
                insertVals[side + "TeamCenterId"] = fixedPositions["Center"][0]
                insertVals[side + "TeamForward1Id"] = fixedPositions["Forward"][0]
                insertVals[side + "TeamForward2Id"] = fixedPositions["Forward"][1]
                insertVals[side + "TeamGuard1Id"] = fixedPositions["Guard"][0]
                insertVals[side + "TeamGuard2Id"] = fixedPositions["Guard"][1]

            # Now insert the record into the table
            columns = ', '.join(insertVals)
            placeholders = ', '.join('?' * len(insertVals))
            insertsql = '''INSERT INTO playermatchup ({}) VALUES ({})'''.format(columns, placeholders)
            conn.execute(insertsql, list(insertVals.values()))

conn.commit()


# The PlayerStatsNumView table
exeNextSQL()
exeNextSQL()
conn.commit()

# Drop view if it exists
exeSQL('DROP VIEW IF EXISTS timecapsuleview')

columnNames = '''playerId, teamId, age, gp, w, l, wPct, min, fgm, fga, fgPct, fG3M, fG3A, fg3Pct, ftm, fta, ftPct, oreb, dreb, reb, ast, tov, stl, blk, blka, pf, pfd, pts, plusMinus, nbaFantasyPts, dD2, tD3, gpRank, wRank, lRank, wPctRank, minRank, fgmRank, fgaRank, fgPctRank, fg3mRank, fg3aRank, fg3PctRank, ftmRank, ftaRank, ftPctRank, orebRank, drebRank, rebRank, astRank, tovRank, stlRank, blkRank, blkaRank, pfRank, pfdRank, ptsRank, plusMinusRank, nbaFantasyPtsRank, dd2Rank, td3Rank, cfid'''
columnNames = columnNames.split(', ')
columnNames.remove("playerId")
columnNames.remove("teamId")

selectColumns = []
for tableNum in range(2, 12):
    tableAlias = "T" + str(tableNum)
    for cName in columnNames:
        selectColumns.append(tableAlias + "." + cName)
selectColumns.append("T1.plusMinusPerMinute")
selectColumns = ', '.join(selectColumns)

timecapsule_view = """
CREATE VIEW IF NOT EXISTS timecapsuleview
AS
   SELECT """ + selectColumns + """ FROM
   playermatchup as T1
   INNER JOIN playerstatsnumview as T2 on T2.playerId = T1.homeTeamCenterId
   INNER JOIN playerstatsnumview as T3 on T3.playerId = T1.homeTeamForward1Id
   INNER JOIN playerstatsnumview as T4 on T4.playerId = T1.homeTeamForward2Id
   INNER JOIN playerstatsnumview as T5 on T5.playerId = T1.homeTeamGuard1Id
   INNER JOIN playerstatsnumview as T6 on T6.playerId = T1.homeTeamGuard2Id
   INNER JOIN playerstatsnumview as T7 on T7.playerId = T1.awayTeamCenterId
   INNER JOIN playerstatsnumview as T8 on T8.playerId = T1.awayTeamForward1Id
   INNER JOIN playerstatsnumview as T9 on T9.playerId = T1.awayTeamForward2Id
   INNER JOIN playerstatsnumview as T10 on T10.playerId = T1.awayTeamGuard1Id
   INNER JOIN playerstatsnumview as T11 on T11.playerId = T1.awayTeamGuard2Id
"""
exeSQL(timecapsule_view)
conn.commit()

# The playermatchup_testdata table
exeNextSQL()
exeNextSQL()
conn.commit()

for filename in os.listdir('../data-loader/output/2016-17/Playoffs/'):
    if timecapsule_filename_regex.match(filename):
        with open('../data-loader/output/2016-17/Playoffs/' + filename, 'r') as f:
            data = json.load(f)
            insertVals = dict()
            insertVals["gameId"] = data["gameId"]
            insertVals["startTime"] = data["startTime"]
            insertVals["endTime"] = data["endTime"]
            insertVals["plusMinusPerMinute"] = data["pmPerMinute"]

            # Make sure that IDs are not repeating
            assert len(set(data["homePlayers"])) == 5
            assert len(data["homePlayers"]) == 5
            assert len(set(data["awayPlayers"])) == 5
            assert len(data["awayPlayers"]) == 5
            assert len(set(data["homePlayers"] + data["awayPlayers"])) == 10

            sides = ['home', 'away']
            for side in sides:
                playerPositions = {posName: [] for posName in uniquePositions}

                teamPlayerIds = data[side + "Players"]
                placeholders = ', '.join(["?"] * len(teamPlayerIds))
                whereClause = " WHERE playerId IN ({})".format(placeholders)
                positionSql = "SELECT playerId, position FROM playerstats" + whereClause
                # get the positions of the players...
                for row in conn.execute(positionSql, teamPlayerIds):
                    playerId = row[0]
                    position = row[1]
                    playerPositions[position].append(playerId)

                # Now solve the constraint satisfaction problem
                fixedPositions = bball.getFixedPlayers(playerPositions)

                # Fill the dict now
                insertVals[side + "TeamCenterId"] = fixedPositions["Center"][0]
                insertVals[side + "TeamForward1Id"] = fixedPositions["Forward"][0]
                insertVals[side + "TeamForward2Id"] = fixedPositions["Forward"][1]
                insertVals[side + "TeamGuard1Id"] = fixedPositions["Guard"][0]
                insertVals[side + "TeamGuard2Id"] = fixedPositions["Guard"][1]

            # Now insert the record into the table
            columns = ', '.join(insertVals)
            placeholders = ', '.join('?' * len(insertVals))
            insertsql = '''INSERT INTO playermatchup_testdata ({}) VALUES ({})'''.format(columns, placeholders)
            conn.execute(insertsql, list(insertVals.values()))

conn.commit()

# Drop view if it exists
exeSQL('DROP VIEW IF EXISTS timecapsuleview_testdata')

columnNames = '''playerId, teamId, age, gp, w, l, wPct, min, fgm, fga, fgPct, fG3M, fG3A, fg3Pct, ftm, fta, ftPct, oreb, dreb, reb, ast, tov, stl, blk, blka, pf, pfd, pts, plusMinus, nbaFantasyPts, dD2, tD3, gpRank, wRank, lRank, wPctRank, minRank, fgmRank, fgaRank, fgPctRank, fg3mRank, fg3aRank, fg3PctRank, ftmRank, ftaRank, ftPctRank, orebRank, drebRank, rebRank, astRank, tovRank, stlRank, blkRank, blkaRank, pfRank, pfdRank, ptsRank, plusMinusRank, nbaFantasyPtsRank, dd2Rank, td3Rank, cfid'''
columnNames = columnNames.split(', ')
columnNames.remove("playerId")
columnNames.remove("teamId")

selectColumns = []
for tableNum in range(2, 12):
    tableAlias = "T" + str(tableNum)
    for cName in columnNames:
        selectColumns.append(tableAlias + "." + cName)
selectColumns.append("T1.plusMinusPerMinute")
selectColumns = ', '.join(selectColumns)

timecapsule_view = """
CREATE VIEW IF NOT EXISTS timecapsuleview_testdata
AS
   SELECT """ + selectColumns + """ FROM
   playermatchup_testdata as T1
   INNER JOIN playerstatsnumview as T2 on T2.playerId = T1.homeTeamCenterId
   INNER JOIN playerstatsnumview as T3 on T3.playerId = T1.homeTeamForward1Id
   INNER JOIN playerstatsnumview as T4 on T4.playerId = T1.homeTeamForward2Id
   INNER JOIN playerstatsnumview as T5 on T5.playerId = T1.homeTeamGuard1Id
   INNER JOIN playerstatsnumview as T6 on T6.playerId = T1.homeTeamGuard2Id
   INNER JOIN playerstatsnumview as T7 on T7.playerId = T1.awayTeamCenterId
   INNER JOIN playerstatsnumview as T8 on T8.playerId = T1.awayTeamForward1Id
   INNER JOIN playerstatsnumview as T9 on T9.playerId = T1.awayTeamForward2Id
   INNER JOIN playerstatsnumview as T10 on T10.playerId = T1.awayTeamGuard1Id
   INNER JOIN playerstatsnumview as T11 on T11.playerId = T1.awayTeamGuard2Id
"""
exeSQL(timecapsule_view)
conn.commit()

conn.close()
duration = (datetime.datetime.now() - start)
print("All done! taking ", duration, "seconds")
