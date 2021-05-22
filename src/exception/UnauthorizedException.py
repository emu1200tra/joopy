from StatusCode import StatusCode
from StatusCodeBase import StatusCodeBase
from StatusCodeException import StatusCodeException


"""
Specific error for unauthorized access.

"""


class UnauthorizedException(StatusCodeException):
    def __init__(self, message):
        super(UnauthorizedException, self).__init__(StatusCode.UNAUTHORIZED, message)
        """
        Creates an unauthorized exception.
        @param message Message. Optional.
        
        """


def main():
    message = "Unauthorize"
    aa = UnauthorizedException(message)
    import ipdb; ipdb.set_trace()


if __name__ == "__main__":
    main()
