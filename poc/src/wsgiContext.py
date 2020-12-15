class wsgiContext(object):
    def __init__(self, request, router):
        super(wsgiContext, self).__init__()
    	self.request = request
    	self.router = router
    	self.method = self.environ['REQUEST_METHOD']
    	self.requestPath = environ['PATH_INFO']
        self.pathMap = None
        self.route = None
        
    def getMethod(self):
        return self.method

    def getRequestPath(self):
        return self.requestPath

    def setPathMap(self, pathMap):
        self.pathMap = pathMap
        return self

    def setRoute(self, route):
        self.route = route
        return self