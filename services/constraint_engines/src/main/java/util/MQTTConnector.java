package util;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.MqttSecurityException;

import at.jku.lit.edgemode.esper.EsperManager;
import at.jku.lit.edgemode.esper.eventtypes.BatteryEvent;
import at.jku.lit.edgemode.esper.eventtypes.CollisionEvent;
import at.jku.lit.edgemode.esper.eventtypes.GripperPositionEvent;
import at.jku.lit.edgemode.esper.eventtypes.GripperSubPositionEvent;
import at.jku.lit.edgemode.esper.eventtypes.JointEffortEvent;
import at.jku.lit.edgemode.esper.eventtypes.LinearVelocityEvent;
import at.jku.lit.edgemode.esper.eventtypes.ManipulatorStateEvent;
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
					} else if (topic.contains("scan/ranges")) {
						CollisionEvent ce = new CollisionEvent();
						ce.setDistanceNearestObstacle(getClosestDistance(data));
						ce.setAmountOfInfiniteRangeUnits(getAmountOfInfiniteUnits(data));
						esperManager.update(ce);
					} else if (topic.contains("battery_state")) {
						BatteryEvent be = new BatteryEvent();
						be.setPercentage(getBatteryPercentage(data));
						esperManager.update(be);
					} else if (topic.contains("joint_states")) {
						JointEffortEvent jee = new JointEffortEvent();
						jee.setHighestJointEffort(getHighestJointEffort(data));
						esperManager.update(jee);
					} else if (topic.contains("kinematics_pose")) {
						GripperPositionEvent gpe = new GripperPositionEvent();
						gpe.setGripperPositionZ(Double.parseDouble(data));
						esperManager.update(gpe);
					} else if (topic.contains("open_manipulator/states/open_manipulator_moving_state")) {
						ManipulatorStateEvent mse = new ManipulatorStateEvent();
						mse.setMovingState(data.replace("\"", ""));
						esperManager.update(mse);
					} else if (topic.contains("open_manipulator/gripper_sub_position/command/data")) {
						GripperSubPositionEvent gspe = new GripperSubPositionEvent();
						gspe.setCommand(Double.parseDouble(data));
						esperManager.update(gspe);
					}
				}

				/**
				 * Returns the highest joint effort value of a joint effort string array
				 * 
				 * @param data the joint efforts as string
				 * @return the highest joint effort as String
				 */
				private double getHighestJointEffort(String data) {
					String intermStr = data.replaceAll("\\[", "").replaceAll("\\]", "");
					String[] jeStr = intermStr.split(",");
					double result = 0.0;
					double currJe;
					for (int i = 0; i < jeStr.length; i++) {
						currJe = Double.parseDouble(jeStr[i]);
						if (currJe > result) {
							result = currJe;
						}
					}
					return result;
				}

				/**
				 * Calculates the battery percentage.
				 * 
				 * @param data The mqtt topic data.
				 * @return the percentage as double.
				 */
				private double getBatteryPercentage(String data) {
					if (data.isEmpty()) {
						System.out.println("ERROR: Got empty data");
					}

					double weighted_percentage = Double.parseDouble(data) - 1;
					weighted_percentage *= 1000;
					return weighted_percentage;
				}

				/**
				 * Counts the amount of infinite range unit values.
				 * 
				 * @param data The string array.
				 * @return
				 */
				private int getAmountOfInfiniteUnits(String data) {
					String mySubstring = "None";
					int count = 0, index = 0;
					while ((index = data.indexOf(mySubstring, index)) != -1) {
						count++;
						index++;
					}
					return count;
				}

				/**
				 * Gets the closest distance of a String containing the ranges.
				 * 
				 * @param data The string array.
				 * @return
				 */
				private double getClosestDistance(String data) {
					// parse the string
					String intermStr = data.replaceAll("[\\[\\]]", "").replaceAll(",", "");
					intermStr = intermStr.replaceAll("\"", "").replaceAll("\n", "").replaceAll("None", "");
					String[] strArr = intermStr.split("\\s+");
					List<Double> distanceArr = new ArrayList<Double>();

					// get only the doubles
					for (int i = 0; i < strArr.length; i++) {
						if (!strArr[i].isEmpty()) {
							distanceArr.add(Double.parseDouble(strArr[i]));
						}
					}

					// find minimum
					return getMinimum(distanceArr);
				}

				/**
				 * Returns the minimum of a List of doubles.
				 * 
				 * @param distanceArr The list containting the doubles.
				 * @return
				 */
				private double getMinimum(List<Double> distanceArr) {
					double currMin = 99.0;

					// if too far away from any wall, no ranges will be measured
					if (distanceArr.isEmpty()) {
						return currMin;
					}

					for (int i = 0; i < distanceArr.size(); i++) {
						if (currMin > distanceArr.get(i)) {
							currMin = distanceArr.get(i);
						}
					}
					return currMin;
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
