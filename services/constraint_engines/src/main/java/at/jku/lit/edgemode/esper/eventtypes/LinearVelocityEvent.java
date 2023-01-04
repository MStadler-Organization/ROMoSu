package at.jku.lit.edgemode.esper.eventtypes;

import at.jku.lit.edgemode.esper.validation.api.IdableEvent;

public class LinearVelocityEvent implements IdableEvent {

	private double linearVelocity;

	@Override
	public String getId() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public void setId(String value) {
		// TODO Auto-generated method stub

	}

	public double getLinearVelocity() {
		return linearVelocity;
	}

	public void setLinearVelocity(double linearVelocity) {
		this.linearVelocity = linearVelocity;
	}

}
