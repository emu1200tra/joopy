from .linked_handler import LinkedHandler

class WorkerHandler(LinkedHandler):
    def __init__(self, _next):
        # super(WorkerHandler, self).__init__()
        self.__next = _next

    def apply(self, context):
        def element():
            try:
                self.__next.apply(context)
            except Exception as e:
                context.send_error(e)

        return context.dispatch(element)

    def next(self):
        return self.__next
