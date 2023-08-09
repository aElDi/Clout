Logger-service
=========

## Installation

  npm install logger-service --save

## Usage
```
var logger = require("config/logger")({
  remote: {
    type: 'powerball',
    host: '192.168.64.2',
    port: '8080'
  },
  local: {
    logPath : config.logPath,
    filename: '/all-logs.log'
  }
});

logger.info('Express server listening on port 3000'; 

// Like http listener using morgan

var app = express();
app.use(logger.httpListener);
```