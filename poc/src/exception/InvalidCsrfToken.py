from StatusCode import StatusCode
from StatusCodeBase import StatusCodeBase
from ForbiddenException import ForbiddenException

class InvalidCsrfToken(ForbiddenException):
    def __init__(self, token):
        super(InvalidCsrfToken, self).__init__(token)


def main():
    aa = InvalidCsrfToken("xkdld")
    import ipdb; ipdb.set_trace()


if __name__ == "__main__":
    main()
