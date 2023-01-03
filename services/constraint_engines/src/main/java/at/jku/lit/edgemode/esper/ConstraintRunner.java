package at.jku.lit.edgemode.esper;

import at.jku.lit.edgemode.esper.eventtypes.HeartBeatEvent;
import at.jku.lit.edgemode.esper.eventtypes.LinearVelocityEvent;
import at.jku.lit.edgemode.esper.validation.ValidationManager;
import net.mv.tools.logging.ILogger;
import net.mv.tools.logging.LoggerProvider;
import util.MQTTConnector;

/**
 * 
 * Main Runner class that initializes the CEP engine, listener, etc... and loops
 * infinitely.
 * 
 * @author michvier
 *
 */
public class ConstraintRunner {

	private static final ILogger LOGGER = LoggerProvider.getLogger(ConstraintRunner.class);
	static EsperManager manager = new EsperManager();

	public static void main(String[] args) {

		manager.init();
		ValidationManager.getInstance().init();

		ValidationManager.getInstance().registerEventListener(event -> {
			updateStateEvent(event);
		});

		// subscribe to MQTT broker
//		MQTTConnector mqttConnector = new MQTTConnector();
//		mqttConnector.connect();
		
		while (true) {
			try {
				Thread.sleep(1000);
				System.out.println("Violating now");
				LinearVelocityEvent le = new LinearVelocityEvent();
				le.setLinearVelocity(33.0);
				updateStateEvent(le); // sends a heart beat event to trigger the heartbeat constraint
														// vioaltion for testing
			} catch (InterruptedException e) {
				LOGGER.error(e);
			}
		}
	}

	private static void updateStateEvent(Object event) {
		manager.update(event);

	}

}
