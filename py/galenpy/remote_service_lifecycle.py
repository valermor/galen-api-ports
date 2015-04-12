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

import commands
import logging
from os import path, popen
from random import random
import subprocess
from time import sleep
from galenpy.remote_service_logging import RemoteServiceStreamListener, RemoteServiceLogger


MAX_SLOW_START_DELAY = 1

GALEN_REMOTE_API_SERVER_JAR = 'galen-api-server.jar'

DEFAULT_THRIFT_SERVER_PORT = 9092

logger = logging.getLogger()


def server_running(server_port):
    """
    Checks if GalenRemoteApi service is running.
    """
    # TODO Portability on non-Mac OSs
    output = commands.getoutput('lsof -i :' + str(server_port))
    return 'java' in output


def start_server(server_port=DEFAULT_THRIFT_SERVER_PORT):
    """
    Starts GalenRemoteApi service.
    """
    # TODO Portability on non-Mac OSs
    slow_start(MAX_SLOW_START_DELAY)
    if not server_running(server_port):
        command = "java -jar {path}/{jar_file} -r {port}".format(path=locate_server_path(),
                                                                 jar_file=GALEN_REMOTE_API_SERVER_JAR,
                                                                 port=str(server_port))
        server_process = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        RemoteServiceStreamListener('STDOUT', server_process, 'stdout listener').start()
        RemoteServiceStreamListener('STDERR', server_process, 'stderr listener').start()
        RemoteServiceLogger(server_process, 'Remote service').start()
        logger.info("Started server at port " + str(server_port))


def stop_server(server_port):
    """
    Stop GalenRemoteApi service.
    """
    # TODO Portability on non-Mac OSs
    if server_running(server_port):
        output = commands.getoutput('lsof -i :' + str(server_port))
        lines = output.split('\n')
        for line in lines:
            fields = line.split()
            if 'java' in fields[0] and fields[1] != 'PID':
                popen('kill -9 ' + fields[1])
    logger.info("Stopping server at port " + str(server_port))


def locate_server_path():
    return path.join(path.dirname(__file__), 'service')


def slow_start(max_delay):
    """
    It adds a random delay of max_delay ms to prevent concurrent threads to attempt to initialize the server
      simultaneously.
    """
    sleep(max_delay * random())
