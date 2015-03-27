from Queue import Queue, Empty
import logging
from threading import Thread

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


io_q = Queue()


class RemoteServiceStreamListener(Thread):
    """
    Class implementing a Thread that listen to the remote service process stream (stdin, stderr) and queues logs messages
    into the Queue object, for the RemoteServiceLoggerThread to consume.
    """
    def __init__(self, identifier, proc):
        super(RemoteServiceStreamListener, self).__init__()
        self.setDaemon(True)
        self.process = proc
        self.identifier = identifier
        if 'STDOUT' in self.identifier:
            self.stream = self.process.stdout
        elif 'STDERR' in self.identifier:
            self.stream = self.process.stderr

    def run(self):
        print "starting listener for {id}\n".format(id=self.identifier)
        while True:
            data = self.stream.readline()
            if len(data) == 0:
                break
            io_q.put((self.identifier, data))


class RemoteServiceLogger(Thread):
    """
    Class implementing a Thread that reads fetches logs from the queue and dumps it to an error or an info log depending
    on whether the relevant server logs was issued on stdout or stderr, respectively.
    """
    def __init__(self, process):
        super(RemoteServiceLogger, self).__init__()
        self.setDaemon(True)
        self.process = process

    def run(self):
        logger.info("starting Galen API Remote Service logger")
        while True:
            try:
                item = io_q.get(True)
            except Empty:
                if self.process.poll() is not None:
                    break
            else:
                identifier, line = item
                if identifier == 'STDERR':
                    logging.error(remove_new_line(line))
                elif identifier == 'STDOUT':
                    logging.info(remove_new_line(line))


def remove_new_line(line):
    return line.split('\n')[0]
