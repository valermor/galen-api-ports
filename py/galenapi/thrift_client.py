import logging
from time import sleep

from thrift import Thrift
from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport
from thrift.transport.TTransport import TTransportException

from pythrift import GalenApiRemoteService
from pythrift.ttypes import SpecNotFoundException
from galenapi.remote_service_lifecycle import start_server, stop_server


GALEN_REMOTE_API_SERVICE_DEFAULT_PORT = 9092

""" RESILIENCE_INTERVAL specifies after which amount of time (in seconds) we can assume there is no activity in the remote
    server so that we are allowed to quit it."""
RESILIENCE_INTERVAL = 5

logger = logging.getLogger(__name__)


class ThriftFacade(object):
    """
    This class implements a facade of the thrift_generated client which hides all the details of the thrift
    implementation and exposes the methods needed by the command_executor implemented in GalenRemoteConnection as well
    as the Galen API.
    """
    def __init__(self, service_port=GALEN_REMOTE_API_SERVICE_DEFAULT_PORT):
        try:
            start_galen_remote_api_service(service_port)
            sleep(3) #TODO Implement wait until server is running
            socket = TSocket.TSocket('localhost', service_port)
            self.transport = TTransport.TFramedTransport(socket)
            protocol_factory = TBinaryProtocol.TBinaryProtocolFactory()
            protocol = protocol_factory.getProtocol(self.transport)
            self.client = GalenApiRemoteService.Client(protocol)
            self.transport.open()
        except Thrift.TException, tx:
            stop_galen_remote_api_service(GALEN_REMOTE_API_SERVICE_DEFAULT_PORT)
            raise Exception('%s' % (tx.message))

    def initialize(self, remote_url):
        self.client.initialize(remote_url)
        return self

    def execute(self, session_id, command, request_params):
        return self.client.execute(session_id, command, request_params)

    def close_connection(self):
        self.transport.close()

    def shut_service_if_inactive(self):
        sleep(RESILIENCE_INTERVAL)
        if self.get_active_drivers() == 0:
            self.shut_service()

    def get_active_drivers(self):
        return self.client.active_drivers()

    def shut_service(self):
        try:
            self.client.shut_service()
        except TTransportException:
            pass

    def register_test(self, test_name):
        self.client.register_test(test_name)

    def check_layout(self, driver_session_id, spec_name, included_tags, excluded_tags):
        try:
            return self.client.check_layout(driver_session_id, spec_name, included_tags, excluded_tags)
        except SpecNotFoundException as e:
            logger.error(e.message)
            raise SpecNotFoundException(e)

    def finalize(self, test_name, report):
        try:
            self.client.append(test_name, report)
        except Exception as e:
            logger.error(e)
            raise e

    def generate_report(self, report_folder_path):
        self.client.generate_report(report_folder_path)


def start_galen_remote_api_service(server_port):
    """
    Start CommandExecutor thrift service on the given port.
    """
    start_server(server_port)


def stop_galen_remote_api_service(server_port):
    stop_server(server_port)
