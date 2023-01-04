package at.jku.lit.edgemode.esper.validation.api;

import java.io.Serializable;

/**
 * 
 * Interface for constraint violations - when a esper pattern is triggered.
 * 
 * @author michvier
 *
 */
public interface IViolation extends Serializable {

	IConstraint getConstraint();

}
