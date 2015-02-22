from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
import RemoteCommandExecutor
from ttypes import SpecNotFoundException


class ThriftFacade(object):
    """
    This class is a facade of the thrift client which hides all the details of the implementation and exposes only
    the methods needed by the command_executor implemented in GalenRemoteConnection as well as the Galen API.
    """
    def __init__(self):
        try:
            socket = TSocket.TSocket('localhost', 9092)
            self.transport = TTransport.TFramedTransport(socket)
            protocol_factory = TBinaryProtocol.TBinaryProtocolFactory()
            protocol = protocol_factory.getProtocol(self.transport)
            self.client = RemoteCommandExecutor.Client(protocol)
            self.transport.open()
        except Thrift.TException, tx:
            print '%s' % (tx.message)

    def initialize(self, remote_url):
        self.client.initialize(remote_url)
        return self

    def execute(self, session_id, command, request_params):
        return self.client.execute(session_id, command, request_params)

    def close_connection(self):
        self.transport.close()

    def check_api(self, test_name, driver_session_id, spec_name, included_tags, excluded_tags):
        try:
            self.client.check_layout(test_name, driver_session_id, spec_name, included_tags, excluded_tags)
        except SpecNotFoundException as e:
            raise SpecNotFoundException(e)

    def generate_report(self, report_folder_path):
        self.client.generate_report(report_folder_path)