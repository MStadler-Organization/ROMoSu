package util;

import java.util.UUID;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.MqttSecurityException;

import at.jku.lit.edgemode.esper.EsperManager;
import at.jku.lit.edgemode.esper.eventtypes.LinearVelocityEvent;
import net.mv.tools.logging.ILogger;
import net.mv.tools.logging.LoggerProvider;

public class MQTTConnector {

	private static final ILogger LOGGER = LoggerProvider.getLogger(MQTTConnector.class);
	private String publisherId;
	private MqttClient mqttClient;
	private MqttConnectOptions options;
	private EsperManager esperManager;

	/**
	 * Creates a mqtt connector instance
	 */
	public MQTTConnector(EsperManager esperManager) {
		try {
			// set the manager
			this.esperManager = esperManager;
			// general connection settings
			this.publisherId = UUID.randomUUID().toString();
			// TODO: replace this here with the config details
			this.mqttClient = new MqttClient("tcp://localhost:1883", publisherId);
			this.options = new MqttConnectOptions();
			options.setAutomaticReconnect(true);
			options.setCleanSession(true);
			options.setConnectionTimeout(10);

			// handle received messages
			this.mqttClient.setCallback(new MqttCallback() {

				@Override
				public void messageArrived(String topic, MqttMessage message) throws Exception {
					System.out.println("topic: " + topic);
					System.out.println("Qos: " + message.getQos());
					System.out.println("message content: " + new String(message.getPayload()));
					handleMessage(topic, message.toString());
				}

				/**
				 * Handles a topic with its data by firing the correct event based on the topic.
				 * 
				 * @param topic The topic of the mqtt broker.
				 * @param data  The data received.
				 */
				private void handleMessage(String topic, String data) {
					if (topic.contains("cmd_vel/linear/x") || topic.contains("cmd_vel/linear$x")) {
						LinearVelocityEvent le = new LinearVelocityEvent();
						le.setLinearVelocity(Double.parseDouble(data));
						esperManager.update(le);
					}

				}

				@Override
				public void deliveryComplete(IMqttDeliveryToken token) {
					LOGGER.info("deliveryComplete---------" + token.isComplete());
				}

				@Override
				public void connectionLost(Throwable cause) {
					LOGGER.error(cause);
				}
			});

		} catch (MqttException e) {
			LOGGER.error(e);
			return;
		}
	}

	/**
	 * Connect to the MQTT broker and start monitoring.
	 */
	public void connect() {
		try {
			this.mqttClient.connect(this.options);
			this.mqttClient.subscribe("#"); // TODO ggf hier qos anpassen default = 1
		} catch (MqttSecurityException e) {
			LOGGER.error(e);
		} catch (MqttException e) {
			LOGGER.error(e);
		}

	}

	public MqttClient getMqttClient() {
		return mqttClient;
	}

}
