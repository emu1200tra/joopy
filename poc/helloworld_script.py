from src.joopy import Joopy
# get: Send request to server and get data from it
# post: Send request to server with encrypted body (usually passwd or something that should be secret)
# put: Send request to server with data that would replace original data on remote
# delete: Send request to server to remove specific data


class myApp(Joopy):
    """
    Script API
    """

    def __init__(self):
        super(myApp, self).__init__()
        
        def decorator_sleep(_next):
            import time
            def handler(ctx):
                t1 = time.time()
                response = _next.apply(ctx)
                time.sleep(1)
                t2 = time.time()
                return response + '\nsleep time = {:.2f} sec'.format(t2-t1)
            return handler
        
        self.decorator(lambda _next: lambda ctx: _next.apply(ctx) + '\ndecorator is good !!!!')
        self.decorator(decorator_sleep)

        self.get("/", lambda ctx: 'home')

        self.get("/hello", lambda ctx: 'hello world')

        self.get("/goodbye", lambda ctx: 'good bye')

        def demo_app(ctx):
            data = self.prepare_html()
            ctx.set_header('text/html')
            return data

        self.get("/demo", lambda ctx: demo_app(ctx))

        '''
        post("/login", lambda x: 'login process')

        post("/database", lambda x: 'posting data')

        put("/database", lambda x: 'updating')

        delete("/database", lambda x: 'removing')
        '''
    def prepare_html(self, path="./demo.html"):
        file = open(path)
        lines = file.read()
        # lines = lines.encode("utf-8")
        file.close()
        return lines


if __name__ == '__main__':
    myApp.runApp(provider=myApp)
