package galen.api.server.utils;
import java.util.UUID;

public class StringUtils {

    public static String generateUniqueString() {
        String uniqueKey = UUID.randomUUID().toString();
        return uniqueKey.replaceAll("-", "");
    }
}
