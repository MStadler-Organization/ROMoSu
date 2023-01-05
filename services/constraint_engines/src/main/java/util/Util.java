package util;

import java.text.SimpleDateFormat;

public class Util {

	/**
	 * Creates a current timestamp string
	 * 
	 * @return the timestamp as string in the format yyyy.MM.dd \t HH:mm:ss.SSS
	 */
	public static String getTimestampString() {
		return new SimpleDateFormat("yyyy.MM.dd \t HH:mm:ss.SSS").format(new java.util.Date());
	}
}
