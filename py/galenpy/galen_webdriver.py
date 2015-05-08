############################################################################
# Copyright 2015 Valerio Morsella                                          #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License");          #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#    http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
############################################################################

import json
import logging

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.remote.webdriver import WebDriver

from galenpy.thrift_client import ThriftClient
from pythrift.ttypes import RemoteWebDriverException


logger = logging.getLogger()


class GalenRemoteWebDriver(WebDriver):
    """
    Implementation of Galen RemoteWebDriver which uses JsonWire protocol over Thrift. The commands to be sent
    to a remote Grid are intercepted and sent across the Thrift interface.
    Internally, GalenRemoteWebDriver makes use of ThriftRemoteConnection, an ad-hoc command_executor which sends commands
    over the Thrift interface.
    """
    def __init__(self, remote_url='http://127.0.0.1:4444/wd/hub', desired_capabilities=None, browser_profile=None,
                 proxy=None, keep_alive=False):
        try:
            self.thrift_client = ThriftClient().initialize(remote_url)
            remote_connection = ThriftRemoteConnection(remote_url, self.thrift_client)
            WebDriver.__init__(self, remote_connection, desired_capabilities,
                               browser_profile, proxy, keep_alive)
            remote_connection.set_session_id(self.session_id)
        except WebDriverException as e:
            logger.error(e.msg)
            self.thrift_client.quit_service_if_inactive()
            raise e

    def quit(self):
        super(GalenRemoteWebDriver, self).quit()


class ThriftRemoteConnection(RemoteConnection):
    """
    Subclass of RemoteConnection which implements JsonWire protocol over Thrift Interface.
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
            response_value = ''
            if response.response_value:
                response_value = unwrap_response_value(response.response_value.value, response.contained_values)
            return dict(status=response.status, sessionId=response.session_id, state=response.state, value=response_value)
        except RemoteWebDriverException as e:
            raise WebDriverException(e.message)

    def set_session_id(self, session_id):
        self.session_id = session_id


def unwrap_response_value(value, contained_values):
    if value is None:
        return None
    elif value.int_value:
        return value.int_value
    elif value.string_value or value.string_value == '':
        return value.string_value
    elif value.boolean_value is not None:
        return value.boolean_value
    elif value.wrapped_long_value:
        return long(value.wrapped_long_value)
    elif value.map_values:
        unwrapped_dict = {}
        for k, v in value.map_values.iteritems():
            contained_value = get_contained_value(contained_values, v)
            unwrapped_dict[k] = unwrap_response_value(contained_value, contained_values)
        return unwrapped_dict
    elif value.list_values:
        unwrapped_list = []
        for list_item in value.list_values:
            contained_value = get_contained_value(contained_values, list_item)
            unwrapped_list.append(unwrap_response_value(contained_value, contained_values))
        return unwrapped_list
    else:
        raise ValueError("Unknown type: " + str(type(value)))


def get_contained_value(contained_values, id):
    for value in contained_values:
        if value.value_id == id:
            return value.value

