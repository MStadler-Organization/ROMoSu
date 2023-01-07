package at.jku.lit.edgemode.esper.eventtypes;

import at.jku.lit.edgemode.esper.validation.api.IdableEvent;

public class BatteryEvent implements IdableEvent {

	private double percentage;

	@Override
	public String getId() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public void setId(String value) {
		// TODO Auto-generated method stub

	}

	public double getPercentage() {
		return percentage;
	}

	public void setPercentage(double percentage) {
		this.percentage = percentage;
	}

}
