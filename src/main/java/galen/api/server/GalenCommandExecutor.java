package galen.api.server;

import galen.api.server.thrift.RemoteBrowserException;
import galen.api.server.thrift.RemoteCommandExecutor;
import galen.api.server.thrift.Response;
import net.mindengine.galen.api.Galen;
import net.mindengine.galen.parser.FileSyntaxException;
import net.mindengine.galen.reports.GalenTestInfo;
import net.mindengine.galen.reports.HtmlReportBuilder;
import net.mindengine.galen.reports.TestReport;
import net.mindengine.galen.reports.model.LayoutReport;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.thrift.TException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.remote.*;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.*;

import static com.google.common.collect.Maps.newHashMap;
import static galen.api.server.GsonUtils.getGson;
import static galen.api.server.thrift.ResponseValueType.string_cap;
import static org.openqa.selenium.remote.ErrorCodes.SESSION_NOT_CREATED;
import static org.openqa.selenium.remote.ErrorCodes.SUCCESS;

public class GalenCommandExecutor implements RemoteCommandExecutor.Iface {
    /**
     * Implementation of RemoteCommandExecutor interface.
     */

    private Log log = LogFactory.getLog(GalenApiServer.class);

    private String remoteServerAddress;

    @Override
    public void initialize(String remoteServerAddress) throws TException {
        this.remoteServerAddress = remoteServerAddress;
    }

    @Override
    public Response execute(String sessionId, String name, String params) throws TException {
        Map<String, Object> paramsAsMap = fromJsonToStringObjectMap(params);
        if (name.equals(DriverCommand.NEW_SESSION)) {
            try {
                HashMap<String, Object> hashMap = extractDesiredCapabilities(paramsAsMap);
                WebDriver driver = new RemoteWebDriver(new URL(remoteServerAddress), new DesiredCapabilities(hashMap));
                DriversPool.get().set(driver);
                return createSessionInitSuccessResponse(driver);
            } catch (MalformedURLException e) {
                createSessionInitFailureResponse();
                log.error("Provided URL is malformed " + remoteServerAddress);
                throw new RemoteBrowserException("Provided URL is malformed " + remoteServerAddress);
            } catch (UnreachableBrowserException e) {
                createSessionInitFailureResponse();
                log.error("Could not reach browser at URL " + remoteServerAddress + " check remote server is running.");
                    throw new RemoteBrowserException("Could not reach browser at URL " + remoteServerAddress + " check remote server is running.");
            }
        }
        Command command = new Command(new SessionId(sessionId), name, paramsAsMap);
        try {
            WebDriver driver = DriversPool.get().getBySessionId(sessionId);
            org.openqa.selenium.remote.Response response = null;
            if (driver instanceof RemoteWebDriver) {
                response = ((RemoteWebDriver) driver).getCommandExecutor().execute(command);
            }
            if (response == null) {
                return null;
            } else {
                if (name.equals(DriverCommand.QUIT)) {
                    DriversPool.get().removeDriverBySessionId(sessionId);
                }
                return new Response(string_cap(getGson().toJson(response.getValue())), response.getSessionId(),
                        response.getStatus(), response.getState());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    @Override
    public int check_layout(String testName, String driverSessionId, String specs, List<String> includedTags, List<String> excludedTags) throws SpecNotFoundException {
        WebDriver driver = DriversPool.get().getBySessionId(driverSessionId);
        try {
            TestReport testReport = GalenReportsContainer.get().registerTest(testName);
            LayoutReport layoutReport = Galen.checkLayout(driver, specs, includedTags, excludedTags, new Properties(), null);
            testReport.layout(layoutReport, "Check layout " + specs);
            GalenReportsContainer.get().updateEndTime(testName);
            return layoutReport.errors();
        } catch (FileSyntaxException e) {
            log.error("Could not find spec file " + specs);
            throw new SpecNotFoundException(e.getMessage());
        } catch (IOException e) {
            e.printStackTrace();
        }
        return 0;
    }

    @Override
    public void generate_report(String reportFolderPath) throws TException {
        List<GalenTestInfo> tests = GalenReportsContainer.get().getAllTests();
        try {
            new HtmlReportBuilder().build(tests, reportFolderPath);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * Transform a json String into a map of Object indexed by a String value.
     * This is needed to feed Command and DesideredCapabilities constructor.
     */
    private Map<String, Object> fromJsonToStringObjectMap(String params) {
        return getGson().<Map<String, Object>>fromJson(params, Object.class);
    }

    /**
     * Packages a successful session setup response which can be sent across the Thrift interface.
     */
    private Response createSessionInitSuccessResponse(WebDriver driver) {
        Response response = new Response();
        response.setStatus(SUCCESS);
        RemoteWebDriver remoteDriver = (RemoteWebDriver) driver;
        response.setValue(string_cap(getGson().toJson(remoteDriver.getCapabilities().asMap())));
        response.setSession_id(remoteDriver.getSessionId().toString());
        response.setState(new ErrorCodes().toState(SUCCESS));
        return response;
    }

    /**
     * Packages a failing session setup response which can be sent across the Thrift interface.
     */
    private Response createSessionInitFailureResponse() {
        Response response = new Response();
        response.setStatus(SESSION_NOT_CREATED);
        response.setState(new ErrorCodes().toState(SESSION_NOT_CREATED));
        return response;
    }

    /**
     * Extract desired capabilities from json document as received over Thrift interface into a HashMap
     * where the key set is the names of the capabilities.
     */
    private static HashMap<String, Object> extractDesiredCapabilities(Map<String, Object> paramsAsMap) {
        Map<String, Object> desiredCapabilities;
        if (paramsAsMap.containsKey("desiredCapabilities")) {
            desiredCapabilities = (Map<String, Object>) paramsAsMap.get("desiredCapabilities");
        } else {
            throw new IllegalStateException("New session does not contain desired capabilities.");
        }
        HashMap<String, Object> hashMap = newHashMap();
        Set<String> keySet = desiredCapabilities.keySet();
        for (String key : keySet) {
            hashMap.put(key, desiredCapabilities.get(key));
        }
        return hashMap;
    }
}
