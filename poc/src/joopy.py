import abc
import sys
from src import wsgi
from src import Router
from src import Registry
from src import RouterImpl
from src.Server import Base
from src.wsgi import wsgi

# routers = {}

# def runApp():
#     wsgi.start(routers)

# def get(route):
#     def decorator(func):
#         routers[route] = ("GET", func)
#         return func
#     return decorator

def not_none(*args, **kargs):
    for a in args:
        if a is None:
            raise TypeError("Argument can not be None.")
    for a in kargs:
        if a is None:
            raise TypeError("Argument can not be None.")

class Joopy(Router, Registry):
    # static final variable
    BASE_PACKAGE = "application.package"
    APP_NAME = "___app_name__"
    
    __JOOPY_RUN_HOOK = "___joopy_run_hook__"
    __started = True
    
    """
    Creates a new Jooby instance.
    """
    def __init__(self):
        self.__router = None # RouterImpl
        self.__mode = None # ExecutionMode
        self.__tmpdir = None # Path
        self.__readyCallbacks = [] # List<SneakyThrows.Runnable>
        self.__startingCallbacks = [] # List<SneakyThrows.Runnable>
        self.__stopCallbacks = [] # LinkedList<AutoCloseable>
        self.__env = None # Environment
        self.__registry = None # Registry
        self.__serverOptions = None # ServerOptions
        self.__environmentOptions = None # EnvironmentOptions
        self.__locales = [] # List<Locale>
        self.__lateInit = None # boolean
        self.__name = None # String
        self.__version = None # String
    
    @staticmethod
    def runApp(self,
        args: List[str], 
        executionMode: ExecutionMode = ExecutionMode.DEFAULT, 
        applicationType=None,
        consumer=None, 
        provider=None):

        app = createApp(args, executionMode, provider) # Joopy
        server = app.start() # Server

        print("serving http on port 8000...")
        server.serve_forever()

    """ 
    Setup default environment, logging (logback or log4j2) and run application.
    @param args Application arguments. (@Nonnull String[])
    @param executionMode Application execution mode. (@Nonnull ExecutionMode)
    @param applicationType Application type. (@Nonnull Class<? extends Jooby>)
    @param provider Application provider. (@Nonnull Supplier<Jooby>)
    @return Application.
    """
    @staticmethod
    def createApp(self,
        args: List[str], 
        executionMode: ExecutionModer,
        applicationTyper=None,
        provider=None):
        return provider()
    
    """
    Application execution mode.

    @return Application execution mode.
    """
    def getExecutionMode(self):
        if self.__mode is None:
            return ExecutionMode.DEFAULT
        return self.__mode

    def getLog(self):
        pass
    def getEnvironment(self):
        if env == None:
            env = Environment.loadEnvironment(environmentOptions)
        return env
    def JoopyStart(self):
        servers = []
        if len(servers) == 0:
            raise Exception("Server not found.")
        if len(servers) > 1:
            names = [server.name for server in servers]
            self.getLog().warn("Multiple servers found {}. Using: {}".format(names, names[0]))
        server = servers[0]
        try:
            if serverOptions == None:
                configTemp = self.getEnvironment().getConfig()
                serverOptions = ServerOptions.From(configTemp) if configTemp != None else None
            if serverOptions != None:
                serverOptions.setServer( server.getClass().getSimpleName().lower() )
                server.setOptions(serverOptions)
            return server.start(self)
        except:
            errorType, errorMessage, errorTraceback = sys.exc_info()
            log = self.getLog()
            log.error("Application startup resulted in exception {}".format(errorType))
            try:
                server.stop()
            except:
                errorTypeServer, errorMessageServer, errorTracebackServer = sys.exc_info()
                log.info("Server stop resulted in exception {}".format(errorTypeServer))
            # rethrow
            if isinstance(errorType, StartupException):
                StartupException()
            else:
                raise Exception("Application startup resulted in exception")
            
    
    def start_with_server(self, server):
        self.__router.start(self)
        return self

    def ready(self, server: Base):
        print("Ready and Start")

        return self
