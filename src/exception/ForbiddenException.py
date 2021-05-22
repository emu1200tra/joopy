from StatusCode import StatusCode
from StatusCodeBase import StatusCodeBase
from StatusCodeException import StatusCodeException

class ForbiddenException(StatusCodeException):
    def __init__(self, message):
        super(ForbiddenException, self).__init__(StatusCode.FORBIDDEN, message)


def main():
    aa = ForbiddenException("Hi")
    import ipdb; ipdb.set_trace()


if __name__ == "__main__":
    main()
