from StatusCode import StatusCode
from StatusCodeBase import StatusCodeBase
from StatusCodeException import StatusCodeException

"""
This will often be used in Route

Whether a HTTP method isn't supported. The {@link #getAllow()} contains the supported
 * HTTP methods.

"""


class MethodNotAllowedException(StatusCodeException):
    def __init__(self, method, allow):
        super(MethodNotAllowedException, self).__init__(StatusCode.METHOD_NOT_ALLOWED)
        """
        Creates a new method not allowed exception.
        @param method Requested method.
        @param allow Allow methods.
        """
        self.__method = method
        # allow will be a list
        self.__allow = allow

    def getMethod(self):
        """
        Requested method.
        @return Requested method.

        """
        return self.__method

    def getAllow(self):
        """
        Allow methods.
        @return Allow methods.
        
        """
        return self.__allow


def main():
    method = "GET"
    allow = ["A", "L"]
    aa = MethodNotAllowedException(method, allow)
    import ipdb; ipdb.set_trace()


if __name__ == "__main__":
    main()
