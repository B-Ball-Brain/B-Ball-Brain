import 'colors';
import NbaStats from './nba-stats';
import fs from 'fs';

const nbaStats = new NbaStats('2016-17');
nbaStats.loadAvgPlayerStats()
    .then((stats) => {
        fs.writeFileSync(
            'output/player-stats.json',
            JSON.stringify(stats, null, '\t')
        );
    })
    .catch((err) => console.log(err.toString().red));
