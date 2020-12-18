from .linked_handler import LinkedHandler
from ..context import Context
class DefaultHandler(LinkedHandler):
    def __init__(self, next):
        self.next = next
    def apply(self, ctx):
        try:
            result = next.apply(ctx)
            if ctx.is_response_started():
                return result
            ctx.render(result)
            return result
        except Exception:
            ctx.send_error(Exception)
            return Exception
    def next(self):
        return self.next
