import logging
from time import sleep
from thrift import Thrift
from thrift.Thrift import TApplicationException
from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport
from galenthrift import RemoteCommandExecutor
from galenthrift.ttypes import SpecNotFoundException

from thrift_service_lifecycle import start_server, stop_server

REMOTE_COMMAND_EXECUTOR_SERVICE_PORT = 9092

logger = logging.getLogger(__name__)


class ThriftFacade(object):
    """
    This class implements a facade of the thrift_generated client which hides all the details of the thrift implementation
    and exposes the methods needed by the command_executor implemented in GalenRemoteConnection as well as the Galen API.
    """
    def __init__(self):
        try:
            start_command_executor_service(REMOTE_COMMAND_EXECUTOR_SERVICE_PORT)
            sleep(3)
            socket = TSocket.TSocket('localhost', REMOTE_COMMAND_EXECUTOR_SERVICE_PORT)
            self.transport = TTransport.TFramedTransport(socket)
            protocol_factory = TBinaryProtocol.TBinaryProtocolFactory()
            protocol = protocol_factory.getProtocol(self.transport)
            self.client = RemoteCommandExecutor.Client(protocol)
            self.transport.open()
        except Thrift.TException, tx:
            stop_server(REMOTE_COMMAND_EXECUTOR_SERVICE_PORT)
            raise Exception('%s' % (tx.message))

    def initialize(self, remote_url):
        self.client.initialize(remote_url)
        return self

    def execute(self, session_id, command, request_params):
        return self.client.execute(session_id, command, request_params)

    def close_connection(self):
        self.transport.close()
        stop_command_executor_service(REMOTE_COMMAND_EXECUTOR_SERVICE_PORT)

    def check_api(self, test_name, driver_session_id, spec_name, included_tags, excluded_tags):
        try:
            self.client.check_layout(test_name, driver_session_id, spec_name, included_tags, excluded_tags)
        except SpecNotFoundException as e:
        # except Exception as e:
            logger.error(e.message)
            raise SpecNotFoundException(e)

    def generate_report(self, report_folder_path):
        self.client.generate_report(report_folder_path)


def start_command_executor_service(server_port):
    """
    Start CommandExecutor thrift service on the given port.
    """
    # start_server(server_port)
    pass

def stop_command_executor_service(server_port):
    # stop_server(server_port)
    pass
