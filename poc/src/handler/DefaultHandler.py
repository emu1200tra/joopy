from .LinkedHandler import LinkedHandler
from ..Context import Context
class DefaultHandler(LinkedHandler):
    def __init__(self, next):
        self.next = next
    def apply(self, ctx):
        try:
            result = next.apply(ctx)
            if ctx.isResponseStarted():
                return result
            ctx.render(result)
            return result
        except Exception:
            ctx.sendError(Exception)
            return x
    def next(self):
        return self.next