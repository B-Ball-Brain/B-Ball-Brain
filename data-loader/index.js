const NBA = require("nba");
const util = require("util");
const fs = require("fs");

NBA.stats.playerStats({
    Season: "2016-17"
})
.then(
    (data) => util.promisify(fs.writeFile)("players.json", JSON.stringify(data))
)
.catch(console.error);
