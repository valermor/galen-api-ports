import json
import multiprocessing
import random
from time import sleep
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.remote.webdriver import WebDriver

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
import RemoteCommandExecutor


class GalenWebDriver(WebDriver):
    """
    This is implementation of WebDriver over Thrift which hides all the complexity of remoting commands over RPC
    and exposes the usual WebDriver API.
    Internally, GalenWebDriver makes use of an ad-hoc command_executor which remotes commands to RemoteWebDriver to
    the Thrift interface.
    """
    def __init__(self, remote_url='http://127.0.0.1:4444/wd/hub', desired_capabilities=None, browser_profile=None,
                 proxy=None, keep_alive=False):
        self.thrift = ThriftFacade().initialize(remote_url)
        remote_connection = GalenRemoteConnection(remote_url, self.thrift)
        WebDriver.__init__(self, remote_connection, desired_capabilities,
                           browser_profile, proxy, keep_alive)
        remote_connection.set_session_id(self.session_id)

    def quit(self):
        super(GalenWebDriver, self).quit()
        self.thrift.close_connection()


class ThriftFacade(object):
    """
    This class is a facade of the thrift client which hides all the details of the implementation and exposes only
    the methods needed by the command_executor implemented in GalenRemoteConnection.
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


class GalenRemoteConnection(RemoteConnection):
    """
    Subclass of RemoteConnection which execute commands over the Thrift interface.
    """
    def __init__(self, remote_server_addr, thrift_client, keep_alive=False):
        RemoteConnection.__init__(self, remote_server_addr, keep_alive)
        self.thrift_client = thrift_client
        self.session_id = None

    def execute(self, command, params):
        command_info = self._commands[command]
        assert command_info is not None, 'Unrecognised command %s' % command
        data = json.dumps(params)

        response = self.thrift_client.execute(self.session_id, command, data)
        return {'status': response.status, 'sessionId': response.session_id, 'state': response.state,
                'value': response.value.string_cap}

    def set_session_id(self, session_id):
        self.session_id = session_id


CHROME = {
    "browserName": "chrome",
    "version": "",
    "platform": "ANY"
}


class GalenApi(object):
    pass


def run_galen_test():
    driver1 = GalenWebDriver("http://localhost:4444/wd/hub", desired_capabilities=CHROME)
    driver1.get("http://www.google.it")
    driver1.set_window_size(720, 1024)

    driver2 = GalenWebDriver("http://localhost:4444/wd/hub", desired_capabilities=CHROME)
    driver2.get("http://www.repubblica.it")

    # GalenApi().check_layout(driver, "homePage.spec", ('iphone', 'tablet'), None, )
    driver1.quit()
    driver2.quit()

def execute_browser_session(order):
    print "Starting Session #{0}\n".format(str(order))
    sleep(int(random.random() * 10))
    driver = GalenWebDriver("http://localhost:4444/wd/hub", desired_capabilities=CHROME)
    print "Created Driver for Session #{0}\n".format(str(order))
    driver.get("http://www.google.it")
    print "Opened page for Session #{0}\n".format(str(order))
    driver.set_window_size(720, 1024)
    print "Set windows size for Session #{0}\n".format(str(order))
    driver.quit()
    print "Closed windows for Session #{0}\n".format(str(order))


def run_parallel_sessions():
    p = multiprocessing.Pool(5)
    p.map(execute_browser_session, range(5))


if __name__ == '__main__':
    # run_galen_test()
    run_parallel_sessions()