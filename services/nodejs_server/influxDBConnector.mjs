import CONFIG from './utils/getConfig.js';

//const influxDB = new InfluxDB({YOUR_URL, YOUR_API_TOKEN})
/**
 * Inserts data into the TurtleBot DB
 * @param topic the topic from the mqtt broker
 * @param data the received data via mqtt
 */
export const insertTBData = (topic, data) => {
    console.log(topic)
    console.log(data.hola)
}


console.log(CONFIG.influx_db_api_token)
