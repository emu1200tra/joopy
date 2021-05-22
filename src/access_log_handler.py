import Route
from .context import Context
import time
from typing import List
from collections.abc import Callable
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

    def __USER_ON_DASH(ctx): return str(
        ctx.get_user()) if ctx.get_user() is not None else AccessLogHandler.__DASH
    """
    Default buffer size
    """
    __MESSAGE_SIZE = 256

    @dispatch(Callable)
    def __init__(self, user_id: Callable = None):
        """
        Creates a new {@link AccessLogHandler} and use the given function and userId provider. Please
        note, if the user isn't present this function is allowed to returns <code>-</code> (dash
        character).

        @param userId User ID provider.
        """
        if user_id is None:
            self.__user_id = lambda ctx: ctx
        else:
            self.__user_id = user_id
        self.date_formatter(self.__FORMATTER)
        """
        The logging system
        """
        self.__log = LoggerFactory.get_logger(get_class())
        self.__log_record = self.__log.info()
        self.__request_headers = []
        self.__response_headers = []

    @dispatch()
    def __init__(self):
        """
        Creates a new {@link AccessLogHandler} without user identifier.
        """
        self.__init__(self.__USER_ON_DASH)

    def __apply_inner(self, _next, timestamp, ctx):
        ctx.on_complete(lambda context: self.__apply_inner_inner(
            timestamp, ctx, context))
        return _next.apply(ctx)

    def __apply_inner_inner(self, timestamp, ctx, context):
        sb = ""
        sb += ctx.get_remote_address()
        sb += (self.__SP + self.__DASH + self.__SP)
        sb += self.__userId.apply(ctx)
        sb += self.__SP
        sb += (self.__BL + self.__df.apply(timestamp) + self.__BR)
        sb += self.__SP
        sb += (self.__Q + ctx.get_method())
        sb += self.__SP
        sb += ctx.get_request_path()
        sb += ctx.query_string()
        sb += self.__SP
        sb += ctx.get_protocol()
        sb += (self.__Q + self.__SP)
        sb += ctx.get_response_code().value()
        sb += self.__SP

        response_length = ctx.get_response_length()
        sb += response_length if response_length > 0 else self.__DASH

        now = int(round(time.time() * 1000))
        sb += self.__SP
        sb += (now - timestamp)

        self.__append_headers(sb, self.__request_headers,
                              lambda h: ctx.header(h))
        self.__append_headers(sb, self.__response_headers,
                              lambda h: ctx.get_response_header(h))
        self.__log_record.accept(sb)

    def apply(self, _next: Route.Handler):
        timestamp = int(round(time.time() * 1000))
        return lambda ctx: self.__apply_inner(_next, timestamp, ctx)

    def __append_headers(self, buff: str, request_headers: List[str], headers: Callable):
        for header in request_headers:
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
            self.__log_record = log
        return self

    @dispatch(str)
    def date_formatter(self, formatter: str):
        """
        Override the default date formatter.

        @param formatter New formatter to use.
        @return This instance.
        """
        pass

    @dispatch(Callable)
    def date_formatter(self, formatter: Callable):
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
        self.__request_headers = names.copy()
        return self

    def response_header(self, names: List[str]):
        """
        Append response headers to the end of line.

        @param names Header names.
        @return This instance.
        """
        self.__response_headers = names.copy()
        return self
