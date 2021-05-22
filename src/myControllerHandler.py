from .Route import Route
from .context import Context

class myControllerHandler(Route.Handler):
    def __init__(self, provider: object):
        self.__provider = provider
    
    def apply(self, ctx: Context) -> object:
        ctx.setResponseCode(StatusCode.NO_CONTENT)
        provider.get().controllerMethod()
        if ctx.isResponseStarted():
            return ctx
        else:
            return ctx.send(ctx.getResponseCode())