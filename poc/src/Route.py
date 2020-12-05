class Route:
    """
    Favicon handler as a silent 404 error.
    """
    FAVICON = lambda ctx: ctx.send(StatusCode.NOT_FOUND) # Handler # ctx -> ctx.send(StatusCode.NOT_FOUND);
    __EMPTY_LIST = [] # final # List # Collections.emptyList()
    __EMPTY_MAP = {} # final # Map # Collections.emptyMap()

    """
    Creates a new route.
    @param method HTTP method. (@Nonnull String)
    @param pattern Path pattern. (@Nonnull String)
    @param handler Route handler. (@Nonnull Handler)
    """
    def __init__(self, method, pattern, handler):
        self.__decoders = Route.__EMPTY_MAP # Map<String, MessageDecoder>
        self.__pattern = pattern # final # String
        self.__method = method.upper() # final # String
        self.__pathKeys = Route.__EMPTY_LIST # List<String>
        self.__before = None # Before
        self.__decorator = None # Decorator
        self.__handler = handler # Handler
        self.__after = None # After
        self.__pipeline = None # Handler
        self.__encoder = None # MessageEncoder
        self.__returnType = None # Type
        self.__handle = handler # object
        self.__produces = Route.__EMPTY_LIST # List<MediaType>
        self.__consumes = Route.__EMPTY_LIST # List<MediaType>
        self.__attributes = None # Map<String, Object> # new TreeMap<>(String.CASE_INSENSITIVE_ORDER)
        self.__supportedMethod = None # Set<String>
        self.__executorKey = None # String
        self.__tags = Route.__EMPTY_LIST # List<String>
        self.__summary = None # String
        self.__description = None # String

    class Aware:
        def setRoute(self, route:Route):
            pass
    class Handler:
        pass
    class Decorator(Aware):
        def apply(self, next:Handler) -> Handler:
            pass
        def then_Decorator(self, next:Decorator) -> Decorator:
            return lambda h : apply(next.apply(h))
        def then_Handler(self, next:Handler) -> Handler:
            return lambda ctx : apply(next).apply(ctx)
    class Before:
        def inner_then(self, ctx, next):
            apply(ctx)
            if not ctx.isResponseStarted():
                return next.apply(ctx)
            return ctx
        def apply(self, ctx:Context):
            raise Exception
        def then(self, next):
            return lambda ctx : inner_then(ctx, next)
    class After:
        pass

    def getPattern(self) -> str:
        return self.__pattern

    def getMethod(self) -> str:
        return self.__method

    def getPathKeys(self) -> list[str]:
        return self.__pathKeys

    def setPathKeys(self, pathKeys: list[str]):
        self.__pathKeys = pathKeys
        return self

    def getHandler(self) -> Handler:
        return self.__handler

    def getPipeline(self) -> Handler:
        if self.__pipeline is None:
            self.__pipeline = self.computePipeline()
        return self.__pipeline

    def getBefore(self) -> Before:
        return self.__before

    def setBefore(self, before: Before):
        self.__before = before
        return self

    def getAfter(self):
        return self.__after

    def setAfter(self, after: After):
        self.__after = after
        return self
    
    def getDecorator(self):
        return self.__decorator

    def setDecorator(self, decorator: Decorator):
        self.__decorator = decorator
        return self

    def getEncoder(self) -> MessageEncoder:
        return self.__encoder

    def setEncoder(self, encoder: MessageEncoder):
        self.__encoder = encoder
        return self

    def getReturnType(self): # Type
        return self.__returnType
    
    def setReturnType(self, returnType): # Type
        self.__returnType = returnType
        return self

    def getDecoders(self) -> dict[str, MessageDecoder]:
        return self.__decoders

    def setDecoders(self, decoders: dict[str, MessageDecoder]):
        self.__decoders = decoders
        return self

    def setExecutorKey(self, key: str):
        self.__executorKey = key
        return self

    def getExecutorKey(self) -> str:
        return self.__executorKey

    def setReturnType(self, returntype: object):
        self.__returnType = returntype
        return self

    def getReturnType(self) -> object:
        return self.__returnType
    
    def computePipeline(self) -> Handler:
        pipeline = None # Route.Handler
        if self.__decorator is None:
            pipeline = self.__handler
        else:
            pipeline = self.__decorator.then(self.__handler)

        if self.__before is not None:
            pipeline = self.__before.then(pipeline)
        
        if self.__after is not None:
            pipeline = pipeline.then(self.__after)

        return pipeline