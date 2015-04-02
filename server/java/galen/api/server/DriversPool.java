package galen.api.server;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;

import static galen.api.server.utils.DriverUtils.getSessionId;
import static java.lang.String.format;

/**
 * Utility class to store and retrieve instances of RemoteWebdriver.
 */
public class DriversPool {
    private Logger log = LoggerFactory.getLogger(DriversPool.class);
    private static final DriversPool instance = new DriversPool();
    private final List<WebDriver> driversPool = new ArrayList<WebDriver>();

    private DriversPool() {
    }

    public static final DriversPool get() {
        return instance;
    }

    public void set(WebDriver driver) {
        log.debug("Storing WebDriver instance with sessionId " + getSessionId(driver));
        if (!driversPool.contains(driver)) {
            driversPool.add(driver);
        }
    }

    public WebDriver getBySessionId(String sessionId) {
        for (WebDriver driver : driversPool) {
            if (driver instanceof RemoteWebDriver) {
                if (((RemoteWebDriver) driver).getSessionId().toString().equals(sessionId)) {
                    return driver;
                }
            }
        }
        throw new IllegalStateException(format("Driver with session id %s has never been created", sessionId));
    }

    public void removeDriverBySessionId(String sessionId) {
        log.debug("Removing WebDriver instance with sessionId " + sessionId);
        driversPool.remove(this.getBySessionId(sessionId));
    }

    public int activeDrivers() {
        return driversPool.size();
    }
}
