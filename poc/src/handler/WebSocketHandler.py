from ..Context import Context
from ..Route import Handler
from ..StatusCode import StatusCode
from ..WebSocket import WebSocket

class WebSocketHandler(Handler):
    def __init__(self, handler):
        self.handler = handler
    def apply(self, ctx):
        webSocket = ctx.header("Upgrade").value("").equalsIgnoreCase("WebSocket")
        if webSocket:
            ctx.upgrade(handler)
        if not ctx.isResponseStarted():
            return ctx.send(StatusCode.NOT_FOUND)
        return ctx