package at.jku.lit.edgemode.esper.validation;

import at.jku.lit.edgemode.esper.validation.api.IEventStreamListener;
import at.jku.lit.edgemode.esper.validation.api.IViolation;
import net.mv.tools.logging.ILogger;
import net.mv.tools.logging.LoggerProvider;

/**
 * 
 * ValidationManager needs to handle incoming events and add them to th CEP
 * engine, and violations sent to a target server/database...
 * 
 * 
 * @author michvier
 *
 */
public class ValidationManager {

	private static volatile ValidationManager INSTANCE;
	private static final ILogger LOGGER = LoggerProvider.getLogger(ValidationManager.class);

	public static ValidationManager getInstance() {
		if (INSTANCE == null) {
			synchronized (ValidationManager.class) {
				if (INSTANCE == null) {
					INSTANCE = new ValidationManager();
				}
			}

		}
		return INSTANCE;
	}

	public void sendViolation(IViolation violation) {
		LOGGER.info("New violation occured: " + violation);

	}

	public void init() {
		// TODO initialization...

	}

	public void registerEventListener(IEventStreamListener litener) {
		// TODO event lister for event stream...

	}

}
