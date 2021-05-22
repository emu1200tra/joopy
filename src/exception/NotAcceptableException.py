from StatusCode import StatusCode
from StatusCodeBase import StatusCodeBase
from StatusCodeException import StatusCodeException


"""
Whether the accept header isn't acceptable.

"""


class NotAcceptableException(StatusCodeException):
    def __init__(self, contentType):
        super(NotAcceptableException, self).__init__(StatusCode.NOT_ACCEPTABLE, contentType)
        """
        Creates a new exception.
        @param contentType Content-Type or <code>null</code>.

        """

    def getContentType(self):
        # return getMessage()
        # Don't know how yet
        raise NotImplementedError


def main():
    aa = NotAcceptableException("contentType")
    import ipdb; ipdb.set_trace()


if __name__ == "__main__":
    main()