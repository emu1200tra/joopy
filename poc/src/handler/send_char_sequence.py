from ..context import Context
from ..Route import Route
from .linked_handler import LinkedHandler

class SendCharSequence(LinkedHandler):
    def __init__(self, _next):
        self.next = _next
    def apply(self, ctx):
        try:
            result = next.apply(ctx)
            if ctx.is_response_started():
                return result
            return ctx.send(str(result))
        except Exception:
            ctx.send_error(Exception)
    def next(self):
        return self.next