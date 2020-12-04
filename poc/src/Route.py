class Route:
    def __init__(self):
        self.__executorKey = None # String
        self.__returnType = None; # Type

    class Aware:
        def setRoute(self, route:Route):
            pass
    class Decorator(Aware):
        def apply(self, next:Handler) -> Handler:
            pass
        def then_Decorator(self, next:Decorator) -> Decorator:
            return lambda h : apply(next.apply(h))
        def then_Handler(self, next:Handler) -> Handler:
            return lambda ctx : apply(next).apply(ctx)
    class Before:
        def inner_then(self, ctx, next):
            apply(ctx)
            if not ctx.isResponseStarted():
                return next.apply(ctx)
            return ctx
        def apply(self, ctx:Context):
            raise Exception
        def then(self, next):
            return lambda ctx : inner_then(ctx, next)
    
    def setExecutorKey(self, key: str):
        self.__executorKey = key
        return self

    def getExecutorKey(self) -> str:
        return self.__executorKey

    def setReturnType(self, returntype: object):
        self.__returnType = returntype
        return self

    def getReturnType(self) -> object:
        return self.__returnType