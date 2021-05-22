from .linked_handler import LinkedHandler
from ..context import Context
from ..head_context import HeadContext
from ..Router import Router
class HeadResponseHandler(LinkedHandler):
    def __init__(self, next):
        self.next = next
    def next(self):
        return self.next
    def apply(self, ctx):
        return next.apply(HeadContext(ctx)) if ctx.get_method().equals(Router.HEAD) else next.apply(ctx)
