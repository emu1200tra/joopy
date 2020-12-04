from collections import OrderedDict
import Route
import Context
from typing import List, Set, OrderedDict

class RouterMatch(Router.Match):
    def __init__(self):
        '''
        matches: bool
        __route: Route
        vars: Map
        __handler: Route.Handler
        '''
        self.matches = None
        self.__route = None
        self.vars = {}
        self.__handler = None

    def key(self, keys: List[str]):
        for i in range(min(len(keys), len(self.vars))):
            vars[keys.get(i)] = vars.pop(i, None)

    def truncate(self, size: int):
        while size < len(self.vars):
            size += 1
            del vars[size]

    def value(self, value: str):
        if not self.vars:
            self.vars = OrderedDict()
        self.vars[len(self.vars)] = value

    def pop(self):
        del self.vars[len(self.vars) - 1]

    def methodNotAllowed(self, allow: Set[str]):
        allowString = allow
        pass
        
    def matches(self) -> bool:
        return self.matches

    def route(self) -> Route:
        return self.__route

    def pathMap(self) -> OrderedDict[str, str]:
        return self.vars

    def found(self, route: Route) -> RouterMatch:
        self.__route = route
        self.matches = True
        return self

    def execute(self, context: Context):
        context.setPathMap(self.vars)
        context.setRoute(self.__route)
        try:
            route.getPipeline().apply(context)
        except Exception as e:
            context.sendError(e)
        finally:
            self.__handler = None
            self.__route = None
            self.vars = None

    def missing(self, method: str, path: str, encoder: MessageEncoder) \
            -> RouterMatch:
        h = None # Route.Handler
        if self.__handler is None:
            h = Route.FAVICON if path.endswith("/favicon.ico") \
                else Route.NOT_FOUND
        else:
            h = self.__handler
        self.__route = Route(method, path, h)
        self.__route.setEncoder(encoder)
        self.__route.setReturnType(type(Context))
        return self