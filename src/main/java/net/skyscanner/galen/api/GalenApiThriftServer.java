package net.skyscanner.galen.api;

import org.apache.thrift.server.TServer;
import org.apache.thrift.server.TSimpleServer;
import org.apache.thrift.transport.TServerSocket;
import org.apache.thrift.transport.TServerTransport;

import static net.skyscanner.galen.api.RemoteCommandExecutor.Processor;

public class GalenApiThriftServer {

    public static GalenCommandExecutor handler;

    public static RemoteCommandExecutor.Processor processor;

    public static void main(String [] args) {
        try {
            handler = new GalenCommandExecutor();
            processor = new Processor(handler);

            Runnable simple = new Runnable() {
                public void run() {
                    simple(processor);
                }
            };

            new Thread(simple).start();
        } catch (Exception x) {
            x.printStackTrace();
        }
    }

    public static void simple(RemoteCommandExecutor.Processor processor) {
        try {
            TServerTransport serverTransport = new TServerSocket(9091);
            TServer server = new TSimpleServer(new TServer.Args(serverTransport).processor(processor));

            System.out.println("Starting the simple server...");
            server.serve();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
