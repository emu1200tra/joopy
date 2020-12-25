from multipledispatch import dispatch
from abc import ABCMeta, abstractmethod

from typing import List, Dict
from .context import Context
from .MessageEncoder import MessageEncoder
from .todo import *
from .exception.NotFoundException import NotFoundException


class Route:
    '''
    * Route contains information about the HTTP method, path pattern, which content types consumes and
    * produces, etc..
    *
    * Additionally, contains metadata about route return Java type, argument source (query, path, etc..) and
    * Java type.
    *
    * This class contains all the metadata associated to a route. It is like a {@link Class} object
    * for routes.
    *
    * @author edgar
    * @since 2.0.0
    '''
    class Aware(metaclass=ABCMeta):
        '''
        Allows a handler to listen for route metadata.
        @param route Route metadata.
        '''

        def set_route(self, route):
            pass

    class Handler(Aware):
        '''
        * Route handler here is where the application logic lives.
        *
        * @author edgar
        * @since 2.0.0
        '''

        def __init__(self, func):
            self.__func = func

        def apply(self, ctx: Context):
            '''
            Execute application code.

            @param ctx Web context.
            @return Route response.
            @throws Exception If something goes wrong.
            '''
            return self.__func(ctx)

        def then(self, next_):
            '''
            Chain this after decorator with next and produces a new decorator.

            @param next Next decorator. (After)
            @return A new handler. (Handler)
            '''
            def inner_then(ctx, next_):
                cause = None  # Throwable
                value = None  # Object
                try:
                    value = self.apply(ctx)
                except Exception as error:
                    cause = error
                result = None
                try:
                    if ctx.isResponseStarted():
                        result = Context.readOnly(ctx)
                        next_.apply(result, value, cause)
                    else:
                        result = value
                        next_.apply(ctx, value, cause)
                except Exception as error:
                    result = None
                    if cause is None:
                        cause = error
                    else:
                        cause.addSuppressed(error)

                if cause is None:
                    return result
                else:
                    if ctx.isResponseStarted():
                        return ctx
                    else:
                        raise SneakyThrows.propagate(cause)

            if isinstance(next_, Route.After):
                return lambda ctx: inner_then(ctx, next_)
            else:
                raise ValueError("The type of argument should be Route.After.")

    class Decorator(Aware):
        '''
        * Decorates a route handler by running logic before and after route handler. This pattern is
        * also known as Filter.
        *
        * <pre>{@code
        * {
        *   decorator(next -> ctx -> {
        *     long start = System.currentTimeMillis();
        *     Object result = next.apply(ctx);
        *     long end = System.currentTimeMillis();
        *     System.out.println("Took: " + (end - start));
        *     return result;
        *   });
        * }
        * }</pre>
        *
        * @author edgar
        * @since 2.0.0
        '''

        def __init__(self, func):
            self.__func = func

        def apply(self, next_):
            '''
            * Chain the decorator within next handler.
            *
            * @param next Next handler. (Handler)
            * @return A new handler. (Handler)
            '''
            return self.__func(next_)

        def then(self, next_):
            '''
            * Chain this decorator with another and produces a new decorator.
            *
            * @param next Next decorator. (Decorator)
            * @return A new decorator. (Decorator)
            '''
            '''
            * Chain this decorator with a handler and produces a new handler.
            *
            * @param next Next handler. (Handler)
            * @return A new handler. (Handler)
            '''
            if isinstance(next_, Route.Decorator):
                return lambda h: self.apply(next_.apply(h))
            elif isinstance(next_, Route.Handler):
                return lambda ctx: self.apply(next_).apply(ctx)
            else:
                raise ValueError(
                    "The type of argument should be Route.Decorator or Route.Handler.")

    class Before():
        '''
        * Decorates a handler and run logic before handler is executed.
        *
        * @author edgar
        * @since 2.0.0
        '''

        def __init__(self, func):
            self.__func = func

        def apply(self, ctx: Context):
            '''
            * Chain this filter with next one and produces a new before filter.
            *
            * @param next Next decorator.
            * @return A new decorator.
            '''
            return self.__func(ctx)

        def then(self, next_):
            '''
            * Chain this filter with next one and produces a new before filter.
            *
            * @param next Next decorator. (Before)
            * @return A new decorator. (Before)
            '''
            def then_before(ctx, next_):
                self.apply(ctx)
                if not ctx.isResponseStarted():
                    next.apply(ctx)
            '''
            * Chain this decorator with a handler and produces a new handler.
            *
            * @param next Next handler. (Handler)
            * @return A new handler. (Handler)
            '''
            def then_handler(ctx, next_):
                self.apply(ctx)
                if not ctx.isResponseStarted():
                    return next_.apply(ctx)
                return ctx

            if isinstance(next_, Route.Before):
                return lambda ctx: then_before(ctx, next_)
            elif isinstance(next_, Route.Handler):
                return lambda ctx: then_handler(ctx, next_)
            else:
                raise ValueError(
                    "The type of argument should be Route.Before or Route.Handler.")

    class After():
        '''
        * Execute application logic after a response has been generated by a route handler.
        *
        * For functional handler the value is accessible and you are able to modify the response:
        *
        * <pre>{@code
        * {
        *   after((ctx, result) -> {
        *     // Modify response
        *     ctx.setResponseHeader("foo", "bar");
        *     // do something with value:
        *     log.info("{} produces {}", ctx, result);
        *   });
        *
        *   get("/", ctx -> {
        *     return "Functional value";
        *   });
        * }
        * }</pre>
        *
        * For side-effect handler (direct use of send methods, outputstream, writer, etc.) you are not
        * allowed to modify the response or access to the value (value is always <code>null</code>):
        *
        * <pre>{@code
        * {
        *   after((ctx, result) -> {
        *     // Always null:
        *     assertNull(result);
        *
        *     // Response started is set to: true
        *     assertTrue(ctx.isResponseStarted());
        *   });
        *
        *   get("/", ctx -> {
        *     return ctx.send("Side effect");
        *   });
        * }
        * }</pre>
        *
        * @author edgar
        * @since 2.0.0
        '''

        def __init__(self, func):
            self.__func = func

        # result: Object, failure: Throwable
        def apply(self, ctx: Context, result: object, failure):
            '''
            * Execute application logic on a route response.
            *
            * @param ctx Web context.
            * @param result Response generated by route handler.
            * @param failure Uncaught exception generated by route handler.
            * @throws Exception If something goes wrong.
            '''
            return self.__func(ctx, result, failure)

        def then(self, next_):
            '''
            * Chain this filter with next one and produces a new after filter.
            *
            * @param next Next filter. (After)
            * @return A new filter. (After)
            '''
            def inner_then(ctx, result, failure):
                next_.apply(ctx, result, failure)
                self.apply(ctx, result, failure)

            if isinstance(next_, Route.After):
                return lambda ctx, result, failure: inner_then(ctx, result, failure)
            else:
                raise ValueError("The type of argument should be Route.After.")

    """
    Favicon handler as a silent 404 error.
    """
    def FAVICON(ctx): return ctx.send(
        StatusCode.NOT_FOUND)  # Handler # ctx -> ctx.send(StatusCode.NOT_FOUND);
    """
      public static final Handler NOT_FOUND = ctx -> ctx
      .sendError(new NotFoundException(ctx.getRequestPath()));
    """
    def NOT_FOUND(ctx): return ctx.send_error(
        NotFoundException(ctx.get_request_path()))
    __EMPTY_LIST = []  # final # List # Collections.emptyList()
    __EMPTY_MAP = {}  # final # Map # Collections.emptyMap()

    """
    Creates a new route.
    @param method HTTP method. (@Nonnull String)
    @param pattern Path pattern. (@Nonnull String)
    @param handler Route handler. (@Nonnull Handler)
    """

    def __init__(self, method, pattern, handler):
        self.__decoders = Route.__EMPTY_MAP  # Map<String, MessageDecoder>
        self.__pattern = pattern  # final # String
        self.__method = method.upper()  # final # String
        self.__pathKeys = Route.__EMPTY_LIST  # List<String>
        self.__before = None  # Before
        self.__decorator = None  # Decorator
        self.__handler = handler  # Handler
        self.__after = None  # After
        self.__pipeline = None  # Handler
        self.__encoder = None  # MessageEncoder
        self.__returnType = None  # Type
        self.__handle = handler  # object
        self.__produces = Route.__EMPTY_LIST  # List<MediaType>
        self.__consumes = Route.__EMPTY_LIST  # List<MediaType>
        # Map<String, Object> # new TreeMap<>(String.CASE_INSENSITIVE_ORDER)
        self.__attributes = {}
        self.__supportedMethod = None  # Set<String>
        self.__executorKey = None  # String
        self.__tags = Route.__EMPTY_LIST  # List<String>
        self.__summary = None  # String
        self.__description = None  # String

    def get_pattern(self) -> str:
        return self.__pattern

    def get_method(self) -> str:
        return self.__method

    def get_path_keys(self) -> List[str]:
        return self.__pathKeys

    def set_path_keys(self, pathKeys: List[str]):
        self.__pathKeys = pathKeys
        return self

    def get_handler(self) -> Handler:
        return self.__handler

    def get_handle(self) -> object:
        return self.__handle

    def get_pipeline(self) -> Handler:
        if self.__pipeline is None:
            self.__pipeline = self.computePipeline()
        return self.__pipeline

    def get_before(self) -> Before:
        return self.__before

    def set_before(self, before: Before):
        self.__before = before
        return self

    def get_after(self):
        return self.__after

    def set_after(self, after: After):
        self.__after = after
        return self

    def get_decorator(self):
        return self.__decorator

    def set_decorator(self, decorator: Decorator):
        self.__decorator = decorator
        return self

    def set_pipeline(self, pipeline: Handler):
        self.__pipeline = pipeline
        return self

    def get_encoder(self) -> MessageEncoder:
        return self.__encoder

    def set_encoder(self, encoder: MessageEncoder):
        self.__encoder = encoder
        return self

    def get_return_type(self):  # Type
        return self.__returnType

    def set_return_type(self, returnType):  # Type
        self.__returnType = type(returnType)
        return self

    def get_attributes(self) -> Dict[str, object]:
        return self.__attributes

    @dispatch(str)
    def attribute(self, name: str):  # -> <T> T
        return self.__attributes[name]  # (T)

    def set_attributes(self, attributes: Dict[str, object]):
        self.__attributes.update(attributes)
        return self

    @dispatch(str, object)
    def attribute(self, name: str, value: object):
        if self.__attributes == Route.__EMPTY_MAP:
            # new TreeMap<>(String.CASE_INSENSITIVE_ORDER)
            self.__attributes = {}

        self.__attributes[name] = value

        return self

    def get_decoders(self) -> Dict[str, MessageDecoder]:
        return self.__decoders

    def set_decoders(self, decoders: Dict[str, MessageDecoder]):
        self.__decoders = decoders
        return self

    def set_executor_key(self, key: str):
        self.__executorKey = key
        return self

    def get_executor_key(self) -> str:
        return self.__executorKey

    def set_return_type(self, returntype: object):
        self.__returnType = returntype
        return self

    def get_return_type(self) -> object:
        return self.__returnType

    def get_produces(self) -> List[MediaType]:
        return self.__produces

    def produces(self, *args):
        produces = []
        for produce in args:
            produces.append(produce)

        return self.set_produces(produces)

    # Collection<MediaType> produces
    def set_produces(self, produces: List[MediaType]):
        if len(produces) > 0:
            if self.__produces == Route.__EMPTY_LIST:
                # new arrayList in java(?)
                pass

            for produce in produces:
                self.__produces.append(produce)

        return self

    def get_consumes(self) -> List[MediaType]:
        return self.__consumes

    def consumes(self, *args):
        consumes = []
        for consume in args:
            consumes.append(consume)

        return self.set_consumes(consumes)

    # Collection<MediaType> consumes
    def set_consumes(self, consumes: List[MediaType]):
        # TODO
        if len(consumes) > 0:
            if self.__consumes == Route.__EMPTY_LIST:
                # new arrayList in java(?)
                pass

            for consume in consumes:
                self.__consumes.append(consume)

        return self

    def computePipeline(self) -> Handler:
        pipeline = None  # Route.Handler
        if self.__decorator is None:
            pipeline = self.__handler
        else:
            pipeline = self.__decorator.then(self.__handler)

        if self.__before is not None:
            pipeline = self.__before.then(pipeline)

        if self.__after is not None:
            pipeline = pipeline.then(self.__after)

        return pipeline

    @staticmethod
    def accept(ctx):
        produceTypes = ctx.get_route().get_produces()
        contentType = ctx.accept(produceTypes)  # MediaType
        if contentType is None:
            raise Exception('NotAcceptableException')

        ctx.set_default_response_type(contentType)

    ACCEPT = Before(lambda ctx: Route.accept(ctx))

    @staticmethod
    def support_media_type(ctx):
        contentType = ctx.get_request_type  # MediaType
        if contentType is None:
            raise Exception('UnsupportedMediaType')

        ok = False
        for media_type in ctx.get_route().get_consumes():
            if contentType.matches(media_type):
                ok = True

        if ok == False:
            raise Exception('UnsupportedMediaType' + contentType.getValue())

    SUPPORT_MEDIA_TYPE = Before(lambda ctx: Route.support_media_type(ctx))
