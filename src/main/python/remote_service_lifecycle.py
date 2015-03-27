import commands
import logging
import os
import re
import subprocess

from remote_service_logging import RemoteServiceStreamListener, RemoteServiceLogger


GALEN_REMOTE_API_SERVER_START_SCRIPT = 'run_java_server.sh'

PROJECT_NAME = 'galen-python-api'
EXECUTABLE_PATH_PATTERN = '(.*/' + PROJECT_NAME + ').*'

DEFAULT_THRIFT_SERVER_PORT = 9092

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def server_running(server_port):
    """
    Checks if GalenRemoteApi service is running.
    """
    #TODO Portability on non-Mac OSs
    output = commands.getoutput('lsof -i :' + str(server_port))
    return 'java' in output


def start_server(server_port=DEFAULT_THRIFT_SERVER_PORT):
    """
    Starts GalenRemoteApi service.
    """
    #TODO Portability on non-Mac OSs
    if not server_running(server_port):
        p = re.compile(EXECUTABLE_PATH_PATTERN)
        m = p.match(os.getcwd())
        if m.groups():
            command = "{path}/{start_script} {port}".format(path=m.groups()[0],
                                                                 start_script=GALEN_REMOTE_API_SERVER_START_SCRIPT,
                                                                 port=str(server_port))
            server_process = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
            RemoteServiceStreamListener('STDOUT', server_process).start()
            RemoteServiceStreamListener('STDERR', server_process).start()
            RemoteServiceLogger(server_process).start()
        logger.info("Started server at port " + str(server_port))


def stop_server(server_port):
    """
    Stop GalenRemoteApi service.
    """
    #TODO Portability on non-Mac OSs
    if server_running(server_port):
        output = commands.getoutput('lsof -i :' + str(server_port))
        lines = output.split('\n')
        for line in lines:
            fields = line.split()
            if 'java' in fields[0] and fields[1] != 'PID':
                os.popen('kill -9 ' + fields[1])
    logger.info("Stopping server at port " + str(server_port))


