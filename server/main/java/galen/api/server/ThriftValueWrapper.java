package galen.api.server;

import galen.api.server.thrift.ResponseValueNew;
import galen.api.server.thrift.Value;
import org.testng.collections.Lists;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static galen.api.server.utils.StringUtils.generateUniqueString;

public class ThriftValueWrapper {

    private ResponseValueNew wrappedValue;
    private List<ResponseValueNew> containedValues;

    public ThriftValueWrapper(Object value) {
        containedValues = new ArrayList<ResponseValueNew>();
        wrappedValue = parseValue(value);
    }

    public ResponseValueNew getValue() {
        return wrappedValue;
    }

    public List<ResponseValueNew> getContainedValues() {
        return containedValues;
    }

    private ResponseValueNew parseValue(Object value) {
        ResponseValueNew responseValue = new ResponseValueNew();
        responseValue.setValue_id(generateUniqueString());
        Value valueType = new Value();
        if (value == null) {
            return responseValue;
        } else if (value instanceof Integer) {
            valueType.setInt_value((Integer) value);
        } else if (value instanceof String) {
            valueType.setString_value((String) value);
        } else if (value instanceof Boolean) {
            valueType.setBoolean_value((Boolean) value);
        } else if (value instanceof Long) {
            valueType.setWrapped_long_value((Long.toString((Long) value)));
        } else if (value instanceof Map) {
            Map<String, String> transformedMap = new HashMap<String, String>();
            Map<String, ?> items = (Map<String, ?>) value;
            for (Map.Entry<String, ?> item : items.entrySet()) {
                ResponseValueNew parsedValue = parseValue(item.getValue());
                transformedMap.put(item.getKey(), parsedValue.getValue_id());
                containedValues.add(parsedValue);
            }
            valueType.setMap_values(transformedMap);
        } else if (value instanceof List) {
        List<String> transformedList = Lists.newArrayList();
            for (Object item : (List<Object>) value) {
                ResponseValueNew parsedValue = parseValue(item);
                transformedList.add(parsedValue.getValue_id());
                containedValues.add(parsedValue);
            }
            valueType.setList_values(transformedList);
        } else {
            valueType.setString_value(value.toString());
        }
        responseValue.setValue(valueType);
        return responseValue;
    }
}
