from ..Route import Decorator
class HeadHandler(Decorator):
    '''
    * Add support for HTTP Head requests.
    *
    * Usage:
    * <pre>{@code
    *   decorator(new HeadHandler());
    *
    *   get("/some", ctx -> "...");
    *
    * }</pre>
    * @author edgar
    * @since 2.0.4
    '''
    def apply(self, next):
        #NOOP, but we need it for marking the route as HTTP HEAD
        return lambda ctx : next.apply(ctx)
    def setRoute(self, route):
        route.setHttpHead(True)