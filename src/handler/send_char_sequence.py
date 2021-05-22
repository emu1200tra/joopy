from ..context import Context
from ..Route import Route
from .linked_handler import LinkedHandler

class SendCharSequence(LinkedHandler):
    def __init__(self, _next):
        self.__next = _next

    def apply(self, ctx):
        try:
            result = self.__next.apply(ctx)
            if ctx.is_response_started():
                return result
            return ctx.send(result) # result.toString()
        except Exception as e:
            ctx.send_error(e)
    
    def next(self):
        return self.__next