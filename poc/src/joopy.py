import abc
import sys
from src import wsgi
from src import Router
from src import Registry
from src import RouterImpl
from src.Server import Base
from src.wsgi import wsgi
from src.LoggerFactory import LoggerFactory
from src.Logger import Logger

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

        print("Start running App")
        try:
            while True:
                pass
        except:
            server.stop()
        finally:
            print("App terminated")

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
        logFactory = LoggerFactory()
        log = logFactory.getLogger()
        return log

    def getEnvironment(self):
        if env == None:
            env = Environment.loadEnvironment(environmentOptions)
        return env
    def start(self):
        server = wsgi()
        try:
            return server.start(self)
        except:
            errorType, errorMessage, errorTraceback = sys.exc_info()
            log = self.getLog()
            log.error("Application startup resulted in exception {}".format(errorType), errorMessage)
            try:
                server.stop()
            except:
                errorTypeServer, errorMessageServer, errorTracebackServer = sys.exc_info()
                log.error("Server stop resulted in exception {}".format(errorTypeServer), errorMessageServer)
            # rethrow
            #if isinstance(errorType, StartupException):
            #    StartupException()
            #else:
            #    raise Exception("Application startup resulted in exception")
            
    
    def start_with_server(self, server):
        self.__router.start(self)
        return self

    def ready(self, server: Base):
        print("Ready and Start")

        return self

    def stop(self):
        print("Stop server")
        return self