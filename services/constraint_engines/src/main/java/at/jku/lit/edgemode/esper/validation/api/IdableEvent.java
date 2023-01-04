
package at.jku.lit.edgemode.esper.validation.api;

/**
 * 
 * Base interface for all events sent to the esper engine - so that violations
 * can be assigned to a specific event id.
 * 
 * @author michvier
 *
 */
public interface IdableEvent {

	String getId();

	void setId(String value);

}