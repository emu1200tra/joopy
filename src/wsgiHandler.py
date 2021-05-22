from .wsgiContext import wsgiContext

class wsgiHandler(object):
    def __init__(self, app):
        super().__init__()
        self.router = app

    def __call__(self, environ, start_response):
        response_status = '200 OK'

        context = wsgiContext(environ, self.router)      

        self.router.match(context).execute(context)  

        headers = [('Content-type', context.header)]

        start_response(context.statusCode, headers)

        #dirty method, this should be done by handler pipeline
        # context.extract()
        
        return [context.body]
        '''
        if handler:
            return [handler.execute(context)]
        else:
            response_status = "404 NOT FOUND"
            start_response(response_status, headers)
            return None
        '''