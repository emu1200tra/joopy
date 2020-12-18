from .error_handler import ErrorHandler
from ..Logger import Logger
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
    
    def apply(self, ctx, cause, code):
        log = Logger()
        log.error(ErrorHandler.errorMessage(ctx, code), cause)
        #type = ctx.accept([])
        '''
        type = text or json or html (from MediaType)
        '''
