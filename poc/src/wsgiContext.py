class wsgiContext(object):
	def __init__(self, request, router):
		super(wsgiContext, self).__init__()
		self.request = request
		self.router = router
		self.method = self.environ['REQUEST_METHOD']
		self.requestPath = environ['PATH_INFO']