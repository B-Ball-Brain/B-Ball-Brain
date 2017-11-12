const nba = require('nba');
const util = require('util');
const fs = require('fs');

const downloadLeagueGameLog = (file, ...options) => nba.stats.leagueGameLog(Object.assign(...options))
    .then(
        (data) => util.promisify(fs.writeFile)(file, JSON.stringify(data, null, '\t'))
    );

const baseOptions = {
    Season: '2016-17'
};

Promise.all([
    downloadLeagueGameLog('player-data.json', baseOptions, {PlayerOrTeam: 'P'}),
    downloadLeagueGameLog('team-data.json', baseOptions, {PlayerOrTeam: 'T'})
]).then(
    () => console.log('Successfully loaded data'),
    console.error
);
