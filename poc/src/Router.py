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
        /**
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
        pass