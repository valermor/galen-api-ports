from Queue import Empty, Queue
import commands
import logging
import os
import re
import subprocess
from threading import Thread

REMOTE_EXECUTOR_SERVER_START_SCRIPT = 'run_java_server.sh'

PROJECT_NAME = 'galen-python-api'
EXECUTABLE_PATH_PATTERN = '(.*/' + PROJECT_NAME + ').*'

DEFAULT_THRIFT_SERVER_PORT = 9092

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

io_q = Queue()

def server_running(server_port):
    """
    Checks if RemoteCommandExecutor service is running.
    """
    output = commands.getoutput('lsof -i :' + str(server_port))
    return 'java' in output


def start_server(server_port=DEFAULT_THRIFT_SERVER_PORT):
    """
    Starts RemoteCommandExecutor service.
    :return:
    """
    if not server_running(server_port):
        p = re.compile(EXECUTABLE_PATH_PATTERN)
        m = p.match(os.getcwd())
        if m.groups():
            command = "{path}/{start_script} {port}".format(path=m.groups()[0],
                                                                 start_script=REMOTE_EXECUTOR_SERVER_START_SCRIPT,
                                                                 port=str(server_port))
            server_process = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
            Thread(target=stream_watcher, name='stdout-watcher', args=('STDOUT', server_process.stdout)).start()
            Thread(target=stream_watcher, name='stderr-watcher', args=('STDERR', server_process.stderr)).start()
            Thread(target=printer, name='printer', args=(server_process,)).start()
        logger.info("Started server at port " + str(server_port))


def stop_server(server_port):
    """
    Stop RemoteCommandExecutor service.
    """
    if server_running(server_port):
        output = commands.getoutput('lsof -i :' + str(server_port))
        lines = output.split('\n')
        for line in lines:
            fields = line.split()
            if fields[1] != 'PID':
                os.popen('kill -9 ' + fields[1])
    logger.info("Stopping server at port " + str(server_port))


def stream_watcher(identifier, stream):
    """
    Author Shrikant Sharat
    http://sharats.me/the-ever-useful-and-neat-subprocess-module.html
    """
    for line in stream:
        io_q.put((identifier, line))

    if not stream.closed:
        stream.close()


def printer(proc):
    """
    Author Shrikant Sharat
    http://sharats.me/the-ever-useful-and-neat-subprocess-module.html
    """
    while True:
        try:
            # Block for 1 second.
            item = io_q.get(True, 1)
        except Empty:
            # No output in either streams for a second. Are we done?
            if proc.poll() is not None:
                break
        else:
            identifier, line = item
            if identifier == 'STDERR':
                logging.error(remove_new_line(line))
            elif identifier == 'STDOUT':
                logging.info(remove_new_line(line))
            # logging.info(remove_new_line(line))


def remove_new_line(line):
    return line.split('\n')[0]
