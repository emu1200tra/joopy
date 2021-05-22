from StatusCode import StatusCode
from StatusCodeBase import StatusCodeBase
from StatusCodeException import StatusCodeException


"""
Thrown when a required service is not available.

"""


class RegistryException(StatusCodeException):
    def __init__(self, message):
        super(RegistryException, self).__init__(StatusCode.SERVER_ERROR, message)
        """
        Constructor.
        @param message Error message.
    
        """


def main():
    message = 'registry'
    aa = RegistryException(message)
    import ipdb; ipdb.set_trace()


if __name__ == "__main__":
    main()
