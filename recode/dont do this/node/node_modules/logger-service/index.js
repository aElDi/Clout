var winstonLogger;
var winston = require('winston');
var request = require('request');
var fs = require( 'fs' );
var util = require('util');
winston.emitErrs = true;

var CustomLogger = winston.transports.CustomLogger = function (options) {
  this.name = 'customLogger';
  if (options) {
    this.type = options.type;
    this.host = options.host;
    this.port = options.port;    
  }
};

util.inherits(CustomLogger, winston.Transport);

CustomLogger.prototype.log = function (level, msg, meta, callback) {
  request({ url: 'http://'+this.host+':'+this.port, method: 'PUT', json: {type: this.type, message: msg, meta: meta}}, function(error, response, body){
    callback(null, true);
  })
};
winston.add(CustomLogger);

module.exports = logger;

function logger(options) {
  if (!winstonLogger) {
    winstonLogger = new winston.Logger({
        transports: getTransports(options),
        exitOnError: false
    });

    winstonLogger.httpListener = require("morgan")("combined", { "stream": {
      write: function(message, encoding) {
        winstonLogger.info(message);
      }
    }});
  }

  return winstonLogger;
}


function getTransports(options) {
  var transports = [
    new winston.transports.Console({
      level: 'info',
      handleExceptions: true,
      humanReadableUnhandledException: true,
      json: false,
      colorize: true
    }),
  ];

  if (options.remote) {
    transports.push(
      new winston.transports.CustomLogger({
        host: options.remote.host,
        port: options.remote.port,
        type: options.remote.type,
        handleExceptions: true,
        humanReadableUnhandledException: true,
        json: true,
        colorize: false
      })
    )
  }

  if (options.local) {
    if ( !fs.existsSync( options.local.logPath ) ) {
      fs.mkdirSync( options.local.logPath );
    }

    transports.push(
      new winston.transports.File({
          level: 'info',
          filename: options.local.logPath + '/' + options.local.filename,
          handleExceptions: true,
          humanReadableUnhandledException: true,
          json: true,
          maxsize: 5242880, //5MB
          maxFiles: 5,
          colorize: false
      })
    )
  }

  return transports;
}
