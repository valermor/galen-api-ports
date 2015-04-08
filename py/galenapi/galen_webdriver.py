import json
import logging
import multiprocessing
import random
from time import sleep

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.remote.webdriver import WebDriver

from pythrift.ttypes import RemoteWebDriverException
from galenapi.thrift_client import ThriftFacade


logger = logging.getLogger(__name__)


class GalenWebDriver(WebDriver):
    """
    This is implementation of RemoteWebDriver Client over Thrift. The commands to be sent to a remote Grid are intercepted
    and sent across the Thrift interface.
    Internally, GalenWebDriver makes use of GalenRemoteConnection, an ad-hoc command_executor which sends commands over
    the Thrift interface.
    """
    def __init__(self, remote_url='http://127.0.0.1:4444/wd/hub', desired_capabilities=None, browser_profile=None,
                 proxy=None, keep_alive=False):
        try:
            self.thrift_client = ThriftFacade().initialize(remote_url)
            remote_connection = ThriftRemoteConnection(remote_url, self.thrift_client)
            WebDriver.__init__(self, remote_connection, desired_capabilities,
                               browser_profile, proxy, keep_alive)
            remote_connection.set_session_id(self.session_id)
        except WebDriverException as e:
            logger.error(e.msg)
            self.thrift_client.shut_service_if_inactive()
            raise e

    def quit(self):
        super(GalenWebDriver, self).quit()
        self.thrift_client.shut_service_if_inactive()
        self.thrift_client.close_connection()


class ThriftRemoteConnection(RemoteConnection):
    """
    Subclass of RemoteConnection which execute commands over the Thrift interface.
    """
    def __init__(self, remote_server_addr, thrift_client, keep_alive=False):
        RemoteConnection.__init__(self, remote_server_addr, keep_alive)
        self.thrift_client = thrift_client
        self.session_id = None

    def execute(self, command, params):
        """
        Overrides execute methods by sending commands through the thrift interface.
        :param command: a selenium.webdriver.remote.Command object
        :param params: a list of parameters
        :return: a dict containing the response from the RemoteWebDriver service.
        """
        try:
            command_info = self._commands[command]
            assert command_info is not None, 'Unrecognised command %s' % command
            data = json.dumps(params)

            response = self.thrift_client.execute(self.session_id, command, data)
            return {'status': response.status, 'sessionId': response.session_id, 'state': response.state,
                    'value': response.value.string_cap}
        except RemoteWebDriverException as e:
            raise WebDriverException(e.message)

    def set_session_id(self, session_id):
        self.session_id = session_id
