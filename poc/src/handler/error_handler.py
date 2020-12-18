#from src.handler.DefaultErrorHandler import DefaultErrorHandler
class ErrorHandler():
    '''
    * Catch and encode application errors.
    *
    * @author edgar
    * @since 2.0.0
    '''
    def apply(self, ctx, cause, code):
        '''
        * Produces an error response using the given exception and status code.
        *
        * @param ctx Web context.
        * @param cause Application error.
        * @param code Status code.
        '''
        pass
    def then(self, next):
        '''
        * Chain this error handler with next and produces a new error handler.
        *
        * @param next Next error handler.
        * @return A new error handler.
        '''
        def _then(ctx, cause, statusCode):
            apply(ctx, cause, statusCode)
            if not ctx.isResponseStarted():
                next.apply(ctx, cause, statusCode)
        return lambda ctx, cause, statusCode : _then(ctx, cause, statusCode)
    def errorMessage(self, ctx, statusCode):
        '''
        * Build a line error message that describe the current web context and the status code.
        *
        * <pre>GET /path Status-Code Status-Reason</pre>
        *
        * @param ctx Web context.
        * @param statusCode Status code.
        * @return Single line message.
        '''
        message = ctx.getMethod()
        message += ' '
        message += ctx.getRequestPath()
        message += ' '
        message += statusCode.value()
        message += ' '
        message += statusCode.reason()
        return message
    def create(self):
        from src.handler.DefaultErrorHandler import DefaultErrorHandler
        return DefaultErrorHandler()