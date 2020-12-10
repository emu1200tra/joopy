from src import Route
from src import Router
from src import MediaType
from src.handler import *

class RouterImpl(Router):
    class PathBuilder:
        def __init__(self, *args):
            self.__buffer = None # StringBuilder
            for path in args:
                self.append(path)

        def append(self, path):
            if path != "/":
                if self.__buffer is None:
                    self.__buffer = ""
                self.__buffer += path

            return self

        def toString(self):
            if self.__buffer is None:
                return "/"
            else:
                return self.__buffer

    class Stack:
        def __init__(self, tree, pattern):
            self.__tree = tree # RouteTree
            self.__pattern = pattern # String
            self.__executor = None # Executor
            self.__decoratorList = [] # List<Route.Decorator> # new ArrayList<>()
            self.__afterList = [] # List<Route.After> # new ArrayList<>()
            self.__beforeList = [] # List<Route.Before> # new ArrayList<>()

        # filter is Route.Decorator, Route.Before, Route.After
        def then(self, filter):
            if isinstance(filter, Route.Decorator):
                self.__decoratorList.append(filter)
            elif isinstance(filter, Route.After):
                self.__afterList.append(filter)
            elif isinstance(filter, Route.Before):
                self.__beforeList.append(filter)

        def hasPattern(self):
            return self.__pattern is not None

        def clear(self):
            self.__decoratorList = []
            self.__afterList = []
            self.__beforeList = []
            self.__executor = None

        def executor(self, executor):
            self.__executor = executor
            return self

    __ROUTE_MARK = None # Route # new Route(Router.GET, "/", null)

    def __init__(self, loader):
        super(RouterImpl, self).__init__()
        self.__err = None # ErrorHandler
        self.__errorCodes = None # Map<String, StatusCode>
        self.__chi = None # RouteTree # new Chi()
        self.__stack = [] # LinkedList<Stack> # new LinkedList<>()
        self.__routes = [] # List<Route> # new ArrayList<>()
        self.__encoder = None # HttpMessageEncoder # new HttpMessageEncoder()
        self.__basePath = None # String
        self.__predicateMap = None # Map<Predicate<Context>, RouteTree>
        self.__worker = None # Executor # new ForwardingExecutor()
        self.__routeExecutor = {} # Map<Route, Executor> # new HashMap<>()
        self.__decoders = {} # Map<String, MessageDecoder> # new HashMap<>()
        self.__attributes = None # Map<String, Object> # new ConcurrentHashMap<>()
        self.__handlers = [] # List<ResponseHandler> # new ArrayList<>()
        self.__services = None # ServiceRegistry # new ServiceRegistryImpl()
        self.__sessionStore = None # SessionStore # SessionStore.memory()
        self.__flashCookie = None # Cookie # new Cookie("jooby.flash").setHttpOnly(true)
        self.__converters = ValueConverters.defaultConverters() # List<ValueConverter>
        self.__beanConverters = None # List<BeanConverter> # new ArrayList<>(3)
        self.__classLoader = loader # ClassLoader
        self.__preDispatchInitializer = None # ContextInitializer
        self.__postDispatchInitializer = None # ContextInitializer
        self.__routerOptions = None # Set<RouterOption> # EnumSet.of(RouterOption.RESET_HEADERS_ON_ERROR)
        self.__trustProxy = None # boolean
        self.__contextAsService = None # boolean

        self.__stack.append(RouterImpl.Stack(self.__chi, None))


    def decorator(self, decorator: Route.Decorator) -> Router:
        self.__stack[-1].then(decorator)
        return self

    def after(self, after: Route.After) -> Router:
        self.__stack[-1].then(after)
        return self

    def before(self, before: Route.Before) -> Router:
        self.__stack[-1].then(before)
        return self

    def routes(self, action: Runnable) -> RouteSet:
        return self.path("/", action)
    
    def path(self, pattern: str, action: Runnable) -> RouteSet:
        RouteSet routeSet = RouteSet()
        start = len(self.__routes)
        self.newStack(self.__chi, pattern, action)
        routeSet.setRoutes(self.__routes.subList(start, self.__routes.size())) # TODO: sublist function
        return routeSet

    def route(self, method, pattern, handler):
        return self.newRoute(method, pattern, handler)

    def newRoute(self, method, pattern, handler):
        tree = self.__stack[-1]._Stack__tree # RouteTree
        """ Pattern: """
        pathBuilder = RouterImpl.PathBuilder() # PathBuilder
        for stack in self.__stack:
            if stack.hasPattern():
                pathBuilder.append(stack._Stack__pattern)
        pathBuilder.append(pattern)

        """ Before: """
        before = None # Route.Before
        for stack in self.__stack:
            for next in stack._Stack__beforeList:
                if next is None:
                    before = next
                else:
                    before.then(next)

        """ Decorator: """
        decoratorList = [d for stack in self.__stack for d in stack._Stack__decoratorList]
        decorator = None # Route.Decorator
        for next in decoratorList:
            if next is None:
                decorator = next
            else:
                decorator.then(next)

        """ After: """
        after = None # Route.After
        for stack in self.__stack:
            for next in stack._Stack__afterList:
                if next is None:
                    after = next
                else:
                    after.then(next)

        """ Route: """
        safePattern = pathBuilder.toString() # String
        route = Route(method, safePattern, handler) # Route
        route.setPathKeys(Router.pathKeys(safePattern))
        route.setBefore(before)
        route.setAfter(after)
        route.setDecorator(decorator)
        route.setEncoder(self.__encoder)
        route.setDecoders(self.__decoders)

        for it in decoratorList:
            it.setRoute(route)
        handler.setRoute(route)

        stack = self.__stack[-1] # Stack
        if stack.executor is not None:
            self.__routeExecutor[route] = stack.executor

        finalPattern = None # String
        if self.__basePath is None:
            finalPattern = safePattern
        else:
            finalPattern = RouterImpl.PathBuilder(self.__basePath, safePattern).toString()

        if self.__routerOptions.contains(RouterOption.IGNORE_CASE):
            finalPattern = finalPattern.lower()

        for routePattern in Router.expandOptionalVariables(finalPattern):
            if route.getMethod() == "WS":
                tree.insert(Router.GET, routePattern, route)
                route.setReturnType(Context)
            elif route.getMethod() == "SSE":
                tree.insert(Router.GET, routePattern, route)
                route.setReturnType(Context)
            else:
                tree.insert(route.getMethod(), routePattern, route)

                if route.isHttpOptions():
                    tree.insert(Router.OPTIONS, routePattern, route)
                elif route.isHttpTrace():
                    tree.insert(Router.TRACE, routePattern, route)
                elif route.isHttpHead() and route.getMethod() == Router.GET:
                    tree.insert(Router.HEAD, routePattern, route)

        self.__routes.add(route)

        return route

    """
    @param app (@Nonnull Jooby)
    @return Router.
    """
    def start(self, app):
        if self.__err == None:
            self.__err = ErrorHandler.create()
        else:
            self.__err = self.__err.then(ErrorHandler.create())

        # TODO: HttpMessageEncoder is not implemented yet
        # TODO: MessageEncoder is not implemented yet
        # TODO: ValueConverters is not implemented yet
        # TODO: ClassSource is not implemented yet
        # TODO: RouteAnalyzer is not implemented yet
        self.__encoder.add(MessageEncoder.TO_STRING)
        source = ClassSource(self.__classLoader)
        analyzer = RouteAnalyzer(source, False)

        mode = app.getExecutionMode()

        for route in self.__routes:
            executorKey = route.getExecutorKey()

            # TODO: executor in java, concurrent.futures.threadpoolexecutor in python (?)
            executor = None
            if executorKey == None:
                executor = self.__routeExecutor.get(route)
                # TODO: ForwardingExecutor
            else:
                # TODO: ForwardingExecutor
                pass

            if route.getReturnType() == None:
                route.setReturnType(analyzer.returnType(route.getHandle()))
                pass

            # TODO: class MediaType is not implemented yet
            if isinstance(route.getHandler(), WebSocketHandler):
                if not route.getConsumes(): # empty
                    singletonList = [MediaType.json]
                    route.setConsumes(singletonList)
                if not route.getProduces(): # empty
                    singletonList = [MediaType.json]
                    route.setProduces(singletonList)
            else:
                # TODO: prependMediaType
                # TODO: SUPPORT_MEDIA_TYPE, ACCEPT in Route.py
                route.setBefore(prependMediaType(route.getConsumes(), route.getBefore(), Route.SUPPORT_MEDIA_TYPE))
                route.setBefore(prependMediaType(route.getProduces(), route.getBefore(), Route.ACCEPT))
                pass

            # TODO: Pipeline is not implemented yet
            pipeline = Pipeline()

            # Final render
            Route.setEncoder(self.__encoder)

        return self

    def destroy(self):
        self.__routes.clear()
        self.__routes = None
        self.__chi.destroy()
        if self.__errorCodes is not None:
            self.__errorCodes.clear()
            self.__errorCodes = None
        if self.__predicateMap is not None:
            for key, value in self.__predicateMap.items():
                self.__predicateMap[key].destroy()
            self.__predicateMap.clear()
            self.__predicateMap = None

    def newStack(self, tree: RouteTree = None, pattern: str = None, stack: Stack = None, action: Runnable, decorator: list[Route.Decorator]) -> Router:
        # TODO: use @dispatch to overload
        if stack is None:
            if tree is None or pattern is None:
                return 
            else:
                stack = self.newStack(self.push(tree, pattern), action, decorator)
        for d in decorator:
            stack.then(d)
        self.__stack.append(stack)
        if action is not None:
            action.run()
        self.__stack.pop().clear()
        return self

    def push(self, tree: RouteTree, pattern: str = None) -> Stack:
        stack = RouterImpl.Stack(tree, Router.leadingSlash(pattern))
        if len(self.__stack) > 0:
            parent = self.__stack[-1]
            stack.executor = parent.executor
        return stack