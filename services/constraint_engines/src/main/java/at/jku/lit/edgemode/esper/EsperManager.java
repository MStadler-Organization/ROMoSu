package at.jku.lit.edgemode.esper;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.Stream;

import com.espertech.esper.client.Configuration;
import com.espertech.esper.client.EPAdministrator;
import com.espertech.esper.client.EPRuntime;
import com.espertech.esper.client.EPServiceProvider;
import com.espertech.esper.client.EPServiceProviderManager;
import com.espertech.esper.client.EPStatement;

import at.jku.lit.edgemode.esper.eventtypes.CollisionEvent;
import at.jku.lit.edgemode.esper.eventtypes.LinearVelocityEvent;
import at.jku.lit.edgemode.esper.validation.ValidationFactory;
import at.jku.lit.edgemode.esper.validation.api.IConstraint;
import net.mv.tools.logging.ILogger;
import net.mv.tools.logging.LoggerProvider;

/**
 * 
 * Main esper CEP implementation that holds the CEP Engine and loads pattern as
 * constraints from the resource folder and feeds them into the CEP Runtime.
 * 
 * @author michvier
 *
 */
public class EsperManager {

	private static final ILogger LOGGER = LoggerProvider.getLogger(EsperManager.class);

	private EPRuntime cepRT;
	private EPAdministrator cepAdm;

	private static final String CONSTRAINT_STORAGE_LOCATION = "src/main/resources/constraints";

	public void update(Object event) {
		cepRT.sendEvent(event);

	}

	public void init() {
		LOGGER.info("Initializing Esper Manager");
		Configuration cepConfig = new Configuration();

		registerEventTypes(cepConfig);

		EPServiceProvider cep = EPServiceProviderManager.getProvider("CEP-Engine", cepConfig);
		cepRT = cep.getEPRuntime();
		cepAdm = cep.getEPAdministrator();
		try {
			readConstraints();
		} catch (Exception e) {
			LOGGER.error(e);
		}

	}

	/**
	 * All events used in a pattern need to exist as Java classes and must be
	 * registered with the CEP Runtime
	 * 
	 * @param cepConfig
	 */
	private void registerEventTypes(Configuration cepConfig) {
		cepConfig.addEventType(LinearVelocityEvent.class);
		cepConfig.addEventType(CollisionEvent.class);
	}

	private void readConstraints() throws IOException {
		Stream<Path> path = Files.walk(Paths.get(CONSTRAINT_STORAGE_LOCATION));
		path = path.filter(Files::isRegularFile);
		path.forEach(p -> {
			try {
				loadConstraint(p);
			} catch (Throwable e) {
				LOGGER.error(p.toString() + " not loaded");
			}
		});

	}

	private void loadConstraint(Path p) throws IOException {
		List<String> lines = Files.readAllLines(p);
		IConstraint constraint = readConstraint(p, lines);

		registerConstraint(constraint);

	}

	private IConstraint readConstraint(Path p, List<String> lines) {
		String name = lines.get(0).replace("NAME=", "");

		int i = 1;
		String s = lines.get(i);
		StringBuilder code = new StringBuilder();

		while (!s.equals(";")) {
			code.append(s + "\n");
			i++;
			s = lines.get(i);
		}

		return ValidationFactory.createConstraint(p.getFileName().toString(), name,
				code.toString().replace("CONSTRAINT=", ""));
	}

	public void registerConstraint(IConstraint constraint) {
		try {
			LOGGER.info("Registering new Statement " + constraint);
			EPStatement statemet = cepAdm.createEPL(constraint.getCode());
			statemet.addListener(new CEPStatementListener(constraint));

		} catch (Exception e) {
			LOGGER.error("Error" + constraint.getFile());
			LOGGER.error(e);
		}
	}

}
