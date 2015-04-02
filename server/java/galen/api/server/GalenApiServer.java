package galen.api.server;

import galen.api.server.thrift.GalenApiRemoteService;
import org.apache.commons.cli.*;
import org.apache.thrift.server.TServer;
import org.apache.thrift.server.TThreadedSelectorServer;
import org.apache.thrift.transport.TNonblockingServerSocket;
import org.apache.thrift.transport.TNonblockingServerTransport;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import static java.lang.Integer.valueOf;
import static java.util.Arrays.asList;

public class GalenApiServer {

    private static Logger log = LoggerFactory.getLogger(GalenApiServer.class);

    public static GalenCommandExecutor handler;
    public static GalenApiRemoteService.Processor processor;

    public static void main(String [] args) {
        CommandLineParser parser = new GnuParser();
        Options options = defineCommandOptions();
        HelpFormatter formatter = new HelpFormatter();
        try {
            CommandLine commandLine = parser.parse(options, args);

            if (asList(args).size() == 0) {
                formatter.printHelp("galen-api-server", options);
                System.exit(0);
            } else if (commandLine.hasOption("help")) {
                formatter.printHelp("galen-api-server", options);
            } else if (commandLine.hasOption("run")) {
                String port = commandLine.getOptionValue("run");
                int serverPort = valueOf(port);
                handler = new GalenCommandExecutor();
                processor = new GalenApiRemoteService.Processor(handler);
                log.info("Starting server on port " + serverPort);
                runService(processor, serverPort);

            }
        } catch (ParseException e) {
            System.out.print("Invalid usage: ");
            System.out.println(e.getMessage());
            formatter.printHelp("galen-api-server", options);
        }
    }

    private static Options defineCommandOptions() {
        Option helpOption = new Option("help", "h", false, "explains usage");
        Option runOption = OptionBuilder.hasArg()
                .withArgName("port")
                .withDescription("Runs the server on specified port")
                .withLongOpt("r")
                .create("run");

        Options options = new Options();
        options.addOption(helpOption).addOption(runOption);
        return options;
    }

    public static void runService(GalenApiRemoteService.Processor processor, int serverPort) {
        try {
            TNonblockingServerTransport serverTransport = new TNonblockingServerSocket(serverPort);
            TThreadedSelectorServer.Args args = new TThreadedSelectorServer.Args(serverTransport);
            TServer server = new TThreadedSelectorServer(args.processor(processor));
            server.serve();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
