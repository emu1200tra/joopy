from StatusCode import StatusCode
from StatusCodeBase import StatusCodeBase
from StatusCodeException import StatusCodeException
from RuntimeException import RuntimeException


"""
Thrown when Jooby was unable to initialize and start
an application up.

"""

class StartupException(RuntimeException):
    def __init__(self, message):
        super(StartupException, self).__init__(message)
        """
        Creates a new instance of this class with the specified message.
        @param message The message
        """
        self.__message = message

    def __str__(self):
        return "Startup Exception : {}".format(self.__message)


def main():
    message = "Application startup resulted in exception"
    aa = StartupException(message)
    import ipdb; ipdb.set_trace()


if __name__ == "__main__":
    main()