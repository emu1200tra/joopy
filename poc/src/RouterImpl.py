from multipledispatch import dispatch
from typing import List
from .todo import *
from .Route import Route
from .Router import Router
from .Chi import Chi
from .handler.web_socket_handler import WebSocketHandler
from .HttpMessageEncoder import HttpMessageEncoder
from .MessageEncoder import MessageEncoder
from .pipeline import Pipeline
from .ExecutionMode import ExecutionMode
from .handler.default_error_handler import DefaultErrorHandler
from .route_analyzer import RouteAnalyzer
from .context import Context

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

    __ROUTE_MARK = Route(Router.GET, "/", None) # Route

    def __init__(self, loader):
        super(RouterImpl, self).__init__()
        self.__err = None # ErrorHandler
        self.__errorCodes = None # Map<String, StatusCode>
        self.__chi = Chi()
        self.__stack = [] # LinkedList<Stack> # new LinkedList<>()
        self.__routes = [] # List<Route> # new ArrayList<>()
        self.__encoder = HttpMessageEncoder() # HttpMessageEncoder # new HttpMessageEncoder()
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
        self.__routerOptions = set(RouterOption.RESET_HEADERS_ON_ERROR) # Set<RouterOption> # EnumSet.of(RouterOption.RESET_HEADERS_ON_ERROR)
        self.__trustProxy = None # boolean
        self.__contextAsService = None # boolean
        self.__stack.append(RouterImpl.Stack(self.__chi, None))

    def decorator(self, decorator: Route.Decorator) -> Router:
        self.__stack[-1].then(Route.Decorator(decorator))
        return self

    def after(self, after: Route.After) -> Router:
        self.__stack[-1].then(Route.After(after))
        return self

    def before(self, before: Route.Before) -> Router:
        self.__stack[-1].then(Route.Before(before))
        return self

    def routes(self, action: Runnable) -> RouteSet:
        return self.path("/", action)

    def path(self, pattern: str, action: Runnable) -> RouteSet:
        routeSet = RouteSet()
        start = len(self.__routes)
        self.newStack(self.__chi, pattern, action)
        routeSet.set_route(self.__routes.subList(start, self.__routes.size())) # TODO: sublist function
        return routeSet

    def route(self, method, pattern, handler):
        return self.new_route(method, pattern, Route.Handler(handler))

    def new_route(self, method, pattern, handler):
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
        route.set_path_keys(Router.pathKeys(safePattern))
        route.set_before(before)
        route.set_after(after)
        route.set_decorator(decorator)
        route.set_encoder(self.__encoder)
        route.set_decoders(self.__decoders)

        for it in decoratorList:
            it.set_route(route)
        handler.set_route(route)

        stack = self.__stack[-1] # Stack
        if stack.executor is not None:
            self.__routeExecutor[route] = stack.executor

        finalPattern = None # String
        if self.__basePath is None:
            finalPattern = safePattern
        else:
            finalPattern = RouterImpl.PathBuilder(self.__basePath, safePattern).toString()

        if RouterOption.IGNORE_CASE in self.__routerOptions:
            finalPattern = finalPattern.lower()


        for routePattern in Router.expandOptionalVariables(finalPattern):
            if route.get_method() == "WS":
                tree.insert(Router.GET, routePattern, route)
                route.set_return_type(Context)
            elif route.get_method() == "SSE":
                tree.insert(Router.GET, routePattern, route)
                route.set_return_type(Context)
            else:
                tree.insert(route.get_method(), routePattern, route)

                # if route.isHttpOptions():
                #     tree.insert(Router.OPTIONS, routePattern, route)
                # elif route.isHttpTrace():
                #     tree.insert(Router.TRACE, routePattern, route)
                # elif route.isHttpHead() and route.get_method() == Router.GET:
                #     tree.insert(Router.HEAD, routePattern, route)

        self.__routes.append(route)

        return route

    """
    @param app (@Nonnull Jooby)
    @return Router.
    """
    def start(self, app):
        if self.__err is None:
            self.__err = DefaultErrorHandler()
        else:
            self.__err = self.__err.then(DefaultErrorHandler())

        self.__encoder.add(MessageEncoder.TO_STRING)

        # ValueConverters.addFallbackConverters(self.__converters)
        # ValueConverters.addFallbackBeanConverters(self.__beanConverters)

        # source = ClassSource(self.__classLoader)
        # analyzer = RouteAnalyzer(source, False)

        mode = app.getExecutionMode()

        for route in self.__routes:
            executorKey = route.get_executor_key()
            executor = None
            """
            if executorKey is None:
                executor = self.__routeExecutor.get(route)
            else:
                if executorKey == "worker":
                    if isinstance(executore, ForwardingExecutor):
                        executor = ...
                    else:
                        executor = self.__worker
            """

            if route.get_return_type() is None:
                # TODO: str is analyzer.returnType(route.get_handle())
                route.set_return_type(str)

            if isinstance(route.get_handler(), WebSocketHandler):
                if not route.get_consumes(): # empty
                    singletonList = [MediaType.json]
                    route.set_consumes(singletonList)
                if not route.get_produces(): # empty
                    singletonList = [MediaType.json]
                    route.set_produces(singletonList)
            else:
                route.set_before(self.__prepend_media_type(route.get_consumes(), route.get_before(), Route.SUPPORT_MEDIA_TYPE))
                route.set_before(self.__prepend_media_type(route.get_produces(), route.get_before(), Route.ACCEPT))

            # Route.Handler  # TODO: None is source.get_loader()
            pipeline = Pipeline.compute(None, route, \
                    self.__force_mode(route, mode), executor, \
                    self.__postDispatchInitializer, self.__handlers)
            route.set_pipeline(pipeline)

            # Final render
            route.set_encoder(self.__encoder)

        self.__chi.set_encoder(self.__encoder)
        if RouterOption.IGNORE_CASE in self.__routerOptions:
            pass # chi = new RouteTreeLowerCasePath(chi)
        if RouterOption.IGNORE_TRAILING_SLASH in self.__routerOptions:
            pass # chi = new RouteTreeIgnoreTrailingSlash(chi)
        if RouterOption.NORMALIZE_SLASH in self.__routerOptions:
            pass # chi = new RouteTreeNormPath(chi)

        """
        // unwrap executor
        worker = ((ForwardingExecutor) worker).executor;
        this.stack.forEach(Stack::clear);
        this.stack = null;
        routeExecutor.clear();
        routeExecutor = null;
        source.destroy();
        return this;
        """

        return self

    def __force_mode(self, route: Route, mode: ExecutionMode) -> ExecutionMode:
        if route.get_method() == Router.WS: # "WS" string compare
            return ExecutionMode.WORKER
        return mode

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

    @dispatch(object, str, Runnable, list)
    def newStack(self, tree: object, pattern: str, action: Runnable, decorator: List[Route.Decorator]) -> Router:
        return self.newStack(self.push(tree, pattern), action, decorator)

    @dispatch(Stack, Runnable, list)
    def newStack(self, stack: Stack, action: Runnable, decorator: List[Route.Decorator]) -> Router:
        for d in decorator:
            stack.then(d)
        self.__stack.append(stack)
        if action is not None:
            action.run()
        self.__stack.pop().clear()
        return self

    def push(self, tree: object, pattern: str = None) -> Stack:
        stack = RouterImpl.Stack(tree, Router.leadingSlash(pattern))
        if len(self.__stack) > 0:
            parent = self.__stack[-1]
            stack.executor = parent.executor
        return stack

    def match(self, context):
        #if self.__predicateMap != None:
        #   deal with matching if predicateMap exists
        #   otherwise deal with chi.find
        #   predicateMap not implemented now
        #   use chi to find element directly
        return self.__chi.find(context.get_method(), context.get_request_path())

    def __prepend_media_type(self, contentTypes: List[MediaType], before: Route.Before, prefix: Route.Before) -> Route.Before:
        if len(contentTypes) > 0:
            if before is None:
                return prefix
            else:
                return prefix.then(before)
        else:
            return before
