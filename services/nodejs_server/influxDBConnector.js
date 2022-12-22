const CONFIG = require('./utils/getConfig');
const {InfluxDB} = require("influx");
const {Point} = require("@influxdata/influxdb-client");

const influxUrl = CONFIG.influx_db_url
const influxAPIToken = CONFIG.influx_db_api_token
/*
const influxDB = new InfluxDB.InfluxDB({
    host: "localhost",
    database: "example",
    schema: [
        {
            measurement: 'cpu-temp',
            fields: {
                temp: InfluxDB.FieldType.FLOAT,
                cpu: InfluxDB.FieldType.INTEGER,
                socket: InfluxDB.FieldType.INTEGER
            },
            tags: ['host']
        }
    ]
});
*/

/**
 * Inserts data into the TurtleBot DB
 * @param topic the topic from the mqtt broker
 * @param data the received data via mqtt
 */
exports.insertTBData = function (topic, data) {
    console.log(topic)
    console.log(data.hola)

}

