import MessageEncoder
import Route
import RouteTree
import Router
import StaticRouterMatch
from abc import abstractmethod, ABC
import RouterMatch
from typing import List

class Chi(RouteTree):
    __EMPTY_STRING = ""
    __ntStatic = 0  # /home
    __ntRegexp = 1  # /{id: [0-9]+}
    __ntParam = 2   # /{user}
    __ntCatchAll = 3 # /api/v1/*

    __NODE_SIZE = __ntCatchAll + 1

    ZERO_CHAR = chr(0)

    __BASE_CATCH_ALL = "/?*"

    def __init__(self):
        '''
        __encoder: MessageEncoder
        '''
        self.__encoder = None
        self.__root = _Node()
        self.__staticPaths = {} # Map<Object, StaticRoute>

    class _MethodMatcher(ABC):
        @abstractmethod
        def get(self, method) -> StaticRouterMatch:
            pass

        @abstractmethod
        def put(self, method: str, route: StaticRouterMatch):
            pass

        @abstractmethod
        def matches(self, method: str) -> bool:
            pass
    
    class _SingleMethodMatcher(_MethodMatcher):
        '''
        __method: str
        __route: StaticRouterMatch
        '''
        def __init__(self):
            self.__method = None
            self.__route = None

        def put(self, method: str, route: StaticRouterMatch):
            self.__method = method
            self.__route = route

        def get(self, method: str) -> StaticRouterMatch:
            return self.__route if self.__method is method else None

        def matches(self, method: str) -> bool:
            return self.__method is method
        
        def clear(self):
            self.__method = None
            self.__route = None

    class _MultipleMethodMatcher(_MethodMatcher):
        def __init__(self, matcher: _SingleMethodMatcher):
            '''
            __methods: {str, StaticRouterMatch} dict
            (ConcurrentHashMap in Java)
            '''
            self.__methods = {}
            self.__methods[matcher.__method] = matcher.__route
            matcher.clear()

        def get(self, method: str) -> StaticRouterMatch:
            return self.__methods[method]

        def put(self, method: str, route: StaticRouterMatch):
            self.__methods[method] = route

        def matches(self, method: str) -> bool:
            return method in self.__methods

    class StaticRoute:
        def __init__(self):
            '''
            __matcher: MethodMatcher
            '''
            self.__matcher = None

        def put(self, method: str, route: Route):
            if self.__matcher is None:
                matcher = _SingleMethodMatcher()
            elif isinstance(matcher, _SingleMethodMatcher):
                matcher = _MultipleMethodMatcher()
            self.__matcher.put(method, StaticRouterMatch(route));

    class Segment:
        def __init__(self, nodeType: int = None, 
                regex: str = Chi._Chi__EMPTY_STRING, tail: str = None, 
                startIndex: int = None, endIndex: int = None):
            self.nodeType = nodeType
            self.rexPat = regex
            self.tail = tail
            self.startIndex = startIndex
            self.endIndex = endIndex

    class _Node:
        def __init__(self):
            '''
            typ: int. _Node types: static, regexp, param, catchAll
            label: str, first byte of prefix
            tail: str, first byte of child prefix
            prefix: str, common prefix we ignore
            rex: Pattern, regexp matcher for regexp nodes
            endpoints: Map<String, Route>, http handler endpoints on leaf node
            children: Node[NODE_SIZE][], child nodes should be stored in-order 
            for iteration, in groups of the node type.
            '''
            self.typ = None
            self.label = None
            self.tail = None
            self.prefix = None
            self.rex = None
            self.endpoints = None
            self.children = [[] for i in range(Chi._Chi__NODE_SIZE)]

        def typ(self, typ: int) -> _Node:
            self.typ = typ
            return self
        
        def label(self, label: str) -> _Node:
            self.label = label
            return self

        def tail(self, tail: str) -> _Node:
            self.tail = tail
            return self

        def prefix(self, prefix: str) -> _Node:
            self.prefix = prefix
            return self
                
        def __eq__(self, o: _Node):
            return self.label == o.label

        def __lt__(self, o: _Node):
            return self.label < o.label

        def insertRoute(self, method: str, pattern: str, route: Route) \
            -> _Node:
            pass

        def addChild(self, child: _Node, search: str) -> _Node:
            pass

        def replaceChild(self, label: str, tail: str, child: _Node):
            pass

        def getEdge(self, ntyp: int, label: str, tail: str, prefix: str)\
            -> _Node:
            pass

        def setEndpoint(self, method: str, route: Route):
            pass

        def findRoute(self, rctx: RouterMatch, method: str, path: str)\
            -> Route:
            pass

        def findEdge(self, ns: List[_Node], label: str) -> _Node:
            pass
        
        def isLeaf(self) -> bool:
            pass
        
        def longestPrefix(self, k1: str, k2: str) -> int:
            '''
            longestPrefix finds the filesize of the shared prefix of 
            two strings
            '''
            pass
        
        def tailSort(self, ns: List[_Node]):
            pass

        def __append(self, src: List[_Node], child: _Node) -> List[_Node]:
            pass

        def patNextSegment(self, pattern: str) -> Segment:
            pass

        def destroy(self):
            for ntyp in range(len(self.children)):
                pass

    def insert(self, method: str, pattern: str, route: Route):
        baseCatchAll = baseCatchAll(pattern)

        if len(baseCatchAll) > 1:
            # Add route pattern: /static/?* => /static
            self.insert(method, baseCatchAll, route)
            tail = pattern[len(baseCatchAll) + 2 : ]
            pattern = baseCatchAll + "/" + tail

        if pattern == self.__BASE_CATCH_ALL:
            pattern = "/*"

        if not Router.pathKeys(pattern):
            staticRoute = self.__staticPaths[pattern] if pattern in \
                self.__staticPaths else StaticRoute()
            staticRoute[method] = route
        
        self.__root.insertRoute(method, pattern, route)

    def baseCatchAll(self, pattern: str) -> str:
        i = pattern.index(self.__BASE_CATCH_ALL)
        return pattern[0:i] if i > 0 else ""

    def insert(self, route: Route):
        self.insert(route.getMethod(), route.getPattern(), route)

    def destroy(self):
        self.__root.destroy()

    def exists(self, method: str, path: str) -> bool:
        return self.find(method, path).matches()

    def find(self, method: str, path: str) -> Route.Match:
        staticRoute = self.__staticPaths.get(path)
        if staticRoute is None:
            return self.__findInternal(method, path)
        else:
            match = staticRoute.matcher.get(method)
            return self.__findInternal(method, path) \
                if match is None else match

    def __findInternal(self, method: str, path: str) -> Router.Match:
        # use radix tree
        result = RouterMatch()
        route = self.__root.findRoute(result, method, path)
        if route is None:
            return result.missing(method, path, self.__encoder)
        return result.found(route)

    def setEncoder(self, encoder: MessageEncoder):
        self.__encoder = encoder