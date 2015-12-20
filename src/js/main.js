var safe = require("safe");

Pebble.addEventListener("ready", function(e) {
  require("./app");
});
