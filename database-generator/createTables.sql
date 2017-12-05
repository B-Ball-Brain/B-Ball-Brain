DROP TABLE IF EXISTS playerstats;

CREATE TABLE IF NOT EXISTS playerstats(
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


DROP TABLE IF EXISTS playermatchup;

CREATE TABLE IF NOT EXISTS playermatchup(
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
plusMinusPerMinute     REAL);



DROP VIEW IF EXISTS playerstatsnumview;


CREATE VIEW IF NOT EXISTS playerstatsnumview AS 
    SELECT 
	    playerId,
		teamId,
		age,
		gp,
		w,
		l,
		wPct,
		min,
		fgm,
		fga,
		fgPct,
		fG3M,
		fG3A,
		fg3Pct,
		ftm,
		fta,
		ftPct,
		oreb,
		dreb,
		reb,
		ast,
		tov,
		stl,
		blk,
		blka,
		pf,
		pfd,
		pts,
		plusMinus,
		nbaFantasyPts,
		dD2,
		tD3,
		gpRank,
		wRank,
		lRank,
		wPctRank,
		minRank,
		fgmRank,
		fgaRank,
		fgPctRank,
		fg3mRank,
		fg3aRank,
		fg3PctRank,
		ftmRank,
		ftaRank,
		ftPctRank,
		orebRank,
		drebRank,
		rebRank,
		astRank,
		tovRank,
		stlRank,
		blkRank,
		blkaRank,
		pfRank,
		pfdRank,
		ptsRank,
		plusMinusRank,
		nbaFantasyPtsRank,
		dd2Rank,
		td3Rank,
		cfid
FROM playerstats; 


DROP VIEW IF EXISTS timecapsuleview;

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
   INNER JOIN playerstatsnumview as T11 on T11.playerId = T1.awayTeamGuard2Id;

ALTER VIEW timecapsuleview DROP COLUMN playerId;

ALTER VIEW timecapsuleview DROP COLUMN teamId;
