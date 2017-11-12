const nba = require("nba");
const util = require("util");
const fs = require("fs");

const downloadLeagueGameLog = (file, options) => nba.stats.leagueGameLog(options)
    .then(
        (data) => util.promisify(fs.writeFile)(file, JSON.stringify(data, null, '\t'))
    );

Promise.all([
    downloadLeagueGameLog("player-data.json", {PlayerOrTeam: "P"}),
    downloadLeagueGameLog("team-data.json", {PlayerOrTeam: "T"})
]).then(
    () => console.log("Successfully loaded data"),
    console.error
);
