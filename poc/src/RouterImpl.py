class RouterImpl(Router):
    __ROUTE_MARK = None # Route # new Route(Router.GET, "/", null)
    
    def __init__(self):
        self.__err = None # ErrorHandler
        self.__errorCodes = None # Map<String, StatusCode>
        self.__chi = None # RouteTree # new Chi()
        self.__stack = None # LinkedList<Stack> # new LinkedList<>()
        self.__routes = [] # List<Route> # new ArrayList<>()
        self.__encoder = None # HttpMessageEncoder # new HttpMessageEncoder()
        self.__basePath = None # String
        self.__predicateMap = None # Map<Predicate<Context>, RouteTree>
        self.__worker = None # Executor # new ForwardingExecutor()
        self.__routeExecutor = None # Map<Route, Executor> # new HashMap<>()
        self.__decoders = None # Map<String, MessageDecoder> # new HashMap<>()
        self.__attributes = None # Map<String, Object> # new ConcurrentHashMap<>()
        self.__handlers = None # List<ResponseHandler> # new ArrayList<>()
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

        # this.classLoader = loader
        # stack.addLast(new Stack(chi, null))

        # converters = ValueConverters.defaultConverters()
        # beanConverters = new ArrayList<>(3)
    
    """
    @param app (@Nonnull Jooby)
    @return Router.
    """
    def start(self, app):
        mode = app.getExecutionMode()
        
        return self
