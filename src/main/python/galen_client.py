import json
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.remote.webdriver import WebDriver

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
import RemoteCommandExecutor


class GalenWebDriver(WebDriver):
    def __init__(self, remote_url='http://127.0.0.1:4444/wd/hub', desired_capabilities=None, browser_profile=None,
                 proxy=None, keep_alive=False):
        self.thrift = ThriftFacade().initialize(remote_url)
        WebDriver.__init__(self, GalenRemoteConnection(remote_url, self.thrift), desired_capabilities,
                           browser_profile, proxy, keep_alive)

    def quit(self):
        super(GalenWebDriver, self).quit()
        self.thrift.close_connection()

class ThriftFacade():
    def __init__(self):
        try:
            socket = TSocket.TSocket('localhost', 9091)
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

    def execute(self, command, request_params):
        return self.client.execute(command, request_params)

    def close_connection(self):
        self.transport.close()


class GalenRemoteConnection(RemoteConnection):
    def __init__(self, remote_server_addr, thrift_client, keep_alive=False):
        super(GalenRemoteConnection, self).__init__(remote_server_addr, keep_alive)
        self.thrift_client = thrift_client

    def execute(self, command, params):
        command_info = self._commands[command]
        assert command_info is not None, 'Unrecognised command %s' % command
        data = json.dumps(params)

        response = self.thrift_client.execute(command, data)
        return {'status': response.status, 'sessionId': response.session_id, 'state': response.state,
                'value': response.value.string_cap}


CHROME = {
    "browserName": "chrome",
    "version": "",
    "platform": "ANY"
}


class GalenApi(object):
    pass

driver1 = GalenWebDriver("http://localhost:4444/wd/hub", desired_capabilities=CHROME)
driver1.get("http://www.google.it")
driver1.set_window_size(720, 1024)

driver2 = GalenWebDriver("http://localhost:4444/wd/hub", desired_capabilities=CHROME)
driver2.get("http://www.repubblica.it")

# GalenApi().check_layout(driver, "homePage.spec", ('iphone', 'tablet'), None, )
driver1.quit()
driver2.quit()
