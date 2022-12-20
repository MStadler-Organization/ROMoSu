const CONFIG = require('./utils/getConfig');
const http = require('http');
const run_mqtt = require('./api_connector/mqtt');

const hostname = CONFIG.nodejs_hostname;
const port = CONFIG.nodejs_port;

const server = http.createServer((req, res) => {
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/plain');
    res.end('Node JS Server for InfluxDB');
});

server.listen(port, hostname, () => {
    console.log(`Server running at http://${hostname}:${port}/`);
});

// connect to mqtt
run_mqtt()