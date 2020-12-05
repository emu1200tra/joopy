from src import Route
from src import Router

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

    def __init__(self):
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
        self.__converters = None # List<ValueConverter>
        self.__beanConverters = None # List<BeanConverter>
        self.__classLoader = None # ClassLoader
        self.__preDispatchInitializer = None # ContextInitializer
        self.__postDispatchInitializer = None # ContextInitializer
        self.__routerOptions = None # Set<RouterOption> # EnumSet.of(RouterOption.RESET_HEADERS_ON_ERROR)
        self.__trustProxy = None # boolean
        self.__contextAsService = None # boolean

        # TODO: constructor
        # this.classLoader = loader
        self.__stack.append(RouterImpl.Stack(self.__chi, None))
        # converters = ValueConverters.defaultConverters()
        # beanConverters = new ArrayList<>(3)
    
    """
    @param app (@Nonnull Jooby)
    @return Router.
    """
    def start(self, app):
        # TODO: ErrorHandler Class is not implemented yet
        if self.__err == None:
            self.__err = ErrorHandler.create()
        else:
            self.__err = self.__err.then(ErrorHandler.create())

        # TODO: HttpMessageEncoder is not implemented yet
        # TODO: ValueConverters is not implemented yet

        source = ClassSource(classLoader)
        analyzer = RouteAnalyzer(source, false)
        
        #ClassSource source = new ClassSource(classLoader);
        #RouteAnalyzer analyzer = new RouteAnalyzer(source, false);

        # TODO: ClassSource is not implemented yet
        # TODO: RouteAnalyzer is not implemented yet
        
        mode = app.getExecutionMode()

        for route in self.__routes:
            executorKey = route.getExecutorKey();
            
            # TODO: executor in java, concurrent.futures.threadpoolexecutor in python (?)
            executor = None
            if executorKey == None:
                executor = self.__routeExecutor.get(route)
                # TODO: ForwardingExecutor
            else:
                # TODO: ForwardingExecutor
                pass

            if route.getReturnType() == None:
                # route.setReturnType()
                pass
        
        """
        for (Route route : routes) {
            String executorKey = route.getExecutorKey();
            Executor executor;
            if (executorKey == null) {
                executor = routeExecutor.get(route);
                if (executor instanceof ForwardingExecutor) {
                    executor = ((ForwardingExecutor) executor).executor;
                }
            } else {
                if (executorKey.equals("worker")) {
                executor = (worker instanceof ForwardingExecutor)
                    ? ((ForwardingExecutor) worker).executor
                    : worker;
                } else {
                    executor = executor(executorKey);
                }
            }
            /** Return type: */
            if (route.getReturnType() == null) {
                route.setReturnType(analyzer.returnType(route.getHandle()));
            }

            /** Default web socket values: */
            if (route.getHandler() instanceof WebSocketHandler) {
                if (route.getConsumes().isEmpty()) {
                // default type
                route.setConsumes(Collections.singletonList(MediaType.json));
                }
                if (route.getProduces().isEmpty()) {
                // default type
                route.setProduces(Collections.singletonList(MediaType.json));
                }
            } else {
                /** Consumes && Produces (only for HTTP routes (not web socket) */
                route.setBefore(
                    prependMediaType(route.getConsumes(), route.getBefore(), Route.SUPPORT_MEDIA_TYPE));
                route.setBefore(prependMediaType(route.getProduces(), route.getBefore(), Route.ACCEPT));
            }
            /** Response handler: */
            Route.Handler pipeline = Pipeline
                .compute(source.getLoader(), route, forceMode(route, mode), executor, postDispatchInitializer, handlers);
                route.setPipeline(pipeline);
            /** Final render */
            route.setEncoder(encoder);
        }
        """
        
        
        return self

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