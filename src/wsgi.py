
from wsgiref.util import setup_testing_defaults, guess_scheme, request_uri
from wsgiref.simple_server import make_server
from .Server import Base
from threading import Thread
from .wsgiHandler import wsgiHandler
import socket
from contextlib import closing


class wsgi(Base):
    def __init__(self):
        super().__init__()
        self.apps = []
        self.server = None

    def find_free_port(self):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(('', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

    def start(self, application):
        try:
            self.apps.append(application)
            self.fireStart(self.apps)
            port = 8010  # TODO: self.find_free_port()
            handler = wsgiHandler(application)
            self.server = make_server('', port, handler)
            print("Server on port: {}...".format(port))
            self.m = Thread(target=self.server.serve_forever, name="m_process")
            self.m.start()
            self.fireReady(self.apps)
        except Exception as e:
            print("wsgi server start up error: {}".format(e))
        return self

    def stop(self):
        self.fireStop(self.apps)
        if self.server:
            self.s = Thread(target=self.server.shutdown, name="s_process")
            self.s.start()
            self.s.join()
            self.m.join()
        self.server = None
        return self
