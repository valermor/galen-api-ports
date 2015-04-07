package galen.api.server;

import net.mindengine.galen.reports.GalenTestInfo;
import net.mindengine.galen.reports.TestReport;
import net.mindengine.galen.reports.model.LayoutReport;

import java.lang.reflect.Method;
import java.util.*;

import static net.mindengine.galen.reports.GalenTestInfo.fromString;

public class GalenReportsContainer {

    private static final GalenReportsContainer _instance = new GalenReportsContainer();
    private final List<GalenTestInfo> tests = new LinkedList<GalenTestInfo>();
    private final Map<String, LayoutReport> reports = new HashMap<String, LayoutReport>();

    private GalenReportsContainer() {
    }

    public static final GalenReportsContainer get() {
        return _instance;
    }

    public GalenTestInfo registerTest(String testInfo) {
        GalenTestInfo galenTestInfo = fromString(testInfo);

        tests.add(galenTestInfo);
        return galenTestInfo;
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

    public void storeLayoutReport(String reportId, LayoutReport layoutReport) {
        reports.put(reportId, layoutReport);
    }

    public LayoutReport fetchLayoutReport(String reportId) {
        return reports.get(reportId);
    }
}
