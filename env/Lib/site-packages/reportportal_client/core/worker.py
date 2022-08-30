"""This module contains worker that makes non-blocking HTTP requests.

Copyright (c) 2018 http://reportportal.io .

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from enum import auto, Enum, unique
import logging
from threading import currentThread, Thread
from queue import Empty

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


@unique
class ControlCommand(Enum):
    """This class stores worker control commands."""

    CLEAR_QUEUE = auto()
    NOP = auto()
    REPORT_STATUS = auto()
    STOP = auto()
    STOP_IMMEDIATE = auto()

    def is_stop_cmd(self):
        """Verify if the command is the stop one."""
        return self in (ControlCommand.STOP, ControlCommand.STOP_IMMEDIATE)


class APIWorker(object):
    """Worker that makes non-blocking HTTP requests to the Report Portal."""

    def __init__(self, cmd_queue, data_queue):
        """Initialize instance attributes.

        :param cmd_queue:  Queue for the control commands
        :param data_queue: Queue for the RP requests to process
        """
        self._cmd_queue = cmd_queue
        self._data_queue = data_queue
        self._thread = None
        self.name = self.__class__.__name__

    def _command_get(self):
        """Get control command from the control queue."""
        try:
            cmd = self._cmd_queue.get_nowait()
            logger.debug('[%s] Received {%s} command', self.name, cmd)
            return cmd
        except Empty:
            return None

    def _command_process(self, cmd):
        """Process control command sent to the worker.

        :param cmd: ControlCommand to be processed
        """
        if not cmd:
            return  # No command received

        logger.debug('[%s] Processing {%s} command', self.name, cmd)
        if cmd == ControlCommand.REPORT_STATUS:
            logger.debug('[%s] Current status for tasks is: {%s} unfinished',
                         self.name, self._data_queue.unfinished_tasks)

        if cmd == ControlCommand.STOP:
            request = self._request_get()
            while request is not None:
                self._request_process(request)
                request = self._request_get()

        if cmd.is_stop_cmd():
            self._stop()

    def _monitor(self):
        """Monitor worker queues and process them.

        This method runs on a separate, internal thread. The thread will
        terminate if the stop_immediate control command is received. If
        the stop control command is sent, the worker will process all the
        items from the queue before terminate.
        """
        while True:
            cmd = self._command_get()
            self._command_process(cmd)

            if cmd and cmd.is_stop_cmd():
                logger.debug('[%s] Exiting due to {%s} command',
                             self.name, cmd)
                break

            request = self._request_get()
            self._request_process(request)

    def _request_get(self):
        """Get response object from the data queue."""
        try:
            _, request = self._data_queue.get_nowait()
            logger.debug('[%s] Received {%s} request', self.name, request)
            return request
        except Empty:
            return None

    def _request_process(self, request):
        """Send request to RP and update response attribute of the request."""
        if not request:
            return  # No request received

        logger.debug('[%s] Processing {%s} request', self.name, request)
        request.response = request.http_request.make()
        self._data_queue.task_done()

    def _stop(self):
        """Routine that stops the worker thread(s).

        This asks the thread to terminate, and then waits for it to do so.
        Note that if you don't call this before your application exits, there
        may be some records still left on the queue, which won't be processed.
        """
        if self._thread.isAlive() and self._thread is not currentThread():
            self._thread.join()
        self._thread = None

    def send_command(self, cmd):
        """Send control command to the worker queue."""
        self._cmd_queue.put(cmd)

    def send_request(self, request):
        """Send a request to the worker queue.

        :param request: RPRequest object
        """
        self._data_queue.put(request)

    def start(self):
        """Start the worker.

        This starts up a background thread to monitor the queue for
        requests to process.
        """
        self._thread = Thread(target=self._monitor)
        self._thread.setDaemon(True)
        self._thread.start()

    def stop(self):
        """Stop the worker.

        Send the appropriate control command to the worker.
        """
        self.send_command(ControlCommand.STOP)

    def stop_immediate(self):
        """Stop the worker immediately.

        Send the appropriate control command to the worker.
        """
        self.send_command(ControlCommand.STOP_IMMEDIATE)
