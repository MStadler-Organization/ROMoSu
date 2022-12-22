const MQTTConnector = require('mqtt')
const CONSTANTS = require('./../utils/constants')

const CONFIG = require('./../utils/getConfig')
const influxDBConnector = require("../influxDBConnector");

const DECODER = new TextDecoder("utf-8");

function connectToMQTT() {
    // connect to MQTTConnector
    const client = MQTTConnector.connect(`mqtt://${CONFIG.mqtt_ip}`)


    client.on('connect', function () {
        // successful connection
        console.log('Successful connection to MQTTConnector client!')

        client.subscribe('#') // subscribe to all meta infos
    })


    // on message receive
    client.on('message', function (topic, message, packet) {
        // insert data in influxdb
        if (topic.includes(CONSTANTS.META)) {
            // do nothing...
        } else if (topic.includes(CONSTANTS.TB_TYPE)) {
            influxDBConnector.insertTBData(topic, JSON.parse(DECODER.decode(message)))
        } else if (topic.includes(CONSTANTS.DUMMY_TYPE)) {
            //TODO: insert here the other types e.g. nyro...
        } else {
            console.error(`Got unknown topic: ${topic}`)
        }
    });
}

module.exports = connectToMQTT