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

        self.get("/", lambda ctx: b'home')

        self.get("/hello", lambda ctx: b'hello world')

        self.get("/goodbye", lambda ctx: b'good bye')

        def demo_app(ctx):
            data = self.prepare_html()
            ctx.set_header('text/html')
            return data

        self.get("/demo", lambda ctx: demo_app(ctx))

        '''
        post("/login", lambda x: b'login process')

        post("/database", lambda x: b'posting data')

        put("/database", lambda x: b'updating')

        delete("/database", lambda x: b'removing')
        '''
    def prepare_html(self, path="./demo.html"):
        file = open(path)
        lines = file.read()
        lines = lines.encode("utf-8")
        file.close()
        return lines


if __name__ == '__main__':
    myApp.runApp(provider=myApp)
