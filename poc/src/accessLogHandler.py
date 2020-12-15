import Route
import Context
import time
from typing import List, Callable
from multipledispatch import dispatch

class AccessLogHandler(Route.Decorator):
    __USER_AGENT = "User-Agent"
    __REFERER = "Referer"
    __FORMATTER = "dd/MMM/yyyy:HH:mm:ss Z"
    __DASH = "_"
    __SP = " "
    __BL = "["
    __BR = "]"
    __Q = "\""
    
    """
    function<context, string>
    """
    __USER_ON_DASH = lambda ctx: str(ctx.getUser()) if ctx.getUser() is not None else __DASH
    
    """
    Default buffer size
    """
    __MESSAGE_SIZE = 256
    
    @dispatch(object)
    def __init__(self, userId: func = None):
        """
        Creates a new {@link AccessLogHandler} and use the given function and userId provider. Please
        note, if the user isn't present this function is allowed to returns <code>-</code> (dash
        character).
   
        @param userId User ID provider.
        """
        if userId is None:
            self.__userId = lambda ctx: ctx
        else:
            self.__userId = userId
        self.date_formatter(self.__FORMATTER)
        """
        The logging system
        """
        self.__log = LoggerFactory.getLogger(getClass())
        self.__logRecord = self.__log.info()
        self.__requestHeaders = []
        self.__responseHeaders = []
        
    @dispatch()
    def __init__(self):
        """
        Creates a new {@link AccessLogHandler} without user identifier.
        """
        self.__init__(self.__USER_ON_DASH)
    
    def __apply_inner(self, _next, timestamp, ctx):
        ctx.onComplete(lambda context: self.__apply_inner_inner(timestamp, ctx, context))
        return _next.apply(ctx)
    
    def __apply_inner_inner(self, timestamp, ctx, context):
        sb = ""
        sb += ctx.getRemoteAddress()
        sb += (self.__SP + self.__DASH + self.__SP)
        sb += self.__userId.apply(ctx)
        sb += self.__SP
        sb += (self.__BL + self.__df.apply(timestamp) + self.__BR)
        sb += self.__SP
        sb += (self.__Q + ctx.getMethod())
        sb += self.__SP
        sb += ctx.getRequestPath()
        sb += ctx.queryString()
        sb += self.__SP
        sb += ctx.getProtocol()
        sb += (self.__Q + self.__SP)
        sb += ctx.getResponseCode().value()
        sb += self.__SP
        
        responseLength = ctx.getResponseLength()
        sb += responseLength if responseLength > 0 else self.__DASH
        
        now = int(round(time.time() * 1000))
        sb += self.__SP
        sb += (now - timestamp)
        
        self.__append_headers(sb, self.__requestHeaders, lambda h: ctx.header(h))
        self.__append_headers(sb, self.__responseHeaders, lambda h: ctx.getResponseHeader(h))
        self.__logRecord.accept(sb)
    
    def apply(self, _next: Route.Handler):
        timestamp = int(round(time.time() * 1000))
        return lambda ctx: self.__apply_inner(_next, timestamp, ctx)
    
    def __append_headers(self, buff: str, requestHeaders: List[str], headers: func):
        for header in requestHeaders:
            value = headers(header)
            if value is None:
                buff += (self.__SP + self.__Q + self.__DASH + self.__Q)
            else:
                buff += (self.__SP + self.__Q + value + self.__Q)
    
    def log(self, log):
        """
        Log an NCSA line to somewhere.
   
        <pre>{@code
            {
                use("*", new RequestLogger()
                    .log(System.out::println)
                );
            }
        }</pre>
   
        @param log Log callback.
        @return This instance.
        """
        if log is None:
            """
            new a Consumer<str>
            """
            pass
        else:
            self.__logRecord = log
        return self

    @dispatch(str)
    def date_formatter(self, formatter: str):
        """
        Override the default date formatter.
   
        @param formatter New formatter to use.
        @return This instance.
        """
        pass

    @dispatch(func)
    def date_formatter(self, formatter: func):
        if formatter is None:
            """
            new a formatter
            """
            pass
        else:
            self.__df = formatter
        return self

    def extended(self):
        """
        Append <code>Referer</code> and <code>User-Agent</code> entries to the NCSA line.
   
        @return This instance.
        """
        return self.request_header(self.__USER_AGENT, self.__REFERER)

    def request_header(self, names: List[str]):
        """
        Append request headers to the end of line.
   
        @param names Header names.
        @return This instance.
        """
        self.__requestHeaders = names.copy()
        return self
    
    def response_header(self, names: List[str]):
        """
        Append response headers to the end of line.
   
        @param names Header names.
        @return This instance.
        """
        self.__responseHeaders = names.copy()
        return self