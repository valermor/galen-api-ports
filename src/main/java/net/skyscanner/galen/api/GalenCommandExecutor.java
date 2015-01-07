package net.skyscanner.galen.api;

import com.google.common.collect.Maps;
import org.apache.thrift.TException;
import org.openqa.selenium.remote.*;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;

import static net.skyscanner.galen.api.GsonUtils.getGson;
import static net.skyscanner.galen.api.ResponseValueType.string_cap;
import static org.openqa.selenium.remote.ErrorCodes.SESSION_NOT_CREATED;
import static org.openqa.selenium.remote.ErrorCodes.SUCCESS;

public class GalenCommandExecutor implements RemoteCommandExecutor.Iface {

    private RemoteWebDriver driver;
    private CommandExecutor commandExecutor;
    private SessionId sessionId;
    private String remoteServerAddr;

    @Override
    public void initialize(String remoteServerAddr, String desiredCapabilities) throws TException {
        this.remoteServerAddr = remoteServerAddr;
    }

    @Override
    public Response execute(String name, String params) throws TException {
        Map<String, Object> paramsAsMap = (Map<String, Object>) getGson().fromJson(params, Object.class);
        if (name.equals(DriverCommand.NEW_SESSION)) {
            try {
                HashMap<String, Object> hashMap = transformDesiredCapabilities(paramsAsMap);
                driver = new RemoteWebDriver(new URL(remoteServerAddr), new DesiredCapabilities(hashMap));
                commandExecutor = driver.getCommandExecutor();
                sessionId = driver.getSessionId();
                return createSuccessResponse();
            } catch (MalformedURLException e) {
                createFailureResponse();
                //TODO add logging
            }
        }
        Command command = new Command(sessionId, name, paramsAsMap);
        try {
            org.openqa.selenium.remote.Response response = commandExecutor.execute(command);
            if (response == null) {
                return null;
            }
            return new Response(string_cap(getGson().toJson(response.getValue())), response.getSessionId(),
                    response.getStatus(), response.getState());
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    private Response createSuccessResponse() {
        Response response = new Response();
        response.setStatus(SUCCESS);
        response.setValue(string_cap(getGson().toJson(driver.getCapabilities().asMap())));
        response.setSession_id(sessionId.toString());
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
        HashMap<String, Object> hashMap = Maps.newHashMap();
        Set<String> keySet = desiredCapabilities.keySet();
        for (String key : keySet) {
            hashMap.put(key, desiredCapabilities.get(key));
        }
        return hashMap;
    }
}
