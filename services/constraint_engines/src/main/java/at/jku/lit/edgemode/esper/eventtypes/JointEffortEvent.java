package at.jku.lit.edgemode.esper.eventtypes;

import at.jku.lit.edgemode.esper.validation.api.IdableEvent;

public class JointEffortEvent implements IdableEvent {

	private double highestJointEffort;

	@Override
	public String getId() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public void setId(String value) {
		// TODO Auto-generated method stub

	}

	public double getHighestJointEffort() {
		return highestJointEffort;
	}

	public void setHighestJointEffort(double highestJointEffort) {
		this.highestJointEffort = highestJointEffort;
	}

}
