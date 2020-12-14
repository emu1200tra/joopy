from src.wsgiContext import wsgiContext

class wsgiHandler(object):
    def __init__(self, app):
        super().__init__()
        self.router = app

    def __call__(self, environ, start_response):
        response_status = '200 OK'
        headers = [('Content-type', 'text/plain')]

        context = wsgiContext(environ, self.router)        

        body = self.router.match(context)
        if body:
            start_response(response_status, headers)
            return [body.execute(context)]
        else:
            response_status = "404 NOT FOUND"
            start_response(response_status, headers)
            return None
