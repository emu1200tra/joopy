from ..context import Context
from ..Route import Route
from ..exception.StatusCode import StatusCode

class WebSocketHandler(Route.Handler):
    def __init__(self, handler):
        self.__handler = handler
    
    def apply(self, ctx):
        webSocket = ctx.header("Upgrade").value("").equalsIgnoreCase("WebSocket")
        if webSocket:
            ctx.upgrade(self.__handler)
        if not ctx.isResponseStarted():
            return ctx.send(StatusCode.NOT_FOUND)
        return ctx