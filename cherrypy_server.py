__author__ = 'mnelson'

import bottle
import os
from web.server import cfg, ping_thing
import logging

application = bottle.default_app()

#bottle.run(server='cherrypy', host='0.0.0.0', port=cfg.port, debug=cfg.debug, reloader=cfg.debug, quiet=cfg.debug)

import cherrypy


def stop_ping_thing():
    logging.getLogger().info("Shutting down ping thread")
    ping_thing.shutdown()

if __name__ == '__main__':

    script_dir = os.path.dirname(os.path.realpath(__file__))

    os.chdir(os.path.join(script_dir, 'web'))

    # Mount the application
    cherrypy.tree.graft(application, "/")

    # Unsubscribe the default server
    cherrypy.server.unsubscribe()

    # Instantiate a new server object
    server = cherrypy._cpserver.Server()

    # Configure the server object
    server.socket_host = "0.0.0.0"
    server.socket_port = cfg.port
    server.thread_pool = 30

    # Subscribe this server
    server.subscribe()

    cherrypy.engine.subscribe('stop', stop_ping_thing)

    cherrypy.engine.start()
    cherrypy.engine.block()

    logging.getLogger().info("All clean, good bye")