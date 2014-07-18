__author__ = 'mnelson'

import bottle
import os
from web.server import cfg, ping_thing
import logging

script_dir = os.path.dirname(os.path.realpath(__file__))

os.chdir(os.path.join(script_dir, 'web'))

application = bottle.default_app()


bottle.run(server='cherrypy', host='0.0.0.0', port=cfg.port, debug=cfg.debug, reloader=cfg.debug, quiet=cfg.debug)

logging.getLogger().info("Shutting down ping thread")
ping_thing.shutdown()
logging.getLogger().info("All clean, good bye")