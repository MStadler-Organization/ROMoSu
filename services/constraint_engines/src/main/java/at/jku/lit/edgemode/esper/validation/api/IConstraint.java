package at.jku.lit.edgemode.esper.validation.api;

import java.io.Serializable;

/**
 * Constraint Interface wrapping esper statements.
 * 
 * 
 * @author michvier
 *
 */
public interface IConstraint extends Serializable {

	String getCode();

	String getName();

	String getFile();

}
