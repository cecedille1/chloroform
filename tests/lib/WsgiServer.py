# -*- coding: utf-8 -*-

import threading
import random

from wsgiref.simple_server import make_server, WSGIRequestHandler

from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

from django.utils.module_loading import import_string


class WsgiServerListener(object):
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, wsgi_server):
        self._wsgi_server = wsgi_server

    def close(self):
        logger.info('Closing the application')
        self._wsgi_server.stop_application()


class QuietHandler(WSGIRequestHandler):
    def log_request(*args, **kw):
        pass


class WsgiServer(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, wsgi_module):
        self.ROBOT_LIBRARY_LISTENER = WsgiServerListener(self)
        self._bi = BuiltIn()
        self.wsgi_module = import_string(wsgi_module)
        self._thread = None

    def start_application(self):
        if self._thread is not None:
            logger.debug('Application is running, dismiss')
            return

        port = random.randint(43000, 44000)

        self._bi.set_global_variable('${BASEURL}', 'http://localhost:{}'.format(port))

        self.server = make_server('127.0.0.1', port, self.wsgi_module, handler_class=QuietHandler)
        self._thread = threading.Thread(target=self.server.serve_forever, name='WSGIServer')

        self._thread.start()

    def stop_application(self):
        if self._thread is None:
            logger.debug('Application is not running, dismiss')
            return

        self.server.shutdown()
        self._thread.join()
        self._thread = None
