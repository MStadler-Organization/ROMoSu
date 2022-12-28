'use strict';

const fs = require('fs');
const appRoot = require('app-root-path');
const path = require('path')

let config = {}

let rawData = fs.readFileSync(`${appRoot.path}${path.sep}..${path.sep}..${path.sep}config${path.sep}config.json`);
let jsonConfig = JSON.parse(rawData.toString());


config.nodejs_hostname = jsonConfig.nodejs_hostname;
config.nodejs_port = jsonConfig.nodejs_port;
config.mqtt_ip = jsonConfig.mqtt_ip;
config.mqtt_port = jsonConfig.mqtt_port;
config.influx_db_url = jsonConfig.influx_db_url;
config.influx_db_api_token = jsonConfig.influx_db_api_token;
config.influx_db_organisation = jsonConfig.influx_db_organisation;
config.influx_db_bucket = jsonConfig.influx_db_bucket;

module.exports = config
