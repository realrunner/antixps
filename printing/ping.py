__author__ = 'mnelson'

import threading
import urllib.request, urllib.error, urllib.parse
from bottle import json_dumps
import logging

logger = logging.getLogger(__name__)


class TaskThread(threading.Thread):
    """Thread that executes a task every N seconds"""

    def __init__(self, interval=15.0):
        threading.Thread.__init__(self)
        self._finished = threading.Event()
        self._interval = interval

    def set_interval(self, interval):
        """Set the number of seconds we sleep between executing our task"""
        self._interval = interval

    def shutdown(self):
        """Stop this thread"""
        self._finished.set()

    def run(self):
        while 1:
            if self._finished.isSet():
                return
            self.task()

            # sleep for interval or until shutdown
            self._finished.wait(self._interval)

    def task(self):
        """The task done by this thread - override in subclasses"""
        pass


class Pinger(TaskThread):
    key = "13e8eb3a-0a3e-4b45-b739-e7a11063e98b"

    def __init__(self, config):
        TaskThread.__init__(self, 300.0)
        self.config = config

    def task(self):
        if not self.config.organization_id:
            return

        url = self.config.app_url + "/printer/ping/" + self.key
        data = {
            "name": self.config.server_name,
            "ip": self.config.find_local_ip(),
            "port": self.config.port,
            "secret": self.config.api_key,
            "organizationId": self.config.organization_id
        }
        headers = {"Content-type": "application/json"}
        json = json_dumps(data)
        bin_json = json.encode()
        req = urllib.request.Request(url, bin_json, headers)
        try:
            resp = urllib.request.urlopen(req)
            logger.debug("Ping: {0}".format(resp.read()))
        except Exception as ex:
            logger.error("Ping to %s failed: %s" % (url, str(ex)))


