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

    // get field name
    const fieldName = topic.replaceAll('/', '$')

    const pointToSave = new Point('mqtt-tb')
        .stringField(fieldName, JSON.stringify(data))

    writeApi.writePoint(pointToSave)
}
