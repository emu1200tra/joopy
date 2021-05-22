from StatusCode import StatusCode
from StatusCodeBase import StatusCodeBase
from StatusCodeException import StatusCodeException


"""
Usage:
BadRequestException("Message")
if we call getStatusCode() method, it will return BAD_REQUEST StatusCode

"""

class BadRequestException(StatusCodeException):
    def __init__(self, message):
        super(BadRequestException, self).__init__(StatusCode.BAD_REQUEST, message)


def main():
    aa = BadRequestException("Some")
    import ipdb; ipdb.set_trace()


if __name__ == "__main__":
    main()
