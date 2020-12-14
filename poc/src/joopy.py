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
from src.ExecutionMode import ExecutionMode
from src.mvcExtension import mvcExtension
from multipledispatch import dispatch

#routers = {}

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
        super(Joopy, self).__init__()    
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
        self.router = RouterImpl()
        #self.routes = routers
        #self.routes = None
    
    @staticmethod
    def runApp(args=None, 
        executionMode: ExecutionMode = ExecutionMode.DEFAULT, 
        applicationType=None,
        consumer=None, 
        provider=None):

        app = Joopy.createApp(args, executionMode, provider=provider) # Joopy
        server = app.start() # Server

        print("Start running App")
        try:
            while True:
                pass
        except:
            server.stop()
        finally:
            print("App terminated")
    '''
    @staticmethod
    def get(route):
        def decorator(func):
            global routers
            routers[route] = ("GET", func)
            return func
        return decorator
    '''
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
        args, 
        executionMode: ExecutionMode,
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
        if self.__env is None:
            self.__env = Environment.loadEnvironment(self.__environmentOptions)
        return self.__env

    @dispatch()
    def start(self):
        server = wsgi()
        try:
            return server.start(self)
        except exception as e:
            log = self.getLog()
            log.error("Application startup resulted in exception", e)
            try:
                server.stop()
            except exceptionSvr as esvr:
                log.error("Server stop resulted in exception", esvr)
            # rethrow
            #if isinstance(errorType, StartupException):
            #    StartupException()
            #else:
            #    raise Exception("Application startup resulted in exception")
            
    @dispatch(Base)
    def start(self, server:Base):
        #self.__router.start(self)
        print("Start server")
        self.router.start(self);

        return self

    def ready(self, server: Base):
        print("Ready and Start")

        return self

    def stop(self):
        print("Stop server")
        return self

    def route(self, method, pattern, handler):
        return self.router.route(method, pattern, handler)

    def mvc(self, router):
        provider = lambda: router
        return self.mvc_create(router.__class__, provider)

    def mvc_create(self, router=None, provider=None):
        module = mvcExtension()
        extension = module.create(provider)
        extension.install(self)
        return self

    def decorator(self, decorator):
        self.__router.decorator(decorator)
        return self

    def before(self, before):
        self.__router.before(before)
        return self

    def after(self, after):
        self.__router.after(after)
        return self

    def responseHandler(self, handler):
        self.__router.responseHandler(handler)
        return self
    
    def getErrorHandler(self):
        return self.__router.getErrorHandler() 
    
    def path(self, pattern, action):
        return self.__router.path(pattern, action)
    
    def routes(self, action):
        return self.__router.routes(action)

    def match(self)