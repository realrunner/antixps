#!/usr/bin/python

import logging
from bottle import route, run, get, post, request, static_file, response, template, abort, hook

from printing.config import Config
from printing import printer
from printing import ping
import os
import subprocess
import threading


## load config ##
cfg = Config()


#logging
log_level = logging.DEBUG if cfg.debug else logging.INFO
logging.basicConfig(level=log_level)
logger = logging.getLogger("server")


## ping thread ##
ping_thing = ping.Pinger(cfg)
ping_thing.start()

## update printer list in config ##
printer.merge_connected_with_config(printer.find_printers(), cfg)

## write out latest config ##
cfg.write()

@hook('after_request')
def enable_access_controls():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@route('/log')
def get_log():
    return "Not yet!"


@route('/')
def hello():
    printer.merge_connected_with_config(printer.find_printers(), cfg)
    return template('index', api_key=cfg.api_key)


@route('/<file_path:path>',  method=['OPTIONS'])
def cors(file_path):
    return {}


@route('/static/<file_path:path>')
def server_static(file_path):
    return static_file(file_path, root='./static/')


@get('/config/<api_key>')
def get_config(api_key):
    if api_key != cfg.api_key:
        abort(403, "Access Denied")
    return cfg.data


@get('/listprinters')
def list_printers():
    return dict(printers=cfg.printers)

@get('/scanprinters/<apikey>')
def scan_printers(apikey):
    if apikey != cfg.api_key:
        abort(403, "Access Denied")
    printer.merge_connected_with_config(printer.find_printers(), cfg)
    cfg.write()
    return dict(printers=cfg.printers)

@get('/test/<printer_id>/<apikey>')
def print_test_page(printer_id, apikey):
    if apikey != cfg.api_key:
        abort(403, "Access Denied")

    p = printer.get_printer(printer_id, cfg)
    if p is None:
        abort(400, "Unknown printer " + printer_id)

    commands = [
        {"command": "set", "align": "center", "type": "b", "width": 2, "height": 2},
        {"command": "text", "text": "Printer Test"},
        {"command": "set", "align": "center"},
        {"command": "text", "text": " "},
        {"command": "image", "path": "{0}/api/printer/logo/{1}/{2}".format(cfg.app_url, cfg.organization_id, ping_thing.key)},
        {"command": "text", "text": " "},
        {"command": "set", "align": "left"},
        {"command": "text", "text": "Printer: {0}".format(p.config['name'])},
        {"command": "text", "text": "Printer type: {0} {1}".format(p.config['manufacturer'], p.config['model'])},
        {"command": "text", "text": "Printer serial #: {0}".format(p.config['serial'])},
        {"command": "text", "text": " "},
        {"command": "qr", "data": "Printer Test Data Encoded"},
        {"command": "cut"}
    ]

    p.print_receipt(commands)
    return "done"


@get('/helloprinter/<printer_id>/<api_key>')
def hello_printer(printer_id, api_key):
    if api_key != cfg.api_key:
        abort(403, "Access Denied")

    p = printer.get_printer(printer_id, cfg)
    if p is None:
        abort(400, "Unknown printer " + printer_id)

    commands = [
        {"command": "text", "text": "Printer: %s" % p.config["name"]},
        {"command": "cut"}
    ]

    p.print_receipt(commands)
    return "done"


@get('/opencashbox/<printer_id>/<apikey>')
def open_cash_box(printer_id, apikey):
    if apikey != cfg.api_key:
        abort(403, "Access Denied")

    p = printer.get_printer(printer_id, cfg)
    if p is None:
        abort(400, "Unknown printer " + printer_id)

    commands = [
        {"command": "cashdraw", "pin": 2},
        {"command": "reset"}
    ]

    p.print_receipt(commands)
    return "done"


@post('/config/<apikey>')
def save_config(apikey):
    if apikey != cfg.api_key:
        abort(403, "Access Denied")

    data = request.json
    cfg.data.update(data)
    cfg.write()
    return cfg.data


@post('/print/<printer_id>/<apikey>')
def print_something(printer_id, apikey):
    if apikey != cfg.api_key:
        abort(403, "Access Denied")

    p = printer.get_printer(printer_id, cfg)
    if p is None:
        abort(400, "Unknown printer " + printer_id)

    data = request.json
    try:
        p.print_receipt(data)
        return "success"
    except Exception as ex:
        return "failure " + str(ex)


def restart():
    os.execl("/usr/sbin/service", "antixps", "restart")


@get('/upgrade/<api_key>')
def upgrade(api_key):
    if api_key != cfg.api_key:
        abort(403, "Access Denied")
    pwd = os.getcwd()
    rootdir = os.path.realpath(os.path.join(pwd, '../'))
    os.chdir(rootdir)
    pid = subprocess.Popen(['git', 'pull']).pid
    os.chdir(pwd)
    threading.Timer(2.0, restart).start()
    return template('upgrade')


if __name__ == '__main__':

    logger.info("Antix print server starting up")

    run(host='0.0.0.0', port=cfg.port, debug=cfg.debug, reloader=cfg.debug, quiet=(not cfg.debug))

    logging.getLogger().info("Shutting down ping thread")
    ping_thing.shutdown()
    logging.getLogger().info("All clean, good bye")
