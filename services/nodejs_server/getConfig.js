'use strict';

const fs = require('fs');
const appRoot = require('app-root-path');
const path = require('path')

let config = {}

let rawData = fs.readFileSync(`${appRoot}${path.sep}..${path.sep}..${path.sep}config${path.sep}config.json`);
let jsonConfig = JSON.parse(rawData.toString());

config.nodejs_hostname = jsonConfig.nodejs_hostname
config.nodejs_port = jsonConfig.nodejs_port

console.log('Successfully laoded config file!')

module.exports = config
