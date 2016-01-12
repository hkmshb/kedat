﻿"""
This script runs the application using a development server.
"""
import os
import sys
import bottle
from beaker.middleware import SessionMiddleware


# modify sys
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
KEDAT_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, '..', '..'))
sys.path.append(KEDAT_ROOT)


# routes contains the HTTP handlers for our server and must be imported.
import routes

if '--debug' in sys.argv[1:] or 'SERVER_DEBUG' in os.environ:
    # Debug mode will enable more verbose output in the console window.
    # It must be set at the beginning of the script.
    bottle.debug(True)

def wsgi_app():
    """Returns the application to make available through wfastcgi. This is used
    when the site is published to Microsoft Azure."""
    session_options = {
        'session.type': 'file',
        'session.cookie_expires': 300,
        'session.data_dir': './session.dat',
        'session.auto': True
    }
    app = SessionMiddleware(bottle.default_app(), session_options)
    return app

if __name__ == '__main__':    
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static').replace('\\', '/')
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('XSERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    @bottle.route('/static/<filepath:path>')
    def server_static(filepath):
        """Handler for static files, used with the development server.
        When running under a production server such as IIS or Apache,
        the server should be configured to serve the static files."""
        return bottle.static_file(filepath, root=STATIC_ROOT)



    # Starts a local test server.
    bottle.run(app=wsgi_app(), server='wsgiref', host=HOST, port=PORT)
