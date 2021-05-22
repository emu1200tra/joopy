from StatusCode import StatusCode
from StatusCodeBase import StatusCodeBase
from StatusCodeException import StatusCodeException

"""
Whether there is no decoder for the requested <code>Content-Type</code>

"""


class UnsupportedMediaType(StatusCodeException):
    def __init__(self, Type):
        super(UnsupportedMediaType, self).__init__(StatusCode.UNSUPPORTED_MEDIA_TYPE, Type)
        """
        Unsupported media type.
        @param type Content Type. Optional.
        
        """
        self.__type = Type

    def getContentType(self):
        # return getMessage()
        # Don't know how yet
        raise NotImplementedError
