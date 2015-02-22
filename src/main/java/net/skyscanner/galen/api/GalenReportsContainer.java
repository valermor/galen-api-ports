package net.skyscanner.galen.api;

import net.mindengine.galen.reports.GalenTestInfo;
import net.mindengine.galen.reports.TestReport;

import java.lang.reflect.Method;
import java.util.Date;
import java.util.LinkedList;
import java.util.List;

import static net.mindengine.galen.reports.GalenTestInfo.fromString;

public class GalenReportsContainer {

    private static final GalenReportsContainer _instance = new GalenReportsContainer();
    private final List<GalenTestInfo> tests = new LinkedList<GalenTestInfo>();

    private GalenReportsContainer() {
    }

    public static final GalenReportsContainer get() {
        return _instance;
    }

    public TestReport registerTest(String testInfo) {
        GalenTestInfo galenTestInfo = fromString(testInfo);

        tests.add(galenTestInfo);
        return galenTestInfo.getReport();
    }

    public void updateEndTime(String actualTestInfo) {
        GalenTestInfo galenTestInfo = fromString(actualTestInfo);
        for (GalenTestInfo testInfo : tests) {
            if (testInfo.getName().equals(galenTestInfo.getName())) {
                testInfo.setEndedAt(new Date());
            }
        }
    }

    public List<GalenTestInfo> getAllTests() {
        return tests;
    }

    private String createNameFromTestInfo(Method method, String config) {
        return method.getDeclaringClass().getName()+ "_" + method.getName() + "_" + config;
    }
}
