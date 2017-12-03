
import os
import re
import json
import sqlite3


def playerLineupCSAT(playerPositions):
    """
    Accepts a dictionary with the following keys
    playerPositions                     = dict()
    playerPositions['Guard']            = []
    playerPositions['Center']           = []
    playerPositions['Forward']          = []
    playerPositions['Forward-Center']   = []
    playerPositions['Center-Forward']   = []
    playerPositions['Forward-Guard']    = []
    playerPositions['Guard-Forward']    = []
    playerPositions['']                 = []
    """
    # Remove excess players
    if len(playerPositions['Forward']) > 2:
        playerPositions[''].extend(playerPositions['Forward'][2:])
        del playerPositions['Forward'][2:]
                
    if len(playerPositions['Center']) > 1:
        playerPositions[''].extend(playerPositions['Center'][1:])
        del playerPositions['Center'][1:]

    if len(playerPositions['Guard']) > 2:
        playerPositions[''].extend(playerPositions['Guard'][2:])
        del playerPositions['Guard'][2:]
                
    # Add players as needed
    while len(playerPositions['Forward']) < 2 and len(playerPositions['Forward-Center']) > 0:
        playerPositions['Forward'].append(playerPositions['Forward-Center'].pop())
                
    while len(playerPositions['Forward']) < 2 and len(playerPositions['Forward-Guard']) > 0:
        playerPositions['Forward'].append(playerPositions['Forward-Guard'].pop())

    while len(playerPositions['Center']) < 1  and len(playerPositions['Center-Forward']) > 0:
        playerPositions['Center'].append(playerPositions['Center-Forward'].pop())

    while len(playerPositions['Guard']) < 2  and len(playerPositions['Guard-Forward']) > 0:
        playerPositions['Guard'].append(playerPositions['Guard-Forward'].pop())

    while len(playerPositions['Forward']) < 2  and len(playerPositions['Center-Forward']) > 0:
        playerPositions['Forward'].append(playerPositions['Center-Forward'].pop())

    while len(playerPositions['Forward']) < 2  and len(playerPositions['Guard-Forward']) > 0:
        playerPositions['Forward'].append(playerPositions['Guard-Forward'].pop())

    while len(playerPositions['Center']) < 1 and len(playerPositions['Forward-Center']) > 0:
        playerPositions['Center'].append(playerPositions['Forward-Center'].pop())
                
    while len(playerPositions['Guard']) < 2 and len(playerPositions['Forward-Guard']) > 0:
        playerPositions['Guard'].append(playerPositions['Forward-Guard'].pop())

    # Now pop everything into the empty key list
    playerPositions[''].extend(playerPositions['Forward-Center'])
    del playerPositions['Forward-Center'][0:]
    playerPositions[''].extend(playerPositions['Forward-Guard'])
    del playerPositions['Forward-Guard'][0:]
    playerPositions[''].extend(playerPositions['Center-Forward'])
    del playerPositions['Center-Forward'][0:]
    playerPositions[''].extend(playerPositions['Guard-Forward'])
    del playerPositions['Guard-Forward'][0:]

    while len(playerPositions['Forward']) < 2 and len(playerPositions['']) > 0:
        playerPositions['Forward'].append(playerPositions[''].pop())

    while len(playerPositions['Center']) < 1  and len(playerPositions['']) > 0:
        playerPositions['Center'].append(playerPositions[''].pop())
                
    while len(playerPositions['Guard']) < 2  and len(playerPositions['']) > 0:
        playerPositions['Guard'].append(playerPositions[''].pop())

    assert(len(playerPositions['Forward']) == 2)
    assert(len(playerPositions['Center'])  == 1)
    assert(len(playerPositions['Guard'])   == 2)



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
"playerId"           INTEGER PRIMARY KEY,
"playerName"         TEXT,
"teamId"             INTEGER,
"teamAbbreviation"   TEXT,
"age"                INTEGER,
"gp"                 INTEGER,
"w"                  INTEGER,
"l"                  INTEGER,
"wPct"               REAL,
"min"                REAL,
"fgm"                REAL,
"fga"                REAL,
"fgPct"              REAL,
"fG3M"               INTEGER,
"fG3A"               INTEGER,
"fg3Pct"             INTEGER,
"ftm"                REAL,
"fta"                REAL,
"ftPct"              REAL,
"oreb"               REAL,
"dreb"               REAL,
"reb"                REAL,
"ast"                REAL,
"tov"                REAL,
"stl"                REAL,
"blk"                REAL,
"blka"               REAL,
"pf"                 REAL,
"pfd"                REAL,
"pts"                REAL,
"plusMinus"          REAL,
"nbaFantasyPts"      REAL,
"dD2"                INTEGER,
"tD3"                INTEGER,
"gpRank"             INTEGER,
"wRank"              INTEGER,
"lRank"              INTEGER,
"wPctRank"           INTEGER,
"minRank"            INTEGER,
"fgmRank"            INTEGER,
"fgaRank"            INTEGER,
"fgPctRank"          INTEGER,
"fg3mRank"           INTEGER,
"fg3aRank"           INTEGER,
"fg3PctRank"         INTEGER,
"ftmRank"            INTEGER,
"ftaRank"            INTEGER,
"ftPctRank"          INTEGER,
"orebRank"           INTEGER,
"drebRank"           INTEGER,
"rebRank"            INTEGER,
"astRank"            INTEGER,
"tovRank"            INTEGER,
"stlRank"            INTEGER,
"blkRank"            INTEGER,
"blkaRank"           INTEGER,
"pfRank"             INTEGER,
"pfdRank"            INTEGER,
"ptsRank"            INTEGER,
"plusMinusRank"      INTEGER,
"nbaFantasyPtsRank"  INTEGER,
"dd2Rank"            INTEGER,
"td3Rank"            INTEGER,
"cfid"               INTEGER,
"cfparams"           TEXT,
"position"           TEXT);
'''

curr.execute(create_player_statistics_table)

with open('../data-loader/output/player-stats.json','r') as f:
    data = json.load(f)
    # Using the dictionaries key names as column
    # names and the values as values and inserting
    # data into the database
    # See: https://stackoverflow.com/a/14108554/
    if data:
        # Make the assumption that every JSON object has
        # list of all the columns
        columns      = ', '.join(list(data[0].keys()))
        placeholders = ', '.join('?' * len(data[0]))
        insertsql    = '''INSERT INTO {}  ({}) VALUES ({})'''.format("playerstats", columns, placeholders)

        for row in data:
            curr.execute(insertsql, list(row.values()))

conn.commit()

for row in curr.execute("SELECT DISTINCT(position) from playerstats"):
    print(row[0])

# Drop table if it exists
curr.execute('DROP TABLE IF EXISTS playermatchup')

# Create a table if it does not exist for player statistics
create_player_matchup_table = '''
CREATE TABLE IF NOT EXISTS playermatchup
(
id                     INTEGER PRIMARY KEY AUTOINCREMENT,       
gameId                 INTEGER,          
startTime              INTEGER, 
endTime                INTEGER,         
homeTeamCenterId       INTEGER,          
homeTeamForward1Id     INTEGER,         
homeTeamForward2Id     INTEGER,          
homeTeamGuard1Id       INTEGER,     
homeTeamGuard2Id       INTEGER,       
awayTeamCenterId       INTEGER,      
awayTeamForward1Id     INTEGER,       
awayTeamForward2Id     INTEGER,      
awayTeamGuard1Id       INTEGER,    
awayTeamGuard2Id       INTEGER,   
plusMinusPerMinute     REAL          
);                    
'''                   

# Create table to store player match ups
curr.execute(create_player_matchup_table)

# RegEx to match timecapsule filenames
timecapsule_filename_regex = re.compile('[0-9]+-[0-9]+-[0-9]+-data\.json')

for filename in os.listdir('../data-loader/output/'):
    if timecapsule_filename_regex.match(filename):
        with open('../data-loader/output/' + filename, 'r') as f:
            data                                 = json.load(f)
            values_dict                          = dict()
            values_dict["gameId"]                = data["gameId"]     
            values_dict["startTime"]             = data["startTime"]
            values_dict["endTime"]               = data["endTime"]   
            values_dict["homeTeamCenterId"]      = None    
            values_dict["homeTeamForward1Id"]    = None
            values_dict["homeTeamForward2Id"]    = None    
            values_dict["homeTeamGuard1Id"]      = None 
            values_dict["homeTeamGuard2Id"]      = None 
            values_dict["awayTeamCenterId"]      = None
            values_dict["awayTeamForward1Id"]    = None
            values_dict["awayTeamForward2Id"]    = None
            values_dict["awayTeamGuard1Id"]      = None
            values_dict["awayTeamGuard2Id"]      = None
            values_dict["plusMinusPerMinute"]    = data["pmPerMinute"]

            # Make sure that IDs are not repeating
            assert(len(set(data["homePlayers"])) == 5 and len(data["homePlayers"]) == 5)
            assert(len(set(data["awayPlayers"])) == 5 and len(data["awayPlayers"]) == 5)
            assert(len(set(data["homePlayers"] + data["awayPlayers"])) == 10)
                                                   
            # now go over the home team players and query what
            # their position is and then try to satisfy consts.
            # List of player positions
            playerPositions                     = dict()
            playerPositions['Guard']            = []
            playerPositions['Center']           = []
            playerPositions['Forward']          = []
            playerPositions['Forward-Center']   = []
            playerPositions['Center-Forward']   = []
            playerPositions['Forward-Guard']    = []
            playerPositions['Guard-Forward']    = []
            playerPositions['']                 = []
            
            for playerId in data["homePlayers"]:
                # Query home player and add to player positions
                positionSql = "SELECT position FROM playerstats WHERE playerId = {}".format(playerId)
                for position in curr.execute(positionSql):
                    for key in list(playerPositions.keys()):
                        if key == position[0].strip():
                            if playerId not in playerPositions[position[0]]:
                                playerPositions[position[0]].append(playerId)

            # Now solve the constraint satisfaction problem
            playerLineupCSAT(playerPositions)

            # Fill the values dict now
            values_dict["homeTeamCenterId"]      = playerPositions["Center"][0]    
            values_dict["homeTeamForward1Id"]    = playerPositions["Forward"][0]    
            values_dict["homeTeamForward2Id"]    = playerPositions["Forward"][1]    
            values_dict["homeTeamGuard1Id"]      = playerPositions["Guard"][0]    
            values_dict["homeTeamGuard2Id"]      = playerPositions["Guard"][1]    

            # now go over the away team players and query what
            # their position is and then try to satisfy consts.
            # List of player positions
            playerPositions                     = dict()
            playerPositions['Guard']            = []
            playerPositions['Center']           = []
            playerPositions['Forward']          = []
            playerPositions['Forward-Center']   = []
            playerPositions['Center-Forward']   = []
            playerPositions['Forward-Guard']    = []
            playerPositions['Guard-Forward']    = []
            playerPositions['']                 = []
            
            for playerId in data["awayPlayers"]:
                # Query home player and add to player positions
                positionSql = "SELECT position FROM playerstats WHERE playerId = {}".format(playerId)
                for position in curr.execute(positionSql):
                    for key in list(playerPositions.keys()):
                        if key == position[0].strip():
                            if playerId not in playerPositions[position[0]]:
                                playerPositions[position[0]].append(playerId)
            
            # Now solve the constraint satisfaction problem    
            playerLineupCSAT(playerPositions)

            values_dict["awayTeamCenterId"]      = playerPositions["Center"][0]
            values_dict["awayTeamForward1Id"]    = playerPositions["Forward"][0]
            values_dict["awayTeamForward2Id"]    = playerPositions["Forward"][1]
            values_dict["awayTeamGuard1Id"]      = playerPositions["Guard"][0]
            values_dict["awayTeamGuard2Id"]      = playerPositions["Guard"][1]

            # Now insert the record into the table
            columns      = ', '.join(list(values_dict.keys()))
            placeholders = ', '.join('?' * len(values_dict))
            insertsql    = '''INSERT INTO {}  ({}) VALUES ({})'''.format("playermatchup", columns, placeholders)
            curr.execute(insertsql, list(values_dict.values()))

conn.commit()

# Drop view if it exists
curr.execute('DROP VIEW IF EXISTS playerstatsnumview')

# Create view where we only select the numeric values from the table and use it in join
playerstats_numeric_view = """
CREATE VIEW IF NOT EXISTS playerstatsnumview
AS
   SELECT
          playerId           ,
          teamId             ,
          age                ,
          gp                 ,
          w                  ,
          l                  ,
          wPct               ,
          min                ,
          fgm                ,
          fga                ,
          fgPct              ,
          fG3M               ,
          fG3A               ,
          fg3Pct             ,
          ftm                ,
          fta                ,
          ftPct              ,
          oreb               ,
          dreb               ,
          reb                ,
          ast                ,
          tov                ,
          stl                ,
          blk                ,
          blka               ,
          pf                 ,
          pfd                ,
          pts                ,
          plusMinus          ,
          nbaFantasyPts      ,
          dD2                ,
          tD3                ,
          gpRank             ,
          wRank              ,
          lRank              ,
          wPctRank           ,
          minRank            ,
          fgmRank            ,
          fgaRank            ,
          fgPctRank          ,
          fg3mRank           ,
          fg3aRank           ,
          fg3PctRank         ,
          ftmRank            ,
          ftaRank            ,
          ftPctRank          ,
          orebRank           ,
          drebRank           ,
          rebRank            ,
          astRank            ,
          tovRank            ,
          stlRank            ,
          blkRank            ,
          blkaRank           ,
          pfRank             ,
          pfdRank            ,
          ptsRank            ,
          plusMinusRank      ,
          nbaFantasyPtsRank  ,
          dd2Rank            ,
          td3Rank            ,
          cfid               
     FROM playerstats;
"""

curr.execute(playerstats_numeric_view)
conn.commit()

# Drop view if it exists
curr.execute('DROP VIEW IF EXISTS timecapsuleview')

timecapsule_view = """
CREATE VIEW IF NOT EXISTS timecapsuleview
AS 
   SELECT 
   T2.*,
   T3.*,
   T4.*,
   T5.*,
   T6.*,
   T7.*,
   T8.*,
   T9.*,
   T10.*,
   T11.*,
   T1.plusMinusPerMinute 
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
   INNER JOIN playerstatsnumview as T11 on T11.playerId = T1.awayTeamGuard2Id
"""
curr.execute(timecapsule_view)
conn.commit()

conn.close()
