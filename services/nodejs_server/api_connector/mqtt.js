const mqtt = require('mqtt')
const CONFIG = require('./../utils/getConfig');

function connectToMQTT() {
    // connect to mqtt
    const client = mqtt.connect(`mqtt://${CONFIG.mqtt_ip}`)


    client.on('connect', function () {
        // successful connection
        console.log('Successful connection to mqtt client!')

        client.subscribe('+/meta') // subscribe to all meta infos
    })

    client.on('message', function (topic, message, packet) {
        console.log("message is " + message);
        console.log("topic is " + topic);
    });
}

module.exports = connectToMQTT
