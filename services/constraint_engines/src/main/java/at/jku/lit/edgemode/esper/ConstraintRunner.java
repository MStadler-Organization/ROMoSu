package at.jku.lit.edgemode.esper;

import at.jku.lit.edgemode.esper.eventtypes.HeartBeatEvent;
import at.jku.lit.edgemode.esper.validation.ValidationManager;
import net.mv.tools.logging.ILogger;
import net.mv.tools.logging.LoggerProvider;

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

		while (true) {
			try {
				Thread.sleep(10000);
				updateStateEvent(new HeartBeatEvent()); // sends a heart beat event to trigger the heartbeat constraint
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
