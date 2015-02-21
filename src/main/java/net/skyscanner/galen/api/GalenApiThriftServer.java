package net.skyscanner.galen.api;

import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.server.TServer;
import org.apache.thrift.server.TThreadPoolServer;
import org.apache.thrift.server.TThreadedSelectorServer;
import org.apache.thrift.transport.*;

import java.util.concurrent.ExecutorService;

import static net.skyscanner.galen.api.RemoteCommandExecutor.Processor;

public class GalenApiThriftServer {

    public static GalenCommandExecutor handler;

    public static RemoteCommandExecutor.Processor processor;

    public static void main(String [] args) {
        handler = new GalenCommandExecutor();
        processor = new Processor(handler);
        runService(processor);
    }

    public static void runService(RemoteCommandExecutor.Processor processor) {
        try {
            TNonblockingServerTransport serverTransport = new TNonblockingServerSocket(9092);
            TThreadedSelectorServer.Args args = new TThreadedSelectorServer.Args(serverTransport);
            TServer server = new TThreadedSelectorServer(args.processor(processor));
            System.out.println("Starting the server...");
            server.serve();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
