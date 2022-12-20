const http = require('http');
const Influx = require('influx');


const config = require('./getConfig');

const hostname = config.nodejs_hostname;
const port = config.nodejs_port;

const server = http.createServer((req, res) => {
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/plain');
    res.end('Node JS Server for InfluxDB');
});

server.listen(port, hostname, () => {
    console.log(`Server running at http://${hostname}:${port}/`);
});

