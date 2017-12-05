import os
import re
import json
import sqlite3
import bball
import datetime


start = datetime.datetime.now()
print("Getting SQL commands...")
sqlCommands = list()
with open('./createTables.sql', 'r') as f:
    sqlCommands.extend(f.read().split(';'))
sqlCommands.reverse()


print("Opening sqlite3 connection... ")
# Open the database connection
conn = sqlite3.connect('nba-insight.db')

# Get a cursor to execute statements
curr = conn.cursor()


def exeSQL(sql, optCommand=None):
    shortened = ' '.join(sql[:60].split())
    print("    SQL:", shortened, "...")
    if optCommand is None:
        return curr.execute(sql)
    else:
        return curr.execute(sql, optCommand)


def exeNextSQL():
    sql = sqlCommands.pop()
    return exeSQL(sql)


# The createPlayerStats table
exeNextSQL()
exeNextSQL()
conn.commit()


with open('../data-loader/output/player-stats.json', 'r') as f:
    data = json.load(f)
    # Using the dictionaries key names as column
    # names and the values as values and inserting
    # data into the database
    # See: https://stackoverflow.com/a/14108554/
    if data:
        # Make the assumption that every JSON object has
        # list of all the columns
        columns = ', '.join(list(data[0].keys()))
        placeholders = ', '.join('?' * len(data[0]))
        insertsql = '''INSERT INTO playerstats  ({}) VALUES ({})'''.format(
            columns, placeholders)

        for row in data:
            curr.execute(insertsql, list(row.values()))

conn.commit()

# The playermatchup table
exeNextSQL()
exeNextSQL()
conn.commit()

uniquePositions = []
for row in exeSQL("SELECT DISTINCT(position) from playerstats"):
    uniquePositions.append(row[0])
print("\tUnique Positions:", len(uniquePositions))

playerPositionsTemplate = dict()
for pos in uniquePositions:
    playerPositionsTemplate[pos] = []

timeCapColumns = ['gameId', 'startTime', 'endTime', 'plusMinusPerMinute']
sides = ['home', 'away']
mainPositions = ['Center', 'Forward1', 'Forward2', 'Guard1', 'Guard2']
for side in sides:
    for pos in mainPositions:
        timeCapColumns.append(side + "Team" + pos + "Id")

columns = ', '.join(timeCapColumns)
placeholders = ', '.join(['?'] * len(timeCapColumns))
timeCapInsertSQL = '''INSERT INTO playermatchup ({}) VALUES ({})'''.format(columns, placeholders)
positionSql = "SELECT position FROM playerstats WHERE playerId = ?"

# RegEx to match timecapsule filenames
timecapsule_filename_regex = re.compile('[0-9]+-[0-9]+-[0-9]+-data\.json')

for filename in os.listdir('../data-loader/output/'):
    if timecapsule_filename_regex.match(filename):
        with open('../data-loader/output/' + filename, 'r') as f:
            data = json.load(f)
            values_dict = dict()
            for side in sides:
                for pos in mainPositions:
                    key = side + "Team" + pos + "Id"
                    values_dict[key] = None
            values_dict["gameId"] = data["gameId"]
            values_dict["startTime"] = data["startTime"]
            values_dict["endTime"] = data["endTime"]
            values_dict["plusMinusPerMinute"] = data["pmPerMinute"]

            # Make sure that IDs are not repeating
            assert(len(set(data["homePlayers"])) == 5)
            assert (len(data["homePlayers"]) == 5)
            assert(len(set(data["awayPlayers"])) == 5)
            assert(len(data["awayPlayers"]) == 5)
            assert(len(set(data["homePlayers"] + data["awayPlayers"])) == 10)

            for side in sides:
                # now go over the home team players and query what
                # their position is and then try to satisfy consts.
                # List of player positions
                playerPositions = {posName: [] for posName in uniquePositions}

                for playerId in data[side + "Players"]:
                    # Query home player and add to player positions
                    for position in curr.execute(positionSql, (playerId, )):
                        for key in list(playerPositions.keys()):
                            if key == position[0].strip():
                                if playerId not in playerPositions[position[0]]:
                                    playerPositions[position[0]].append(playerId)

                # Now solve the constraint satisfaction problem
                bball.playerLineupCSAT(playerPositions)

                # Fill the values dict now
                values_dict[side + "TeamCenterId"] = playerPositions["Center"][0]
                values_dict[side + "TeamForward1Id"] = playerPositions["Forward"][0]
                values_dict[side + "TeamForward2Id"] = playerPositions["Forward"][1]
                values_dict[side + "TeamGuard1Id"] = playerPositions["Guard"][0]
                values_dict[side + "TeamGuard2Id"] = playerPositions["Guard"][1]

                curr.execute(timeCapInsertSQL, list(values_dict.values()))

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
    cols = [tableAlias + "." + cName for cName in columnNames]
    selectColumns.extend(cols)

selectColumns = ', '.join(selectColumns)

timecapsule_view = """
CREATE VIEW IF NOT EXISTS timecapsuleview
AS 
   SELECT """ + selectColumns + """
   , T1.plusMinusPerMinute 
   FROM
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
   INNER JOIN playerstatsnumview as T11 on T11.playerId = T1.awayTeamGuard2Id;
"""

exeSQL(timecapsule_view)
conn.commit()

conn.close()
duration = (datetime.datetime.now() - start)
print("All done! taking ", duration, "seconds")
