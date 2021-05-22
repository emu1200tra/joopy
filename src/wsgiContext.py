from .defaultContext import DefaultContext
from multipledispatch import dispatch
from .exception.StatusCode import StatusCode
import os
from .exception.StatusCodeBase import StatusCodeBase
from .exception.NotFoundException import NotFoundException

class wsgiContext(DefaultContext):
    def __init__(self, request, router):
        super(wsgiContext, self).__init__()
        self.request = request
        self.router = router
        self.method = request['REQUEST_METHOD']
        self.requestPath = request['PATH_INFO']
        self.pathMap = None
        self.route = None
        self.ResponseStarted = False
        self.body = None
        self.statusCode = StatusCode.OK.toString()
        self.handler = None
        self.header = 'text/plain'

    def get_router(self):
        return self.router

    def get_method(self):
        return self.method

    def get_request_path(self):
        return self.requestPath

    def set_path_map(self, pathMap):
        self.pathMap = pathMap
        return self

    def set_route(self, route):
        self.route = route
        return self

    def dispatch(self, action):
        action()
        return self

    def is_response_started(self):
        return self.ResponseStarted

    def send(self, data, codec='utf-8'):
        self.body = data.encode(codec)
        return self.body

    def send_code(self, statusCode, codec):
        self.set_status_code(statusCode.toString())
        self.body = statusCode.toString().encode(codec)
        return self.body

    def send_error(self, ecp, codec):
        self.set_status_code(ecp.getStatusCode().toString())
        self.body = ecp.getStatusCode().toString().encode(codec)
        return self.body

    def set_handler(self, handler):
        self.handler = handler
        return handler

    #"this should be invalid function"
    def extract(self):
        self.body = self.handler.apply(self)
        return self.body

    def set_status_code(self, code):
        self.statusCode = code
        return self.statusCode

    def set_header(self, header):
        self.header = header
        return self.header