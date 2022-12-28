const http = require('http');
const connectToMQTT = require("./api_connector/MQTTConnector");
const config = require("./utils/getConfig");

const hostname = config.nodejs_hostname;
const port = config.nodejs_port;


// connect to mqtt
connectToMQTT()