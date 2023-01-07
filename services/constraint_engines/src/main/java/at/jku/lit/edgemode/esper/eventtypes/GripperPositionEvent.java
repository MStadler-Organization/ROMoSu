package at.jku.lit.edgemode.esper.eventtypes;

import at.jku.lit.edgemode.esper.validation.api.IdableEvent;

public class GripperPositionEvent implements IdableEvent {

	private double gripperPositionZ;

	@Override
	public String getId() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public void setId(String value) {
		// TODO Auto-generated method stub

	}

	public double getGripperPositionZ() {
		return gripperPositionZ;
	}

	public void setGripperPositionZ(double gripperPositionZ) {
		this.gripperPositionZ = gripperPositionZ;
	}

}
