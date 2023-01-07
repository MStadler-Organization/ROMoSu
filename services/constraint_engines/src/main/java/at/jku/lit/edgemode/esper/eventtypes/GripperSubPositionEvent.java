package at.jku.lit.edgemode.esper.eventtypes;

import at.jku.lit.edgemode.esper.validation.api.IdableEvent;

public class GripperSubPositionEvent implements IdableEvent {

	private double command;

	@Override
	public String getId() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public void setId(String value) {
		// TODO Auto-generated method stub

	}

	public double getCommand() {
		return command;
	}

	public void setCommand(double command) {
		this.command = command;
	}

}
