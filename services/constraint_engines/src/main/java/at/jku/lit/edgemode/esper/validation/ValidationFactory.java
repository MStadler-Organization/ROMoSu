package at.jku.lit.edgemode.esper.validation;

import at.jku.lit.edgemode.esper.validation.api.IConstraint;
import at.jku.lit.edgemode.esper.validation.api.IViolation;
import at.jku.lit.edgemode.esper.validation.impl.Constraint;
import at.jku.lit.edgemode.esper.validation.impl.Violation;

/**
 * 
 * Factory class for violations and constraints.
 * 
 * 
 * @author michvier
 *
 */
public class ValidationFactory {

	public static IViolation createViolation(String id, IConstraint constraint, Object underlying) {
		return new Violation(id, constraint, underlying.getClass(), underlying.toString());
	}

	public static IConstraint createConstraint(String file, String name, String code) {
		return new Constraint(file, name, code);
	}

}
