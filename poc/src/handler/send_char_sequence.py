from ..context import Context
from ..Route import Route
from .linked_handler import LinkedHandler

class SendCharSequence(LinkedHandler):
    def __init__(self, _next):
        self.next = _next
    def apply(self, context):
        try:
            result = next.apply(context)
            if ctx.is_response_started():
                return result
            return context.send(str(result))
        except Exception:
            context.send_error(Exception)
    def next(self):
        return self.next