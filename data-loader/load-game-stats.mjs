import 'colors';
import NbaStats from './nba-stats';
import fs from 'fs';

const playersOnCourtPerTeam = 5;

const writeData = async (options) => {
    const nbaStats = new NbaStats(options.season);

    console.log('Loading all game IDs');
    const gameIds = await nbaStats.loadGameIds();

    let i = 1;
    for (const gameId of gameIds) {
        console.log(`Loading game ${i} of ${gameIds.size}: ${gameId}`);
        i++;

        const subTimes = await nbaStats.loadGameSubTimes(gameId);

        let startTime = 0;
        for (const subTime of subTimes) {
            const endTime = subTime - options.subPadding;
            const file = `output/${gameId}-${startTime}-${endTime}-data.json`;

            if (endTime - options.minTimeBetweenSubs > startTime &&
                !fs.existsSync(file)) {
                const timeRangeStats = await nbaStats
                    .loadTrainingDataInTimeRange(gameId, startTime, endTime);

                const numHomePlayers = timeRangeStats.homePlayers.length;
                const numAwayPlayers = timeRangeStats.awayPlayers.length;

                if (numHomePlayers === playersOnCourtPerTeam &&
                    numAwayPlayers === playersOnCourtPerTeam) {
                    fs.writeFileSync(
                        file,
                        JSON.stringify(timeRangeStats, null, '\t')
                    );
                } else {
                    console.warn(`From ${startTime} to ${endTime}, the home \
team has ${numHomePlayers} players and the away team has ${numAwayPlayers}!
Skipping...`.yellow);
                }
            }

            startTime = subTime + options.subPadding;
        }
    }
};

writeData({
    season: '2016-17',
    minTimeBetweenSubs: 300,
    subPadding: 10
}).then(
    () => console.log('Successfully wrote data'.green),
    (err) => console.error(err.toString().red)
);
