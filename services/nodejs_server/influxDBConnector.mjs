import {InfluxDB, Point} from "@influxdata/influxdb-client";
import CONFIG from './utils/getConfig.js';

const url = CONFIG.influx_db_url
const api_token = CONFIG.influx_db_api_token
const organization = CONFIG.influx_db_organisation
const bucket = CONFIG.influx_db_bucket

const influxDB = new InfluxDB({url: url, token: api_token})
const writeApi = influxDB.getWriteApi(organization, bucket)


/**
 * Inserts data into the TurtleBot DB
 * @param topic the topic from the mqtt broker
 * @param data the received data via mqtt
 */
export const insertTBData = (topic, data) => {
    console.log(topic)
    console.log(data)


    const pointToSave = new Point('mqtt-tb')
        .stringField('data', data.toString())

    writeApi.writePoint(pointToSave)

    writeApi.close().then(() => {
        console.log('WRITE FINISHED')
    })
}
