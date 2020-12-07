from .ErrorHandler import ErrorHandler
class DefaultErrorHandler(ErrorHandler):
    '''
    * Default error handler with content negotiation support and optionally mute log statement base
    * on status code or exception types.
    *
    * @author edgar
    * @since 2.4.1
    '''
    def __init__(self):
        self.muteCodes = set()
        self.muteTypes = set()
