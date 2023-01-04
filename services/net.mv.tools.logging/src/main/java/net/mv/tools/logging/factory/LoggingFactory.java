package net.mv.tools.logging.factory;

import net.mv.tools.logging.ILogger;
import net.mv.tools.logging.log4j2.Log4Jv2Logger;


public class LoggingFactory {



	public static ILogger getLogger(Class<?> clazz) {
		return new Log4Jv2Logger(clazz);
	}
}
