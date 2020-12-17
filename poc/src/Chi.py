from .MessageEncoder import MessageEncoder
from .Route import Route
from .RouteTree import RouteTree
from .Router import Router
from .StaticRouterMatch import StaticRouterMatch
from abc import abstractmethod, ABC
from .RouterMatch import RouterMatch
from typing import List
import re

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
        self.__root = Chi._Node()
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
            return self.__route if self.__method == method else None

        def matches(self, method: str) -> bool:
            return self.__method == method
        
        def clear(self):
            self.__method = None
            self.__route = None

    class _MultipleMethodMatcher(_MethodMatcher):
        def __init__(self, matcher):
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
                matcher = Chi._SingleMethodMatcher()
            elif isinstance(matcher, Chi._SingleMethodMatcher):
                matcher = Chi._MultipleMethodMatcher()
            self.__matcher.put(method, StaticRouterMatch(route));

    class Segment:
        def __init__(self, nodeType: int = None, 
                regex: str = None, tail: str = None, 
                startIndex: int = None, endIndex: int = None):
            self.nodeType = nodeType
            self.rexPat = Chi.__EMPTY_STRING if regex is None else regex
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

        def typ(self, typ: int):
            self.typ = typ
            return self
        
        def label(self, label: str):
            self.label = label
            return self

        def tail(self, tail: str):
            self.tail = tail
            return self

        def prefix(self, prefix: str):
            self.prefix = prefix
            return self

        def insertRoute(self, method: str, pattern: str, route: Route):
            n = self
            parent = None # Node
            search = pattern
            while True:
                # Handle key exhaustion
                if not search:
                    # Insert or update the node's leaf handler
                    n.setEndpoint(method, route)
                    return n

                # Search for wild node next. In this case, we need to get
                # the tail
                label = search[0]
                seg = None # Segment
                if label == "{" or label == "*":
                    seg = self.patNextSegment(search)
                else:
                    seg = Chi.Segment()

                prefix = None # str
                if seg.nodeType == Chi._Chi__ntRegexp:
                    prefix = seg.rexPat
                else:
                    prefix = Chi._Chi__EMPTY_STRING
                
                # Look for the edge to attach to
                parent = n
                n = n.getEdge(seg.nodeType, label, seg.tail, prefix)

                # No edge, create one
                if n is None:
                    child = Chi._Node().label(label).tail(seg.tail).prefix(search)
                    hn = parent.addChild(child, search)
                    hn.setEndpoint(method, route)
                    return hn

                # Found an edge to newRuntimeRoute the pattern
                if n.typ > Chi._Chi__ntStatic:
                    # found a param node, trim the param from the search path 
                    # and continue. This param/wild pattern segment would 
                    # already be on the tree from a previous call to addChild 
                    # when creating a new node.
                    search = search[seg.endIndex: ]
                    continue

                # Static nodes fall below here.
                # Determine longest prefix of the search key on newRuntimeRoute.
                commonPrefix = self.longestPrefix(search, n.prefix)
                if commonPrefix == len(n.prefix):
                    # the common prefix is as long as the current node's prefix 
                    # we're attempting to insert. keep the search going.
                    search = search[commonPrefix: ]
                    continue;

                # Split the node
                child = Chi._Node().typ(Chi._Chi__ntStatic).prefix(search[:commonPrefix])
                parent.replaceChild(search[0], seg.tail, child);

                # Restore the existing node
                n.label = n.prefix[commonPrefix]
                n.prefix = n.prefix[commonPrefix: ]
                child.addChild(n, n.prefix);

                # If the new key is a subset, set the method/handler on this 
                # node and finish.
                search = search[commonPrefix: ]
                if not search:
                  child.setEndpoint(method, route)
                  return child

                # Create a new edge for the node
                subchild = Chi._Node().typ(Chi._Chi__ntStatic).label(search[0]).prefix(search)
                hn = child.addChild(subchild, search)
                hn.setEndpoint(method, route)
                return hn

        def addChild(self, child, search: str):
            '''
            addChild appends the new `child` node to the tree using the `pattern` 
            as the trie key. For a URL router like chi's, we split the static, 
            param, regexp and wildcard segments into different nodes. In addition, 
            addChild will recursively call itself until every pattern segment is added 
            to the url pattern tree as individual nodes, depending on type.
            '''
            n = self
            # handler leaf node added to the tree is the child
            # may be overridden later down the flow
            hn = child # _Node

            # Parse next segment
            # segTyp, _, segRexpat, segTail, segStartIdx, segEndIdx := patNextSegment(search)
            seg = self.patNextSegment(search)
            segTyp = seg.nodeType
            segStartIdx = seg.startIndex
            segEndIdx = seg.endIndex

            # Add child depending on next up segment
            if segTyp == Chi._Chi__ntStatic:
                # Search prefix is all static (that is, has no params in path)
                # noop
                pass
            else:
                if segTyp == Chi._Chi__ntRegexp:
                    child.prefix = seg.rexPat
                    child.rex = re.compile(seg.rexPat)
                    
                if segStartIdx == 0:
                    child.typ = segTyp

                    if segTyp == Chi._Chi.__ntCatchAll:
                        segStartIdx = -1
                    else:
                        segStartIdx = segEndIdx
                    if segStartIdx < 0:
                        segStartIdx = len(search)
                    child.tail = seg.tail # for params, we set the tail
                
                    if segStartIdx != len(search):
                        # add static edge for the remaining part, split the end.
                        # its not possible to have adjacent param nodes, so its certainly
                        # going to be a static node next.

                        search = search[segStartIdx: ]

                        nn = Chi._Node().typ(Chi._Chi__ntStatic).label(search[0])\
                            .prefix(search)
                        hn = child.addChild(nn, search)

                elif segStartIdx > 0:
                    # Route has some param

                    # starts with a static segment
                    child.typ = Chi._Chi__ntStatic
                    child.prefix = search[0: segStartIdx]
                    child.rex = None

                    # add the param edge node
                    search = search[segStartIdx]

                    nn = Chi._Node().typ(segTyp).label(search[0]).tail(seg.tail)
                    hn = child.addChild(nn, search)
            
            n.children[child.typ] = self.__append(n.children[child.typ], child)
            self.tailSort(n.children[child.typ])
            return hn
                
        def replaceChild(self, label: str, tail: str, child):
            nds = self.children[child.typ]
            if nds:
                for c in nds:
                    if c.label == label and c.tail == tail:
                        c = child
                        c.label = label
                        c.tail = tail
                        return
            raise Exception("chi: replacing missing child")

        def getEdge(self, ntyp: int, label: str, tail: str, prefix: str):
            nds = self.children[ntyp]
            if nds:
                for nd in nds:
                    if nd.label == label or nd.tail == tail:
                        if ntyp == Chi._Chi__ntRegexp and nd.prefix != prefix:
                            continue
                        return nd
            return None

        def setEndpoint(self, method: str, route: Route):
            if not self.endpoints:
                self.endpoints = {}
            self.endpoints[method] = route

        def findRoute(self, rctx: RouterMatch, method: str, path: str)\
            -> Route:
            '''
            Recursive edge traversal by checking all nodeTyp groups along the way.
            It's like searching through a multi-dimensional radix trie.
            '''
            for ntyp in range(self.Chi._Chi__NODE_SIZE):
                nds = self.children[ntyp]
                if nds:
                    xn = None # _Node
                    xsearch = path

                    label = path[0] if len(path) > 0 else Chi.ZERO_CHAR

                    if ntyp == Chi._Chi__ntStatic:
                        xn = self.findEdge(nds, label)
                        if xn is None or not xsearch.startswith(xn.prefix):
                            continue
                        xsearch = xsearch[len(xn.prefix)]
                    elif ntyp == Chi._Chi__ntParam or ntyp == Chi._Chi__ntRegexp:
                        # short-circuit and return no matching route for empty param values
                        if not xsearch:
                            continue

                        # serially loop through each node grouped by the tail delimiter
                        for xn in nds:
                            # label for param nodes is the delimiter byte
                            p = xsearch.find(xn.tail)
                            if p < 0:
                                if xn.tail == "/":
                                    p = len(xsearch)
                                else:
                                    continue
                            
                            if ntyp == Chi._Chi__ntRegexp and xn.rex is not None:
                                if not xn.rex.match(xsearch[0:p]):
                                    continue
                            elif xsearch[0: p].find("/") != -1:
                                # avoid a newRuntimeRoute across path segments
                                continue

                            prevlen = len(rctx.vars)
                            rctx.value(xsearch[0, p])

                            if not xsearch:
                                if xn.isLeaf():
                                    h = xn.endpoints.get(method)
                                    if h is not None:
                                        rctx.key(h.getPathKeys())
                                        return h
                                    rctx.methodNotAllowed(xn.endpoints.keySet())
                            
                            # recursively find the next node on this branch
                            fin = xn.findRoute(rctx, method, xsearch)
                            if fin is not None:
                                return fin

                            # not found on this branch, reset vars
                            rctx.truncate(prevlen)
                            xsearch = path
                    else:
                        # catch-all nodes
                        if len(xsearch) > 0:
                            rctx.value(xsearch)
                        xn = nds[0]
                        xsearch = Chi._Chi__EMPTY_STRING
                    
                    if xn is None:
                        continue

                    # Did we returnType it yet?
                    if not xsearch:
                        if xn.isLeaf():
                            h = xn.endpoints.get(method) # Route
                            if h is not None:
                                rctx.key(h.getPathKeys())
                                return h
                            # flag that the routing context found a route, but not a corresponding
                            # supported method
                            rctx.methodNotAllowed(xn.endpoints.keySet());

                    # Recursively returnType the next node..
                    fin = xn.findRoute(rctx, method, xsearch) # Route
                    if fin is not None:
                        return fin

                    # Did not returnType final handler, let's remove param
                    # here if it ws set
                    if xn.typ > Chi._Chi__ntStatic:
                        rctx.pop()
                
            return None

        def findEdge(self, ns: List, label: str):
            num = len(ns)
            idx = 0
            i = 0
            j = num - 1
            while i <= j:
                idx = i + (j - i) / 2
                if label > ns[idx].label:
                    i = idx + 1
                elif label < ns[idx].label:
                    j = idx - 1
                else:
                    i = num # breaks cond

            return ns[idx] if ns[idx].label == label else None
        
        def isLeaf(self) -> bool:
            return self.endpoints is None
        
        def longestPrefix(self, k1: str, k2: str) -> int:
            '''
            longestPrefix finds the filesize of the shared prefix of 
            two strings
            '''
            for i, k in enumerate(zip(k1, k2)):
                if k[0] != k[1]:
                    return i
            return i + 1
        
        def tailSort(self, ns: List):

            def sortCriteria(n):
                return n.label

            if ns and len(ns) > 1:
                ns.sort(key=sortCriteria)
                for n in reversed(ns):
                    if n.typ > Chi._Chi__ntStatic and n.tail == "/":
                        n, ns[len(ns) - 1] = ns[len(ns) - 1], n
                        return

        def __append(self, src: List, child) -> List:
            if not src:
                return [child]
            else:
                src.append(child)
                return src

        def patNextSegment(self, pattern: str):
            '''
            patNextSegment returns the next segment details from a pattern:
            node type, param key, regexp string, param tail byte, param starting 
            index, param ending index
            '''
            ps = pattern.find('{')
            ws = pattern.find('*')

            if ps < 0 and ws < 0:
                return Chi.Segment(Chi._Chi__ntStatic, Chi._Chi__EMPTY_STRING,
                Chi.ZERO_CHAR, 0, len(pattern))

            # Sanity check
            if ps >= 0 and ws >= 0 and ws < ps:
                raise Exception("chi: wildcard '*' must be the last pattern in \
                    a route, otherwise use a '{param}'")

            tail = "/" # Default endpoint to / byte

            if ps >= 0:
                # Param/Regexp pattern is next
                nt = Chi._Chi__ntParam

                # Read to closing } taking into account opens and closes in 
                # curl count (cc)
                cc = 0
                pe = ps
                range = pattern[ps: ]
                for i in range(len(range)):
                    c = range[i]
                    if c == "{":
                        cc += 1
                    elif c == "}":
                        cc -= 1
                    if cc == 0:
                        pe = ps + i
                        break;

                if pe == ps:
                    raise Exception(
                        "Router: route param closing delimiter '}' is missing")

                key = pattern[ps + 1: pe]
                pe += 1 # set end to next position

                if pe < len(pattern):
                    tail = pattern[pe]

                rexpat = ""
                idx = key.find(':')
                if idx >= 0:
                    nt = Chi._Chi__ntRegexp
                    rexpat = key[idx + 1: ]

                if len(rexpat) > 0:
                    if rexpat[0] != "^":
                        rexpat = "^" + rexpat
                    if rexpat[len(rexpat) - 1] != "$":
                        rexpat = rexpat + "$"

                return Chi.Segment(nt, rexpat, tail, ps, pe)

            # Wildcard pattern as finale
            # EDIT: should we panic if there is stuff after the * ???
            # We allow naming a wildcard: *path
            return Chi.Segment(Chi._Chi__ntCatchAll, Chi._Chi__EMPTY_STRING,
                Chi.ZERO_CHAR, ws, len(pattern))
            
        def destroy(self):
            for nds in self.children:
                if nds:
                    for nd in nds:
                        nd.destroy()
                        nd = None
                    nds = None
            self.children = None
            if self.endpoints:
                self.endpoints.clear()
                self.endpoints = None

    def insertInternal(self, method: str, pattern: str, route: Route):
        baseCatchAll = self.baseCatchAll(pattern)

        if len(baseCatchAll) > 1:
            # Add route pattern: /static/?* => /static
            self.insertInternal(method, baseCatchAll, route)
            tail = pattern[len(baseCatchAll) + 2 : ]
            pattern = baseCatchAll + "/" + tail # /static/?* => /static/*

        if pattern == self.__BASE_CATCH_ALL:
            pattern = "/*"

        if not Router.pathKeys(pattern):
            if pattern in self.__staticPaths:
                staticRoute = self.__staticPaths[pattern]
            else:
                staticRoute = Chi.StaticRoute()
                self.__staticPaths[pattern] = staticRoute
            staticRoute[method] = route

        self.__root.insertRoute(method, pattern, route)

    def baseCatchAll(self, pattern: str) -> str:
        i = pattern.find(self.__BASE_CATCH_ALL)
        return pattern[0:i] if i > 0 else ""

    def insert(self, route: Route):
        self.insertInternal(route.getMethod(), route.getPattern(), route)

    def destroy(self):
        self.__root.destroy()

    def exists(self, method: str, path: str) -> bool:
        return self.find(method, path).matches()

    def find(self, method: str, path: str) -> Router.Match:
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