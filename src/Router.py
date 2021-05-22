import os
from .Registry import Registry
from .Route import Route
from .todo import *
from abc import abstractmethod
import copy
from multipledispatch import dispatch
import sys

class Router(Registry):
    """
    Find route result.
    """
    class Match():
        @abstractmethod
        def matches(self):
            """
            True for matching route.
            @return True for matching route.
            """
            pass
        @abstractmethod
        def route(self):
            """
            Matched route.
            @return Matched route.
            """
            pass
        @abstractmethod
        def execute(self, context):
            pass
        @abstractmethod
        def pathMap(self):
            """
            Path pattern variables.
            @return Path pattern variables.
            """
            pass

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"

    METHODS = (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS, TRACE)
    WS = "WS"
    SSE = "SSE"

    @abstractmethod
    def getConfig(self):
        """
        Application configuration.
        @return Application configuration.
        """
        pass
    @abstractmethod
    def getEnvironment(self):
        """
        Application environment.
        @return Application environment.
        """
        pass
    @abstractmethod
    def getLocales(self):
        """
        Returns the supported locales.
        @returns the supported locales.
        """
        pass
    @abstractmethod
    def getAttributes(self):
        """
        Mutable map of application attributes.
        @return Mutable map of application attributes.
        """
        pass
    def attribute(self, key):
        """
        Get an attribute by his key. This is just an utility method around {@link #getAttributes()}.
        @param key Attribute key.
        @param <T> Attribute type.
        @return Attribute value.
        """
        attribute = self.getAttributes()[key]
        if attribute == None:
            MissingValueException(key)
        else:
            return attribute

    def RouterAttribute(self, key, value):
        """
        Set an application attribute.
        @param key Attribute key.
        @param value Attribute value.
        @return This router.
        """
        self.getAttributes()[key] = value
        return self

    @abstractmethod
    def getServices(self):
        """
        Application service registry. Services are accessible via this registry or
        {@link Jooby#require(Class)} calls.
        This method returns a mutable registry. You are free to modify/alter the registry.
        @return Service registry.
        """
        pass
    @abstractmethod
    def setContextPath(self, contextPath):
        """
        Set application context path. Context path is the base path for all routes. Default is:
        <code>/</code>.
        @param contextPath Context path.
        @return This router.
        """
        pass
    @abstractmethod
    def getContextPath(self):
        """
        Get application context path (a.k.a as base path).
        @return Application context path (a.k.a as base path).
        """
        pass
    @abstractmethod
    def isTrustProxy(self):
        """
        When true handles X-Forwarded-* headers by updating the values on the current context to
        match what was sent in the header(s).

        This should only be installed behind a reverse proxy that has been configured to send the
        <code>X-Forwarded-*</code> header, otherwise a remote user can spoof their address by
        sending a header with bogus values.

        The headers that are read/set are:
        <ul>
            <li>X-Forwarded-For: Set/update the remote address {@link Context#setRemoteAddress(String)}.</li>
            <li>X-Forwarded-Proto: Set/update request scheme {@link Context#setScheme(String)}.</li>
            <li>X-Forwarded-Host: Set/update the request host {@link Context#setHost(String)}.</li>
            <li>X-Forwarded-Port: Set/update the request port {@link Context#setPort(int)}.</li>
        </ul>

        @return True when enabled. Default is false.
        """
        pass
    @abstractmethod
    def setTrustProxy(self, trustProxy):
        """
        When true handles X-Forwarded-* headers by updating the values on the current context to
        match what was sent in the header(s).

        This should only be installed behind a reverse proxy that has been configured to send the
        <code>X-Forwarded-*</code> header, otherwise a remote user can spoof their address by
        sending a header with bogus values.

        The headers that are read/set are:
        <ul>
            <li>X-Forwarded-For: Set/update the remote address {@link Context#setRemoteAddress(String)}.</li>
            <li>X-Forwarded-Proto: Set/update request scheme {@link Context#setScheme(String)}.</li>
            <li>X-Forwarded-Host: Set/update the request host {@link Context#setHost(String)}.</li>
            <li>X-Forwarded-Port: Set/update the request port {@link Context#setPort(int)}.</li>
        </ul>

        @param trustProxy True to enabled.
        @return This router.
        """
        pass
    @abstractmethod
    def setHiddenMethod(self, parameterName):
        """
        Provides a way to override the current HTTP method. Request must be:

        - POST Form/multipart request

        For alternative strategy use the {@link #setHiddenMethod(Function)} method.

        @param parameterName Form field name.
        @return This router.
        """
        pass
    @abstractmethod
    def setHiddenMethod(self, provider):
        """
        Provides a way to override the current HTTP method using lookup strategy.

        @param provider Lookup strategy.
        @return This router.
        """
        pass
    @abstractmethod
    def setCurrentUser(self, provider):
        """
        Provides a way to set the current user from a {@link Context}. Current user can be retrieve it
        using {@link Context#getUser()}.

        @param provider User provider/factory.
        @return This router.
        """
        pass
    @abstractmethod
    def setContextAsService(self, contextAsService):
        """
        If enabled, allows to retrieve the {@link Context} object associated with the current
        request via the service registry while the request is being processed.

        @param contextAsService whether to enable or disable this feature
        @return This router.
        """
        pass

    @abstractmethod
    def domainRouter(self, domain, subrouter):
        """
        Enabled routes for specific domain. Domain matching is done using the <code>host</code> header.

        <pre>{@code
            {
                domain("foo.com", new FooApp());
                domain("bar.com", new BarApp());
            }
        }</pre>

        NOTE: if you run behind a reverse proxy you might to enabled {@link #setTrustProxy(boolean)}.

        NOTE: ONLY routes are imported. Services, callback, etc.. are ignored.

        @param domain Predicate
        @param subrouter Subrouter.
        @return This router.
        """
        pass

    @abstractmethod
    def domainRouterSet(self, domain, body):
        """
        Enabled routes for specific domain. Domain matching is done using the <code>host</code> header.

        <pre>{@code
            {
                domain("foo.com", () -> {
                    get("/", ctx -> "foo");
                });
                domain("bar.com", () -> {
                    get("/", ctx -> "bar");
                });
            }
        }</pre>

        NOTE: if you run behind a reverse proxy you might to enabled {@link #setTrustProxy(boolean)}.

        @param domain Predicate
        @param body Route action.
        @return This router.
        """
        pass

    def useRouter(self, predicate, router):
        """
        Import routes from given router. Predicate works like a filter and only when predicate pass
        the routes match against the current request.

        Example of domain predicate filter:

        <pre>{@code
            {
                use(ctx -> ctx.getHost().equals("foo.com"), new FooApp());
                use(ctx -> ctx.getHost().equals("bar.com"), new BarApp());
            }
        }</pre>

        Imported routes are matched only when predicate pass.

        NOTE: if you run behind a reverse proxy you might to enabled {@link #setTrustProxy(boolean)}.

        NOTE: ONLY routes are imported. Services, callback, etc.. are ignored.

        @param predicate Context predicate.
        @param router Router to import.
        @return This router.
        @deprecated Use {@link #mount(Predicate, Router)}
        """
        return self.mountRouter(predicate, router)

    @abstractmethod
    def mountRouter(self, predicate, router):
        """
        Import routes from given router. Predicate works like a filter and only when predicate pass
        the routes match against the current request.

        Example of domain predicate filter:

        <pre>{@code
            {
                use(ctx -> ctx.getHost().equals("foo.com"), new FooApp());
                use(ctx -> ctx.getHost().equals("bar.com"), new BarApp());
            }
        }</pre>

        Imported routes are matched only when predicate pass.

        NOTE: if you run behind a reverse proxy you might to enabled {@link #setTrustProxy(boolean)}.

        NOTE: ONLY routes are imported. Services, callback, etc.. are ignored.

        @param predicate Context predicate.
        @param router Router to import.
        @return This router.
        """
        pass

    def userRouterSet(self, predicate, body):
        """
        Import routes from given action. Predicate works like a filter and only when predicate pass
        the routes match against the current request.

        Example of domain predicate filter:

        <pre>{@code
            {
                use(ctx -> ctx.getHost().equals("foo.com"), () -> {
                    get("/", ctx -> "foo");
                });
                use(ctx -> ctx.getHost().equals("bar.com"), () -> {
                    get("/", ctx -> "bar");
                });
            }
        }</pre>

        NOTE: if you run behind a reverse proxy you might to enabled {@link #setTrustProxy(boolean)}.

        @param predicate Context predicate.
        @param body Route action.
        @return This router.
        @deprecated Use {@link #mount(Predicate, Runnable)}
        """
        return self.mountRouterSet(predicate, body)

    @abstractmethod
    def mountRouterSet(predicate, body):
        """
        Import routes from given action. Predicate works like a filter and only when predicate pass
        the routes match against the current request.

        Example of domain predicate filter:

        <pre>{@code
            {
                mount(ctx -> ctx.getHost().equals("foo.com"), () -> {
                    get("/", ctx -> "foo");
                });
                mount(ctx -> ctx.getHost().equals("bar.com"), () -> {
                    get("/", ctx -> "bar");
                });
            }
        }</pre>

        NOTE: if you run behind a reverse proxy you might to enabled {@link #setTrustProxy(boolean)}.

        NOTE: ONLY routes are imported. Services, callback, etc.. are ignored.

        @param predicate Context predicate.
        @param body Route action.
        @return This router.
        """
        pass

    def useRouterPath(self, path, router):
        """
        Import all routes from the given router and prefix them with the given path.

        NOTE: ONLY routes are imported. Services, callback, etc.. are ignored.

        @param path Prefix path.
        @param router Router to import.
        @return This router.
        @deprecated Use {@link #mount(String, Router)}
        """
        return self.mount(path, router)

    @abstractmethod
    def mountRouterPath(self, path, router):
        """
        Import all routes from the given router and prefix them with the given path.

        NOTE: ONLY routes are imported. Services, callback, etc.. are ignored.

        @param path Prefix path.
        @param router Router to import.
        @return This router.
        """
        pass

    def useRouterOnly(self, router):
        """
        Import all routes from the given router.

        NOTE: ONLY routes are imported. Services, callback, etc.. are ignored.

        @param router Router to import.
        @return This router.
        @deprecated Use {@link #mount(Router)}
        """
        return self.mountRouterOnly(router)

    @abstractmethod
    def mountRouterOnly(self, router):
        """
        Import all routes from the given router.

        NOTE: ONLY routes are imported. Services, callback, etc.. are ignored.

        @param router Router to import.
        @return This router.
        """
        pass

    @abstractmethod
    def mvcRouter(self, router):
        """
        Import all route method from the given controller class. At runtime the controller instance
        is resolved by calling {@link Jooby#require(Class)}.

        @param router Controller class.
        @return This router.
        """
        pass

    @abstractmethod
    def mvcT(self, router, provider):
        """
        Import all route method from the given controller class.

        @param router Controller class.
        @param provider Controller provider.
        @param <T> Controller type.
        @return This router.
        """
        pass

    @abstractmethod
    def mvcObj(self, router):
        """
        Import all route methods from given controller instance.

        @param router Controller instance.
        @return This routes.
        """
        pass

    @abstractmethod
    def ws(self, pattern, handler):
        """
        Add a websocket handler.

        @param pattern WebSocket path pattern.
        @param handler WebSocket handler.
        @return A new route.
        """
        pass

    @abstractmethod
    def sse(self, pattern, handler):
        """
        Add a server-sent event handler.

        @param pattern Path pattern.
        @param handler Handler.
        @return A new route.
        """
        pass

    @abstractmethod
    def getRoutes(self):
        """
        Returns all routes.

        @return All routes.
        """
        pass

    @abstractmethod
    def encoderRouter(self, encoder):
        """
        Register a route response encoder.

        @param encoder MessageEncoder instance.
        @return This router.
        """
        pass

    @abstractmethod
    def encoderRouterContent(self, contentType, encoder):
        """
        Register a route response encoder.

        @param contentType Accept header should matches the content-type.
        @param encoder MessageEncoder instance.
        @return This router.
        """
        pass

    @abstractmethod
    def getTmpdir(self):
        """
        Application temporary directory. This method initialize the {@link Environment} when isn't
        set manually.

        @return Application temporary directory.
        """
        pass

    @abstractmethod
    def decoder(self, contentType, decoder):
        """
        Register a decoder for the given content type.

        @param contentType Content type to match.
        @param decoder MessageDecoder.
        @return This router.
        """
        pass

    @abstractmethod
    def getWorker(self):
        """
        Returns the worker thread pool. This thread pool is used to run application blocking code.

        @return Worker thread pool.
        """
        pass

    @abstractmethod
    def setWorker(self, worker):
        """
        Set a worker thread pool. This thread pool is used to run application blocking code.

        @param worker Worker thread pool.
        @return This router.
        """
        pass

    @abstractmethod
    def setDefaultWorker(self, worker):
        """
        Set the default worker thread pool. Via this method the underlying web server set/suggests the
        worker thread pool that should be used it.

        A call to {@link #getWorker()} returns the default thread pool, unless you explicitly set one.

        @param worker Default worker thread pool.
        @return This router.
        """
        pass

    @abstractmethod
    def decorator(self, decorator: Route.Decorator):
        """
        Add a route decorator to the route pipeline.

        @param decorator Decorator.
        @return This router.
        """
        pass

    @abstractmethod
    def before(self, before: Route.Decorator):
        """
        Add a before route decorator to the route pipeline.

        @param before Before decorator.
        @return This router.
        """
        pass

    @abstractmethod
    def after(self, after: Route.Decorator):
        """
        Add an after route decorator to the route pipeline.

        @param after After decorator.
        @return This router.
        """
        pass

    @abstractmethod
    def _dispatch(self, body):
        """
        Dispatch route pipeline to the {@link #getWorker()} worker thread pool. After dispatch
        application code is allowed to do blocking calls.

        @param body Dispatch body.
        @return This router.
        """
        pass

    @abstractmethod
    def dispatchExecutor(self, executor, body):
        """
        Dispatch route pipeline to the given executor. After dispatch application code is allowed to
        do blocking calls.

        @param executor Executor. {@link java.util.concurrent.ExecutorService} instances automatically
        shutdown at application exit.
        @param body Dispatch body.
        @return This router.
        """
        pass

    @abstractmethod
    def routes(self, body):
        """
        Group one or more routes. Useful for applying cross cutting concerns to the enclosed routes.

        @param body Route body.
        @return All routes created.
        """
        pass

    @abstractmethod
    def path(self, pattern, body):
        """
        Group one or more routes under a common path prefix. Useful for applying cross cutting
        concerns to the enclosed routes.

        @param pattern Path pattern.
        @param body Route body.
        @return All routes created.
        """
        pass

    @abstractmethod
    def route(self, method, pattern, handler):
        """
        Add a route.

        @param method HTTP method.
        @param pattern Path pattern.
        @param handler Application code.
        @return A route.
        """
        pass

    @dispatch(str, object)
    def get(self, pattern, handler):
        """
        Add a HTTP GET handler.

        @param pattern Path pattern.
        @param handler Application code.
        @return A route.
        """
        return self.route(Router.GET, pattern, handler)

    @dispatch(str, object)
    def post(self, pattern, handler):
        """
        Add a HTTP POST handler.

        @param pattern Path pattern.
        @param handler Application code.
        @return A route.
        """
        return self.route(Router.POST, pattern, handler)

    @dispatch(str, object)
    def put(self, pattern, handler):
        """
        Add a HTTP PUT handler.

        @param pattern Path pattern.
        @param handler Application code.
        @return A route.
        """
        return self.route(Router.PUT, pattern, handler)

    @dispatch(str, object)
    def delete(self, pattern, handler):
        """
        Add a HTTP DELETE handler.

        @param pattern Path pattern.
        @param handler Application code.
        @return A route.
        """
        return self.route(Router.DELETE, pattern, handler)

    @dispatch(str)
    def get(self, pattern):
        def decorator(handler):
            self.route(Router.GET, pattern, handler)
            return handler
        return decorator

    @dispatch(str)
    def post(self, pattern):
        def decorator(handler):
            self.route(Router.POST, pattern, handler)
            return handler
        return decorator

    @dispatch(str)
    def put(self, pattern):
        def decorator(handler):
            self.route(Router.PUT, pattern, handler)
            return handler
        return decorator

    @dispatch(str)
    def delete(self, pattern):
        def decorator(handler):
            self.route(Router.DELETE, pattern, handler)
            return handler
        return decorator

    def patch(self, pattern, handler):
        """
        Add a HTTP PATCH handler.

        @param pattern Path pattern.
        @param handler Application code.
        @return A route.
        """
        return self.route(PATCH, pattern, handler)

    def head(self, pattern, handler):
        """
        Add a HTTP HEAD handler.

        @param pattern Path pattern.
        @param handler Application code.
        @return A route.
        """
        return self.route(HEAD, pattern, handler)

    def options(self, pattern, handler):
        """
        Add a HTTP OPTIONS handler.

        @param pattern Path pattern.
        @param handler Application code.
        @return A route.
        """
        return self.route(OPTIONS, pattern, handler)

    def trace(self, pattern, handler):
        """
        Add a HTTP TRACE handler.

        @param pattern Path pattern.
        @param handler Application code.
        @return A route.
        """
        return self.route(TRACE, pattern, handler)

    def assets(self, pattern, handler):
        """
        Add a static resource handler.

        @param pattern Path pattern.
        @param handler Asset handler.
        @return A route.
        """
        return self.route(GET, pattern, handler)

    def assetsPath(self, pattern, source):
        """
        Add a static resource handler. Static resources are resolved from file system.

        @param pattern Path pattern.
        @param source File system directory.
        @return A route.
        """
        return self.assets(pattern, AssetSource.create(source))

    def assetsString(self, pattern, source):
        """
        Add a static resource handler. Static resources are resolved from:

        - file-system if the source folder exists in the current user directory
        - or fallback to classpath when file-system folder doesn't exist.

        NOTE: This method choose file-system or classpath, it doesn't merge them.

        @param pattern Path pattern.
        @param source File-System folder when exists, or fallback to a classpath folder.
        @return A route.
        """
        source_list = source.split('/')
        source_list = [s for s in source_list if len(s) > 0]
        path = os.path.join(os.getcwd(), '/'.join(source_list))
        if os.path.exists(path):
            return self.assets(pattern, path)
        return self.assets(pattern, AssetSource.create(getClass().getClassLoader(), source))

    def AssetsSource(self, pattern, source):
        """
        Add a static resource handler.

        @param pattern Path pattern.
        @param source Asset sources.
        @return A route.
        """
        return self.assets(pattern, AssetHandler(source))

    @abstractmethod
    def match(self, ctx):
        """
        Find a matching route using the given context.

        If no match exists this method returns a route with a <code>404</code> handler.
        See {@link Route#NOT_FOUND}.

        @param ctx Web Context.
        @return A route match result.
        """
        pass

    @abstractmethod
    def matchResult(self, method, path):
        """
        Find a matching route using the given context.

        If no match exists this method returns a route with a <code>404</code> handler.
        See {@link Route#NOT_FOUND}.

        @param method Method to match.
        @param path Path to match.
        @return A route match result.
        """
        pass

    @dispatch(object, StatusCode)
    @abstractmethod
    def error_code(self, obj, statusCode):
        """
        Map an exception type to a status code.

        @param type Exception type.
        @param statusCode Status code.
        @return This router.
        """
        pass

    @dispatch(Exception)
    @abstractmethod
    def error_code(self, cause):
        pass

    @abstractmethod
    def errorCodeCause(self, cause):
        """
        Computes the status code for the given exception.

        @param cause Exception.
        @return Status code.
        """
        pass

    @abstractmethod
    def error(self, handler):
        """
        Add a custom error handler.

        @param handler Error handler.
        @return This router.
        """
        pass

    def errorStatusCode(self, statusCode, handler):
        """
        Add a custom error handler that matches the given status code.

        @param statusCode Status code.
        @param handler Error handler.
        @return This router.
        """
        return self.errorStatusCode(statusCode.equals(), handler)

    def errorType(self, Dtype, handler):
        """
        Add a custom error handler that matches the given exception type.

        @param type Exception type.
        @param handler Error handler.
        @return This router.
        """
        return self.error( lambda ctx, x, statusCode: handler.apply(ctx, x, statusCode) \
            if isinstance(x, Dtype) or isinstance(x.getCause(), Dtype) else None)

    def errorPredicate(self, predicate, handler):
        """
        Add a custom error handler that matches the given predicate.

        @param predicate Status code filter.
        @param handler Error handler.
        @return This router.
        """
        return self.error( lambda ctx, x, statusCode: handler.apply(ctx, x, statusCode) \
            if predicate.test(statusCode) else None)

    @abstractmethod
    def getErrorHandler(self):
        """
        Get the error handler.

        @return An error handler.
        """
        pass

    @abstractmethod
    def getLog(self):
        """
        Application logger.

        @return Application logger.
        """
        pass

    @abstractmethod
    def responseHandler(self, factory):
        """
        Add a response handler factory.

        @param factory Response handler factory.
        @return This router.
        """
        pass

    @abstractmethod
    def getRouterOptions(self):
        """
        Router options.

        @return Router options.
        """
        pass

    @abstractmethod
    def setRouterOptions(self, options):
        """
        Set router options.

        @param options router options.
        @return This router.
        """
        pass

    @abstractmethod
    def getSessionStore(self):
        """
        Session store. Default use a cookie ID with a memory storage.

        See {@link SessionStore#memory()}.

        @return Session store.
        """
        pass

    @abstractmethod
    def setSessionStore(self, store):
        """
        Set session store.

        @param store Session store.
        @return This router.
        """
        pass

    def executor(self, name):
        """
        Get an executor from application registry.

        @param name Executor name.
        @return Executor.
        """
        return Registry.require(Executor, name)

    @abstractmethod
    def executorRouter(self, name, executor):
        """
        Put an executor into the application registry.

        @param name Executor's name.
        @param executor Executor.
        @return This router.
        """
        pass

    @abstractmethod
    def setFlashCookieByName(self, name):
        """
        Set flash cookie name.

        @param name Flash cookie name.
        @return This router.
        @deprecated Use {@link #setFlashCookie(Cookie)} instead.
        """
        pass

    @abstractmethod
    def getFlashCookie(self):
        """
        Template for the flash cookie. Default name is: <code>jooby.flash</code>.

        @return Template for the flash cookie.
        """
        pass

    @abstractmethod
    def setFlashCookie(self, flashCookie):
        """
        Sets a cookie used as a template to generate the flash cookie, allowing
        to customize the cookie name and other cookie parameters.

        @param flashCookie The cookie template.
        @return This router.
        """
        pass

    @abstractmethod
    def converterValue(self, converter):
        """
        Add a custom string value converter.

        @param converter Custom value converter.
        @return This router.
        """
        pass

    @abstractmethod
    def converterBean(self, converter):
        """
        Add a custom bean value converter.

        @param converter Custom value converter.
        @return This router.
        """
        pass

    @abstractmethod
    def getConverters(self):
        """
        Get all simple/string value converters.

        @return All simple/string value converters.
        """
        pass

    @abstractmethod
    def getBeanConverters(self):
        """
        Get all complex/bean value converters.

        @return All complex/bean value converters.
        """
        pass

    @abstractmethod
    def getServerOptions(self):
        """
        Available server options.

        @return Server options.
        """
        pass

    @staticmethod
    def leadingSlash(path):
        """
        Ensure path start with a <code>/</code>(leading slash).

        @param path Path to process.
        @return Path with leading slash.
        """
        if path == None or len(path) == 0 or path == '/':
            return '/'
        if path[0] == '/':
            return path
        else:
            return '/' + path

    @staticmethod
    def noTrailingSlash(path):
        """
        Strip trailing slashes.

        @param path Path to process.
        @return Path without trailing slashes.
        """
        return path.split('/')[0]


    @staticmethod
    def normalizePath(path):
        """
        Normalize a path by removing consecutive <code>/</code>(slashes).

        @param path Path to process.
        @return Safe path pattern.
        """
        if path == None or len(path) == 0 or path == '/':
            return '/'
        buff = '/' + path if path[0] != '/' else path
        return buff.replace('//', '/')

    @staticmethod
    def pathKeyConsumer(pattern, consumer):
        """
        Extract path keys from given path pattern. A path key (a.k.a path variable) looks like:

        <pre>/product/{id}</pre>

        @param pattern Path pattern.
        @param consumer Listen for key and regex variables found.
        @return Path keys.
        """
        result = []
        start = -1;
        end = sys.maxsize
        len_ = len(pattern)
        curly = 0
        for i in range(len_):
            ch = pattern[i]
            if ch == '{':
                if curly == 0:
                    start = i + 1
                    end = sys.maxsize
                curly += 1
            elif ch == ':':
                end = i
            elif ch == '}':
                curly -= 1;
                if curly == 0:
                    id = pattern[start: min(i, end)]
                    if end == sys.maxsize:
                        value = None
                    else:
                        value = pattern.substring(end + 1, i)
                    consumer(id, value)
                    result.add(id)
                    start = -1
                    end = sys.maxsize
            elif ch == '*':
                if i == len_ - 1:
                    id = "*"
                else:
                    id = pattern[i + 1:]
                result.add(id)
                consumer(id, "\\.*")
                i = len_

        if len(result) == 0:
            return []
        elif len(result) == 1:
            return [result[0]]
        else:
            return result

    @staticmethod
    def pathKeys(pattern):
        """
        Extract path keys from given path pattern. A path key (a.k.a path variable) looks like:

        <pre>/product/{id}</pre>

        @param pattern Path pattern.
        @return Path keys.
        """
        return Router.pathKeyConsumer(pattern, lambda k, v: ())

    @staticmethod
    def expandOptionalVariables(pattern):
        """
        Look for optional path parameter and expand the given pattern into multiple pattern.

        <pre>
            /path =&gt; [/path]
            /{id} =&gt; [/{id}]
            /path/{id} =&gt; [/path/{id}]

            /{id}? =&gt; [/, /{id}]
            /path/{id}? =&gt; [/path, /path/{id}]
            /path/{id}/{start}?/{end}? =&gt; [/path/{id}, /path/{id}/{start}, /path/{id}/{start}/{end}]
            /path/{id}?/suffix =&gt; [/path, /path/{id}, /path/suffix]
        </pre>

        @param pattern Pattern.
        @return One or more patterns.
        """
        if pattern is None or pattern == "/":
            return ["/"]
        len_ = len(pattern)
        key = 0
        paths = {} # {int, str}
        def path_appender(index, segment):
            for i in range(index, index-1):
                paths[i] += segment

            if index not in paths:
                value = ""
                if index > 0:
                    previous = paths[index-1]
                    if previous != "/":
                        value.append(previous)
                paths[index] = value
            
            paths[index] += segment
            return paths[index]

        segment = ""
        is_last_optional = False
        i = 0
        while i < len_:
            ch = pattern[i]
            if ch == "/":
                if len(segment) > 0:
                    path_appender(key, segment)
                    segment = ""
                segment += ch
                i += 1
            elif ch == "{":
                segment += ch
                curly = 1
                j = i + 1
                while j < len_:
                    next_ = pattern[j]
                    j += 1
                    segment += next_
                    if next_ == "{":
                        curly += 1
                    elif next_ == "}":
                        curly -= 1
                        if curly == 0:
                            break
                if j < len_ and pattern[j] == "?":
                    j += 1
                    is_last_optional = True
                    if paths is None:
                        paths[0] = "/"
                    key += 1
                    path_appender(key, segment)
                else:
                    is_last_optional = False
                    path_appender(key, segment)
                segment = ""
                i = j
            else:
                segment += ch
                i += 1
        if paths is None:
            return [pattern]
        if len(segment) > 0:
            path_appender(key, segment)
            if is_last_optional:
                key += 1
                paths[key] = segment
        return list(paths.values())
        
    @staticmethod
    def reverseWithMap(pattern, keys):
        """
        Recreate a path pattern using the given variables.

        @param pattern Path pattern.
        @param keys Path keys.
        @return Path.
        """
        return ""

    @staticmethod
    def reverse(pattern, values):
        """
        Recreate a path pattern using the given variables. Variable replacement is done using the
        current index.

        @param pattern Path pattern.
        @param values Path keys.
        @return Path.
        """
        keys = {}
        for idx, v in enumerate(values):
            keys[ str(idx) ] = v
        return Router.reverseWithMap(pattern, keys)

