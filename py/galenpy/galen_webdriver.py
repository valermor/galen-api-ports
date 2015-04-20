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
    This is implementation of RemoteWebDriver Client which uses JsonWire protocol over Thrift. The commands to be sent
    to a remote Grid are intercepted and sent across the Thrift interface.
    Internally, GalenWebDriver makes use of GalenRemoteConnection, an ad-hoc command_executor which sends commands over
    the Thrift interface.
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
            if response.value:
                response_value = unwrap_response_value(response.value)
            return dict(status=response.status, sessionId=response.session_id, state=response.state, value=response_value)
        except RemoteWebDriverException as e:
            raise WebDriverException(e.message)

    def set_session_id(self, session_id):
        self.session_id = session_id


def unwrap_response_value(response_value):
    """
    Transforms the response value received on the Thrift interface from ResponseValueType to the types WebDriver expects
    to receive from a CommandExecutor.
    """
    if response_value.map_values:
        return unwrap_dict_values(response_value.map_values)
    elif response_value.list_values:
        return unwrap_list_values(response_value.list_values)
    elif response_value.string_value:
        return response_value.string_value
    elif response_value.wrapped_long_value:
        return long(response_value.wrapped_long_value)
    raise ValueError("Unknown response.value type")


def unwrap_list_values(list_values):
    """
    Transforms a Thrift list of values to a Python list.
    """
    response_value = list()
    for list_item in list_values:
        if list_item.unicode_value:
            response_value.append(list_item.unicode_value)
        elif list_item.boolean_value:
            response_value.append(list_item.boolean_value)
        elif list_item.dict_value:
            if list_item.dict_value == 'True':
                response_value.append(True)
            elif list_item.dict_value == 'False':
                response_value.append(False)
            else:
                response_value.append(list_item.dict_value)
        elif list_item.list_value:
            response_value.append(list_item.list_value)
    return response_value


def unwrap_dict_values(map_values):
    """
    Transforms a Thrift map of values to a Python dict.
    """
    dict_value = dict()
    for key, value in map_values.iteritems():
        if value.unicode_value:
            dict_value[key] = value.unicode_value
        elif value.boolean_value:
            dict_value[key] = value.boolean_value
        elif value.dict_value:
            if value.dict_value == 'True':
                dict_value[key] = True
            elif value.dict_value == 'False':
                dict_value[key] = False
            else:
                dict_value[key] = value.dict_value
        elif value.list_value:
            dict_value[key] = value.list_value
        elif value.wrapped_long_value:
            dict_value[key] = long(value.wrapped_long_value)
    return dict_value


