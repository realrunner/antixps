__author__ = 'mnelson'
from bottle import json_dumps, json_loads
from os import path
import logging
import socket

logger = logging.getLogger("Config")

defaults = {
    "app_url": "https://antix.io",
    "app_printer_key": "13e8eb3a-0a3e-4b45-b739-e7a11063e98b",
    "api_key": "pass22",
    "server_name": "Alpha",
    "port": 48120,
    "printers": [],
    "debug": True,
    "organization_id": "9ad05259-42fe-4f95-a7b9-4ee1b8aa516f",
}


class Config(object):
    filename = "printsrv.json"

    def __init__(self):
        self.data = {}
        self.data.update(defaults)
        self.load()

    def load(self):
        if path.exists(self.filename):
            try:
                with open(self.filename) as fp:
                    json = fp.read()
                    self.data.update(json_loads(json))
            except Exception as ex:
                logger.error("Failed reading config file: " + str(ex))
                self.data = {}

    def write(self):
        try:
            with open(self.filename, mode='w') as fp:
                json = json_dumps(self.data, indent=4)
                fp.write(json)
        except Exception as ex:
            logger.error("Failed writing config file: " + str(ex))

    @staticmethod
    def find_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        finally:
            s.close()

    # def server_url(self):
    #     return "http://{0}:{1}".format(self.find_local_ip(), self.data['port'])

    def __getattr__(self, item):
        return self.data[item] if item in self.data else None

