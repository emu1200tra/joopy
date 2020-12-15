from src.handler.LinkedHandler import LinkedHandler

class WorkerHandler(LinkedHandler):
    def __init__(self, _next):
        super(WorkerHandler, self).__init__()
        self.next = _next

    def apply(self, context):
        return context.dispatch(lambda: self.element)

    def element(self):
        try:
            self.next.apply(context)
        except Exception as e:
            context.sendError(e)

    def next(self):
        return self.next
