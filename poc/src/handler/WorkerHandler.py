from src.handler.LinkedHandler import LinkedHandler

class WorkerHandler(LinkedHandler):
    def __init__(self, _next):
        super(WorkerHandler, self).__init__()
        self.next = _next

    def apply(self, context):
        pass
