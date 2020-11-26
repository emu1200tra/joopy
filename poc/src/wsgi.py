from wsgiref.util import setup_testing_defaults, guess_scheme, request_uri
from wsgiref.simple_server import make_server
from src.Server import Base
from threading import Thread
#
# # A relatively simple WSGI application. It's going to print out the
# # environment dictionary after being updated by setup_testing_defaults
# def simple_app(environ, start_response):
#     setup_testing_defaults(environ)
#
#     status = '200 OK'
#     headers = [('Content-type', 'text/plain; charset=utf-8')]
#
#     start_response(status, headers)
#
#     print(guess_scheme(environ))
#     print(request_uri(environ))
#
#     geturl = environ['PATH_INFO']
#     print(geturl)
#     # for item in url:
#     #     if item[0] == geturl:
#     #         return [item[1]().encode("utf-8")]
#     # else:
#     #     return '404'
#
#     ret = [("%s: %s\n" % (key, value)).encode("utf-8")
#            for key, value in environ.items()]
#
#     ret = b'hello world'
#     return [ret, ]
#
#     # return ret
#
#
# with make_server('', 8000, simple_app) as httpd:
#     print("Serving on port 8000...")
#     httpd.serve_forever()

class wsgi_function():
    def __init__(self, routes):
        super().__init__()
        self.routes = routes
    def setup_wsgi(self, environ, start_response):
        response_status = '200 OK'
        # content-type 應該由 route 決定, 暫時先 hard code
        headers = [('Content-type', 'text/plain')]

        start_response(response_status, headers)

        uri = environ['PATH_INFO']
        # method = environ['REQUEST_METHOD']

        return [self.routes[uri][1]()]

class wsgi(Base):
    def __init__(self):
        super().__init__()
        self.apps = []
        self.server = None
    
    def start(self, application):
        self.apps.append(application)
        self.fireStart(self.apps)

        routes = application.routes
        func = wsgi_function(routes)
        self.server = make_server('', 8000, func.setup_wsgi)
        self.m = Thread(target=self.server.serve_forever, name="m_process")
        self.m.start()
        self.fireReady(self.apps)

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


        
        


