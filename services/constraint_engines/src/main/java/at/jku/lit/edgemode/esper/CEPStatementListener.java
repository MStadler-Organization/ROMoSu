package at.jku.lit.edgemode.esper;

import java.util.Map.Entry;

import com.espertech.esper.client.EventBean;
import com.espertech.esper.client.UpdateListener;
import com.espertech.esper.event.bean.BeanEventBean;
import com.espertech.esper.event.map.MapEventBean;

import at.jku.lit.edgemode.esper.validation.ValidationFactory;
import at.jku.lit.edgemode.esper.validation.ValidationManager;
import at.jku.lit.edgemode.esper.validation.api.IConstraint;
import at.jku.lit.edgemode.esper.validation.api.IViolation;
import at.jku.lit.edgemode.esper.validation.api.IdableEvent;
import net.mv.tools.logging.ILogger;
import net.mv.tools.logging.LoggerProvider;

/**
 * 
 * Implementation of an Esper CEP Listener that is is called when a pattern is
 * triggered.
 * 
 * @author michvier
 *
 */
public class CEPStatementListener implements UpdateListener {

	private static final ILogger LOGGER = LoggerProvider.getLogger(CEPStatementListener.class);
	private IConstraint constraint;

	public CEPStatementListener(IConstraint constraint) {
		this.constraint = constraint;
	}

	@Override
	public void update(EventBean[] newData, EventBean[] oldData) {
		try {

			EventBean event = newData[0];
			Object eve = event.getUnderlying();
			if (event instanceof MapEventBean) {
				MapEventBean ev = (MapEventBean) event;
				System.out.println(ev.getProperties());
				IdableEvent idevent = null;
				for (Entry<String, Object> p : ev.getProperties().entrySet()) {

					if (p.getValue() instanceof BeanEventBean) {
						idevent = (IdableEvent) ((BeanEventBean) p.getValue()).getUnderlying();
						break;
					}

					idevent = (IdableEvent) p.getValue();
					break;
				}
				IViolation violation = ValidationFactory.createViolation(idevent != null ? idevent.getId() : "null",
						constraint, ev.getUnderlying());
				ValidationManager.getInstance().sendViolation(violation);

			} else if (event instanceof EventBean) {
				IViolation violation = ValidationFactory.createViolation(((IdableEvent) event.getUnderlying()).getId(),
						constraint, event.getUnderlying());
				ValidationManager.getInstance().sendViolation(violation);
			}

			else {
				LOGGER.error("not handled:" + event.getClass());
			}
		} catch (Throwable t) {
			t.printStackTrace();
		}
	}

}
