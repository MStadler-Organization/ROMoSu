const http = require('http');
const Influx = require('influx');


const CONFIG = require('./utils/getConfig');

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

console.log(CONFIG.mqtt_ip);
