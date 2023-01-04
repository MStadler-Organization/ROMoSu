package at.jku.lit.edgemode.esper.eventtypes;

import at.jku.lit.edgemode.esper.validation.api.IdableEvent;

public class CollisionEvent implements IdableEvent {

	// closest is 0.11999999731779099
	private double distanceNearestObstacle;

	private int amountOfInfiniteRangeUnits;

	@Override
	public String getId() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public void setId(String value) {
		// TODO Auto-generated method stub

	}

	public int getAmountOfInfiniteRangeUnits() {
		return amountOfInfiniteRangeUnits;
	}

	public void setAmountOfInfiniteRangeUnits(int amountOfInfiniteRangeUnits) {
		this.amountOfInfiniteRangeUnits = amountOfInfiniteRangeUnits;
	}

	public double getDistanceNearestObstacle() {
		return distanceNearestObstacle;
	}

	public void setDistanceNearestObstacle(double distanceNearestObstacle) {
		this.distanceNearestObstacle = distanceNearestObstacle;
	}

}
