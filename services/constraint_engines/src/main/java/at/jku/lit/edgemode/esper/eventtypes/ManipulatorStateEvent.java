package at.jku.lit.edgemode.esper.eventtypes;

import at.jku.lit.edgemode.esper.validation.api.IdableEvent;

public class ManipulatorStateEvent implements IdableEvent {

	private String movingState;

	@Override
	public String getId() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public void setId(String value) {
		// TODO Auto-generated method stub

	}

	public String getMovingState() {
		return movingState;
	}

	public void setMovingState(String movingState) {
		this.movingState = movingState;
	}

}
