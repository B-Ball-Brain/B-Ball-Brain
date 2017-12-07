import 'colors';
import {loadAvgPlayerStats, loadPlayerInfo} from './nba-stats';
import config from './config';
import fs from 'fs';
import makeDir from 'make-dir';
import path from 'path';

const run = async () => {
    try {
        const options = {
            Season: config.season
        };

        const playerStats = await loadAvgPlayerStats(options);

        for (const p of playerStats) {
            const playerInfo = await loadPlayerInfo(p.playerId, options);
            p.position = playerInfo.position;
        }

        const outputDir = path.join(config.outputDir, config.season);
        await makeDir(outputDir);

        const outputFile = path.join(outputDir, 'player-stats.json');
        fs.writeFileSync(outputFile, JSON.stringify(playerStats, null, '\t'));
    } catch (err) {
        console.log(err.toString().red);
    }
};

run();
