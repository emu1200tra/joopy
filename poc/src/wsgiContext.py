from src.defaultContext import DefaultContext
from multipledispatch import dispatch
from .exception.StatusCode import StatusCode
import os

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

    @dispatch(str, str)
    def send(self, data, codec):
        self.body = data.encode(codec)
        return self.body

