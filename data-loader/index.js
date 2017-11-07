const NBA = require("nba");
const util = require("util");
const fs = require("fs");

NBA.stats.playerStats({
    Season: "2016-17"
})
.then(
    (data) => util.promisify(fs.writeFile)("players-data.json", JSON.stringify(data))
)
.catch(console.error);

NBA.stats.boxScore({
    GameID: "0021700146"
})
.then(
    (data) => util.promisify(fs.writeFile)("scores-data.json", JSON.stringify(data, null, '\t'))
)
.catch(console.error);
