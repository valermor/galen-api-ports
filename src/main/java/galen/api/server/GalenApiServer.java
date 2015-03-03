package galen.api.server;

import galen.api.server.thrift.RemoteCommandExecutor;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.thrift.server.TServer;
import org.apache.thrift.server.TThreadedSelectorServer;
import org.apache.thrift.transport.TNonblockingServerSocket;
import org.apache.thrift.transport.TNonblockingServerTransport;

import java.util.ArrayList;

import static com.google.common.collect.Lists.newArrayList;
import static galen.api.server.thrift.RemoteCommandExecutor.Processor;
import static java.lang.Integer.valueOf;

public class GalenApiServer {

    private static Log log = LogFactory.getLog(GalenApiServer.class);

    public static final int SERVER_DEFAULT_PORT = 9092;
    public static GalenCommandExecutor handler;
    public static RemoteCommandExecutor.Processor processor;

    public static void main(String [] args) {
        ArrayList<String> argsList = newArrayList(args);
        int serverPort = SERVER_DEFAULT_PORT;
        if (!argsList.isEmpty()) {
            serverPort = valueOf(argsList.get(0));
        }
        //TODO add command to query current number of drivers.
        //TODO add command to stop server instead of kill -9.
        handler = new GalenCommandExecutor();
        processor = new Processor(handler);
        runService(processor, serverPort);
    }

    public static void runService(RemoteCommandExecutor.Processor processor, int serverPort) {
        try {
            TNonblockingServerTransport serverTransport = new TNonblockingServerSocket(serverPort);
            TThreadedSelectorServer.Args args = new TThreadedSelectorServer.Args(serverTransport);
            TServer server = new TThreadedSelectorServer(args.processor(processor));
            log.info("Starting server on port " + serverPort);
            server.serve();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
