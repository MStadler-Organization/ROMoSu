package at.jku.lit.edgemode.esper;

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

		ValidationManager.getInstance().registerEventListener(ConstraintRunner::updateStateEvent);

		// subscribe to MQTT broker
		MQTTConnector mqttConnector = new MQTTConnector(manager);
		mqttConnector.connect();
	}

	private static void updateStateEvent(Object event) {
		manager.update(event);
	}
}
