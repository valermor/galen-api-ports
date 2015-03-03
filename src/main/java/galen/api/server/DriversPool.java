package galen.api.server;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.remote.RemoteWebDriver;

import java.util.ArrayList;
import java.util.List;

import static java.lang.String.format;

public class DriversPool {
    /**
     * Utility class which stores current pool of drivers.
     */
    private static final DriversPool instance = new DriversPool();
    private final List<WebDriver> driversPool = new ArrayList<WebDriver>();

    private DriversPool() {
    }

    public static final DriversPool get() {
        return instance;
    }

    public void set(WebDriver driver) {
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
        driversPool.remove(this.getBySessionId(sessionId));
    }

    public int hasDrivers() {
        return driversPool.size();
    }
}
