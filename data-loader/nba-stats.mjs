import nba from 'nba';

const tenthsOfSecondsPerSecond = 10;
const tenthsOfSecondsPerMinute = 60 * tenthsOfSecondsPerSecond;
const tenthsOfSecondsPerPeriod = 12 * tenthsOfSecondsPerMinute;
const tenthsOfSecondsPerOvertime = 5 * tenthsOfSecondsPerMinute;
const numRegularPeriods = 4;

const tenthsOfSecondsIntoGame = (period, clock) => {
    let time =
        (tenthsOfSecondsPerPeriod * Math.min(period, numRegularPeriods)) +
        (tenthsOfSecondsPerOvertime * Math.max(0, period - numRegularPeriods));

    const [, min, sec] = clock.match(/(\d{1,2}):(\d{2})/);

    time -= tenthsOfSecondsPerMinute * parseInt(min, 10);
    time -= tenthsOfSecondsPerSecond * parseInt(sec, 10);

    return time;
};

export const loadAvgPlayerStats = async (options) => {
    const playerStatsResponses = await nba.stats.playerStats(
        Object.assign({
            PerMode: 'PerMinute'
        }, options)
    );

    return playerStatsResponses.leagueDashPlayerStats;
};

export const loadPlayerInfo = async (playerId, options) => {
    const playerInfoResponse = await nba.stats.playerInfo(
        Object.assign({
            PlayerID: playerId
        }, options)
    );

    return playerInfoResponse.commonPlayerInfo[0];
};

export const loadGameIds = async (options) => {
    const gameLogResponse = await nba.stats.leagueGameLog(
        Object.assign({
            PlayerOrTeam: 'T'
        }, options)
    );
    const gameIdIndex = 4;
    const allIds = gameLogResponse.resultSets[0].rowSet
        .map((g) => g[gameIdIndex]);

    return new Set(allIds);
};

export const loadGameSubTimes = async (gameId, options) => {
    const playByPlayResponse = await nba.stats.playByPlay(
        Object.assign({
            GameID: gameId.toString()
        }, options)
    );
    const subEventMsgType = 8;

    const numPeriods = playByPlayResponse.playByPlay.reduce(
        (prev, cur) => (prev.period < cur.period ? cur : prev)
    ).period;

    const subTimes = playByPlayResponse.playByPlay
        .filter((p) => p.eventmsgtype === subEventMsgType)
        .map((p) => tenthsOfSecondsIntoGame(p.period, p.pctimestring));

    for (let i = 1; i <= numPeriods; i++) {
        subTimes.push(tenthsOfSecondsIntoGame(i, '0:00'));
    }

    return subTimes.sort((a, b) => a - b);
};

export const loadTrainingDataInTimeRange =
    async (gameId, startTime, endTime, options) => {
        const boxScoreResponse = await nba.stats.boxScore(
            Object.assign({
                GameID: gameId.toString(),
                RangeType: '2',
                StartRange: startTime.toString(),
                EndRange: endTime.toString()
            }, options)
        );

        const teamIdIndex = 1;
        const pmIndex = 24;
        const playerIdIndex = 4;

        const players = boxScoreResponse.resultSets[0].rowSet;
        const [awayTeam, homeTeam] = boxScoreResponse.resultSets[1].rowSet;

        if (!homeTeam || !awayTeam) {
            throw new Error(`Cannot load data for ${gameId}: ${startTime}-\
${endTime}`);
        }

        const homeTeamId = homeTeam[teamIdIndex];
        const awayTeamId = awayTeam[teamIdIndex];
        const pmPerMinute = tenthsOfSecondsPerMinute * homeTeam[pmIndex] /
            (endTime - startTime);

        return {
            gameId,
            startTime,
            endTime,
            homePlayers: players.filter((p) => p[teamIdIndex] === homeTeamId)
                .map((p) => p[playerIdIndex]),
            awayPlayers: players.filter((p) => p[teamIdIndex] === awayTeamId)
                .map((p) => p[playerIdIndex]),
            pmPerMinute
        };
    };
