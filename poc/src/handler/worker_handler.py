from .linked_handler import LinkedHandler

class WorkerHandler(LinkedHandler):
    def __init__(self, _next):
        super(WorkerHandler, self).__init__()
        self.next = _next

    def apply(self, context):
        return context.dispatch(lambda ctx: self.element(ctx))

    def element(self, ctx):
        try:
            self.next.apply(ctx)
        except Exception as e:
            ctx.send_error(e)

    def next(self):
        return self.next
