package at.jku.lit.edgemode.esper.eventtypes;

import at.jku.lit.edgemode.esper.validation.api.IdableEvent;

public class CollisionEvent implements IdableEvent {

	// closest is 0.11999999731779099
	private double distanceNearestObstacle;

	@Override
	public String getId() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public void setId(String value) {
		// TODO Auto-generated method stub

	}

	public double getDistanceNearestObstacle() {
		return distanceNearestObstacle;
	}

	public void setDistanceNearestObstacle(double distanceNearestObstacle) {
		this.distanceNearestObstacle = distanceNearestObstacle;
	}

}
