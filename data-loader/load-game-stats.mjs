import 'colors';
import {
    loadGameIds,
    loadGameSubTimes,
    loadTrainingDataInTimeRange
} from './nba-stats';
import config from './config';
import fs from 'fs';
import makeDir from 'make-dir';
import path from 'path';

const playersOnCourtPerTeam = 5;

const writeData = async (minTimeBetweenSubs, subPadding, options) => {
    const outputDir = path.join(
        config.outputDir,
        options.Season,
        options.SeasonType
    );
    await makeDir(outputDir);

    console.log('Loading all game IDs');
    const gameIds = await loadGameIds(options);

    let i = 1;
    for (const gameId of gameIds) {
        console.log(`Loading game ${i} of ${gameIds.size}: ${gameId}`);
        i++;

        const subTimes = await loadGameSubTimes(gameId, options);

        let startTime = 0;
        for (const subTime of subTimes) {
            const endTime = subTime - subPadding;
            const outputFile = path.join(
                outputDir, `${gameId}-${startTime}-${endTime}-data.json`
            );

            if (endTime - minTimeBetweenSubs > startTime &&
                !fs.existsSync(outputFile)) {
                const timeRangeStats = await loadTrainingDataInTimeRange(
                    gameId,
                    startTime,
                    endTime,
                    options
                );

                const numHomePlayers = timeRangeStats.homePlayers.length;
                const numAwayPlayers = timeRangeStats.awayPlayers.length;

                if (numHomePlayers === playersOnCourtPerTeam &&
                    numAwayPlayers === playersOnCourtPerTeam) {
                    fs.writeFileSync(
                        outputFile,
                        JSON.stringify(timeRangeStats, null, '\t')
                    );
                } else {
                    console.warn(`From ${startTime} to ${endTime}, the home \
team has ${numHomePlayers} players and the away team has ${numAwayPlayers}!
Skipping...`.yellow);
                }
            }

            startTime = subTime + subPadding;
        }
    }
};

const run = async () => {
    try {
        const minTimeBetweenSubs = 300;
        const subPadding = 10;

        await writeData(minTimeBetweenSubs, subPadding, {
            Season: config.season,
            SeasonType: 'Regular Season'
        });

        await writeData(minTimeBetweenSubs, subPadding, {
            Season: config.season,
            SeasonType: 'Playoffs'
        });

        console.log('Successfully wrote data'.green);
    } catch (err) {
        console.error(err.toString().red);
    }
};

run();
