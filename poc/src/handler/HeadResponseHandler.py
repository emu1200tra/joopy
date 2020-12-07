from .LinkedHandler import LinkedHandler
from ..Context import Context
from ..HeadContext import HeadContext
class HeadResponseHandler(LinkedHandler):
    def __init__(self, next):
        self.next = next
    def next(self):
        return self.next
    def apply(self, ctx):
        return next.apply(HeadContext(ctx)) if ctx.getMethod().equals(Router.HEAD) else next.apply(ctx)
