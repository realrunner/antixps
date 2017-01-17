import cherrypy
import os
import logging


def stop_ping_thing():
    from web.server import ping_thing
    logging.getLogger().info("Shutting down ping thread")
    ping_thing.shutdown()


def start_server():
    import bottle

    script_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(os.path.join(script_dir, 'web'))

    from web.server import cfg
    application = bottle.default_app()

    cherrypy.config.update({'engine.autoreload.on': False})

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
    server.ssl_module = 'builtin'
    server.ssl_certificate = os.path.realpath(os.path.join('..', 'cert', 'cert.pem'))
    server.ssl_private_key = os.path.realpath(os.path.join('..', 'cert', 'key.pem'))

    # Subscribe this server
    server.subscribe()

    cherrypy.engine.subscribe('stop', stop_ping_thing)

    cherrypy.engine.start()

    logging.getLogger().info("All clean, good bye")


def stop_server():
    cherrypy.engine.exit()

if __name__ == '__main__':
    start_server()
    cherrypy.engine.block()
