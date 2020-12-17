from StatusCodeBase import StatusCodeBase
from StatusCode import StatusCode
from RuntimeException import RuntimeException


"""
Usage:
0) StatusCodeException(StatusCode.OK)
1) StatusCodeException(StatusCode.OK, "message")

"""


class StatusCodeException(RuntimeException):
    def __init__(self, statusCode, message=None, cause=None):
        super(StatusCodeException, self).__init__(message, cause)
        self.__statusCode = StatusCodeBase(statusCode.value(), statusCode.toString())
        
    def getStatusCode(self):
        return self.__statusCode


def main():
    aa = StatusCode.OK
    bb = StatusCodeException(aa)
    cc = StatusCodeException(aa, "Hello")
    ff = bb.getStatusCode()
    import ipdb; ipdb.set_trace()


if __name__ == "__main__":
    main()