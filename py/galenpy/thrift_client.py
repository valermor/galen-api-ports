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

import logging
import os
from time import sleep

from thrift import Thrift
from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport
from thrift.transport.TTransport import TTransportException
from galenpy.remote_service_lifecycle import start_server, stop_server

from pythrift import GalenApiRemoteService
from pythrift.ttypes import SpecNotFoundException


GALEN_REMOTE_API_SERVICE_DEFAULT_PORT = 9092

""" RESILIENCE_INTERVAL specifies after which amount of time (in seconds) we can assume there is no activity in the
    remote server so that we are allowed to quit it."""
RESILIENCE_INTERVAL = 5

logger = logging.getLogger()


class ThriftClient(object):
    """
    Facade class providing access to services exposed by Thrift interface hiding all complex details.
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

    def quit_service_if_inactive(self):
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
    Start Galen API service on the given port.
    """
    if os.getenv('SERVER_ALWAYS_ON', 'False') is 'False':
        start_server(server_port)


def stop_galen_remote_api_service(server_port):
    """
    Stops Galen API service on the given port.
    """
    if os.getenv('SERVER_ALWAYS_ON', 'False') is 'False':
        stop_server(server_port)
