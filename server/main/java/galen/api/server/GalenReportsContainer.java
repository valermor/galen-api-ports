/***************************************************************************
 * Copyright 2015 Valerio Morsella                                          *
 *                                                                          *
 * Licensed under the Apache License, Version 2.0 (the "License");          *
 * you may not use this file except in compliance with the License.         *
 * You may obtain a copy of the License at                                  *
 *                                                                          *
 *    http://www.apache.org/licenses/LICENSE-2.0                            *
 *                                                                          *
 * Unless required by applicable law or agreed to in writing, software      *
 * distributed under the License is distributed on an "AS IS" BASIS,        *
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. *
 * See the License for the specific language governing permissions and      *
 * limitations under the License.                                           *
 ***************************************************************************/

package galen.api.server;

import com.google.common.collect.Lists;
import net.mindengine.galen.reports.GalenTestInfo;
import net.mindengine.galen.reports.TestReport;
import net.mindengine.galen.reports.model.LayoutReport;

import java.lang.reflect.Method;
import java.util.*;

import static net.mindengine.galen.reports.GalenTestInfo.fromString;

public class GalenReportsContainer {

    private static final GalenReportsContainer _instance = new GalenReportsContainer();
    private final Map<String, GalenTestInfo> tests = new HashMap<String, GalenTestInfo>();
    private final Map<String, LayoutReport> reports = new HashMap<String, LayoutReport>();

    private GalenReportsContainer() {
    }

    public static final GalenReportsContainer get() {
        return _instance;
    }

    public GalenTestInfo registerTest(String testName) {
        GalenTestInfo galenTestInfo = fromString(testName);

        tests.put(testName, galenTestInfo);
        return galenTestInfo;
    }

    public GalenTestInfo getTestWithName(String name) {
        return tests.get(name);
    }

    public void updateEndTime(String testName) {
        GalenTestInfo testInfo = tests.get(testName);
        testInfo.setEndedAt(new Date());
    }

    public List<GalenTestInfo> getAllTests() {
        return Lists.newArrayList(tests.values());
    }

    public void storeLayoutReport(String reportId, LayoutReport layoutReport) {
        reports.put(reportId, layoutReport);
    }

    public LayoutReport fetchLayoutReport(String reportId) {
        return reports.get(reportId);
    }
}
