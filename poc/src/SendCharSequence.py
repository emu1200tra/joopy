from src.handler.LinkedHandler import LinkedHandler

class SendCharSequence(LinkedHandler):
    def __init__(self, _next):
        super(WorkerHandler, self).__init__()
        self.next = _next

    def apply(self, context):
        try:
            result = self.next.apply(context)
            if (context.isResponseStarted()):
                return result
            return context.send(str(result))
        except Exception as e:
            return context.sendError(e)

    def next(self):
        return self.next
