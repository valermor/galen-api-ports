package net.skyscanner.galen.api;

import org.apache.thrift.TException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.remote.*;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;

import static com.google.common.collect.Maps.newHashMap;
import static net.skyscanner.galen.api.GsonUtils.getGson;
import static net.skyscanner.galen.api.ResponseValueType.string_cap;
import static org.openqa.selenium.remote.ErrorCodes.SESSION_NOT_CREATED;
import static org.openqa.selenium.remote.ErrorCodes.SUCCESS;

public class GalenCommandExecutor implements RemoteCommandExecutor.Iface {

    private String remoteServerAddr;

    @Override
    public void initialize(String remoteServerAddr) throws TException {
        this.remoteServerAddr = remoteServerAddr;
    }

    @Override
    public Response execute(String sessionId,  String name, String params) throws TException {
        Map<String, Object> paramsAsMap = fromJsonToStringObjectMap(params);
        if (name.equals(DriverCommand.NEW_SESSION)) {
            try {
                HashMap<String, Object> hashMap = transformDesiredCapabilities(paramsAsMap);
                WebDriver driver = new RemoteWebDriver(new URL(remoteServerAddr), new DesiredCapabilities(hashMap));
                DriversPool.get().set(driver);
                return createSuccessResponse(driver);
            } catch (MalformedURLException e) {
                createFailureResponse();
                //TODO add logging
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
                    DriversPool.get().clear(sessionId);
                }
                return new Response(string_cap(getGson().toJson(response.getValue())), response.getSessionId(),
                        response.getStatus(), response.getState());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    /**
     * Transform a json String into a map of Object indexed by a String value.
     * This is needed to feed Command and DesideredCapabilities constructor.
     */
    private Map<String, Object> fromJsonToStringObjectMap(String params) {
        return getGson().<Map<String, Object>>fromJson(params, Object.class);
    }

    private Response createSuccessResponse(WebDriver driver) {
        Response response = new Response();
        response.setStatus(SUCCESS);
        RemoteWebDriver remoteDriver = (RemoteWebDriver) driver;
        response.setValue(string_cap(getGson().toJson(remoteDriver.getCapabilities().asMap())));
        response.setSession_id(remoteDriver.getSessionId().toString());
        response.setState(new ErrorCodes().toState(SUCCESS));
        return response;
    }

    private Response createFailureResponse() {
        Response response = new Response();
        response.setStatus(SESSION_NOT_CREATED);
        response.setState(new ErrorCodes().toState(SESSION_NOT_CREATED));
        return response;
    }

    private static HashMap<String, Object> transformDesiredCapabilities(Map<String, Object> paramsAsMap) {
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
