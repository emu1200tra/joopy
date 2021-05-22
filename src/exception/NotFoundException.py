from .StatusCode import StatusCode
from .StatusCodeBase import StatusCodeBase
from .StatusCodeException import StatusCodeException


"""
When a request doesn't match any of the available routes.

"""

class NotFoundException(StatusCodeException):
    def __init__(self, path):
        super(NotFoundException, self).__init__(StatusCode.NOT_FOUND, path)
        """
        Creates a not found exception.
        @param path Requested path

        """

    def getRequestPath(self):
        # return getMessage()
        # where is getMessage defined ?
        raise NotImplementedError


def main():
    path = './here'
    aa = NotFoundException(path)
    import ipdb; ipdb.set_trace()


if __name__ == "__main__":
    main()
