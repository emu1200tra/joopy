class RuntimeException(BaseException):
    def __init__(self, message=None, cause=None):
        super(RuntimeException, self).__init__()
        self.__message = message
        self.__cause = cause

    @property
    def message(self):
        return self.__message

    @property
    def cause(self):
        return self.__cause