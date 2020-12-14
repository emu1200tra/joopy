from .context import Context
from multipledispatch import dispatch

class ForwardingContext(Context):
    def __init__(self, context):
        self.ctx = context

    def getUser(self):
        return self.ctx.getUser()

    def setUser(self, user):
        self.ctx.setUser(user)
        return self

    def forward(self, path):
        self.ctx.forward()
        return self

    def matches(self, pattern):
        return self.ctx.matches(pattern)

    def isSecure(self):
        return self.isSecure()

    def getAttribute(self):
        return self.ctx.getAttributes()

    @dispatch(str)
    def attribute(self, key):
        return self.ctx.attribute(key)

    @dispatch(str, object)
    def attribute(self, key, value):
        self.ctx.attribute(key, value)
        return self

    def getRouter(self):
        return self.ctx.getRouter()

    def flash(self):
        return self.ctx.flash()

    @dispatch(str)
    def session(self, name):
        return self.ctx.session(name)

    @dispatch()
    def session(self):
        return self.session()

    def sessionOrNull(self):
        return self.ctx.sessionOrNull()

    def cookie(self, name):
        return self.ctx.cookie(name)

    def cookieMap(self):
        return self.ctx.cookieMap()

    def getMethod(self, method):
        self.ctx.setMethod(method)
        return self

    def setMethod(self, method):
        self.ctx.setMethod(method)
        return self
    
    def getRoute(self, route):
        return self.ctx.getRoute()

    def setRoute(self, route):
        return self.ctx.setRoute(route)

    def getRequestPath(self):
        return ctx.getRequestPath()
  
    def setRequestPath(self, path):
        self.ctx.setRequestPath(path)
        return self

    def path(self, name):
        return self.ctx.path(name)
  
    def path(self, type):
        return self.ctx.path(type)

    def path(self):
        return self.ctx.path()   

    def pathMap(self):
        return self.ctx.pathMap()
    
    def setPathMap(self, pathMap):
        self.ctx.setPathMap(pathMap)
        return self

    @dispatch()
    def query(self): 
        return self.ctx.query()

    @dispatch(str)
    def query(self, name):
        return self.ctx.query(name)
    
    @dispatch()
    def query(self, type):
        return self.ctx.query(type)

    def queryString(self): 
        return self.ctx.queryString()
    
    def queryMap(self): 
        return self.ctx.queryMap()

    def queryMultimap(self): 
        return self.ctx.queryMultimap()

    @dispatch()
    def header(self): 
        return self.ctx.header()
    
    @dispatch(str)
    def header(self, name):
        return self.ctx.header(name)
    
    def headerMap(self): 
        return self.ctx.headerMap()
    

    def headerMultimap(self): 
        return self.ctx.headerMultimap()
    '''
    @dispatch()
    def accept(self, contentType):
        return self.ctx.accept(contentType)
    
    @dispatch()
    def accept(self, produceTypes):
        return self.ctx.accept(produceTypes)
    
    @dispatch()
    def getRequestType(self):
        return self.ctx.getRequestType()

    @dispatch()
    def getRequestType(self, defaults):
        return self.ctx.getRequestType(defaults)
    '''

    def getRequestLength(self):
        return self.ctx.getRequestLength()
    
    def getRemoteAddress(self):
        return self.ctx.getRemoteAddress()
    
    def setRemoteAddress(self, remoteAddress):
        self.ctx.setRemoteAddress(remoteAddress)
        return self

    def getHost(self): 
        return self.ctx.getHost()
    
    def setHost(self, host):
        self.ctx.setHost(host)
        return self
    
    def getServerPort(self): 
        return self.ctx.getServerPort()
    

    def getServerHost(self): 
        return self.ctx.getServerHost()
    

    def getPort(self):
        return self.ctx.getPort()
    

    def setPort(self, port):
        self.self.ctx.setPort(port)
        return self
    
    def getHostAndPort(self): 
        return self.ctx.getHostAndPort()

    @dispatch()
    def getRequestURL(self):
        return self.ctx.getRequestURL()

    @dispatch(str)
    def getRequestURL(self, path): 
        return self.ctx.getRequestURL(path)
    

    def getProtocol(self):
        return self.ctx.getProtocol()
    
    def getScheme(self): 
        return self.ctx.getScheme()
    
    def setScheme(self, scheme):
        self.self.ctx.setScheme(scheme)
        return self
    
    def formMultimap(self): 
        return self.ctx.formMultimap()
    
    def formMap(self): 
        return self.ctx.formMap()
    
    @dispatch()
    def form(self): 
        return self.ctx.form()

    @dispatch(str)
    def form(self, name):
        return self.ctx.form(name)
    '''
    @dispatch()
    def form(self, type):
        return self.ctx.form(type)
    '''
    @dispatch
    def multipart(self): 
        return self.ctx.multipart()
    
    @dispatch(str)
    def multipart(self, name):
        return self.ctx.multipart(name)
    '''
    @dispatch()
    def multipart(self, type):
        return self.ctx.multipart(type)
    '''

    def multipartMultimap(self): 
        return self.ctx.multipartMultimap()
    
    def multipartMap(self):
        return self.ctx.multipartMap()
    
    @dispatch()
    def files(self): 
        return self.ctx.files()
    
    @dispatch(str)
    def files(self, name):
        return self.ctx.files(name)
    
    def file(self, name):
        return self.ctx.file(name)
    
    @dispatch()
    def body(self):
        return self.ctx.body()
    '''
    @dispatch()
    def body(self, type):
        return self.ctx.body(type)
    '''

    def convert(self, value, type):
        return self.ctx.convert(value, type)

    def decode(self, type, contentType):
        return self.ctx.decode(type, contentType)
    
    def decoder(self, contentType):
        return self.ctx.decoder(contentType)
    
    def isInIoThread(self):
        return self.ctx.isInIoThread()
    
    '''
    @dispatch
    def dispatch(self, action):
        self.ctx.dispatch(action)
        return self
    
    @dispatch.add
    def dispatch(self, executor, action):
        self.ctx.dispatch(executor, action)
        return self
    '''

    def detach(self, next):
        self.ctx.detach(next)
        return self
    

    def upgrade(self, handler):
        self.ctx.upgrade(handler)
        return self

    def setResponseHeader(self, name, value):
        self.ctx.setResponseHeader(name, value)
        return self
    
    @dispatch(str)
    def removeResponseHeader(self, name):
        self.ctx.removeResponseHeader(name)
        return self
    
    @dispatch()
    def removeResponseHeaders(self):
        self.ctx.removeResponseHeaders()
        return self
    

    def getResponseHeader(self, name):
        return self.ctx.getResponseHeader(name)
    

    def getResponseLength():
        return self.ctx.getResponseLength()
    
    def setResponseLength(self, length):
        self.ctx.setResponseLength(length)
        return self
    

    def setResponseCookie(self, cookie):
        self.ctx.setResponseCookie(cookie)
        return self
    

    def setResponseType(self, contentType):
        self.ctx.setResponseType(contentType)
        return self
    
    '''
    def setResponseType(self, contentType, charset):
        self.ctx.setResponseType(contentType, charset)
        return self
    '''

    def setDefaultResponseType(self, contentType):
        self.ctx.setResponseType(contentType)
        return self
    

    def getResponseType(self):
        return self.ctx.getResponseType()
    
    def setResponseCode(self, statusCode):
        self.ctx.setResponseCode(statusCode)
        return self
    
    def getResponseCode(self): 
        return self.ctx.getResponseCode()
    

    def render(self, value):
        self.ctx.render(value)
        return self
    

    def responseStream(self): 
        return self.ctx.responseStream()
    

    def responseStream(self, contentType):
        return self.ctx.responseStream(contentType)
    '''
    def responseStream(self, contentType, consumer):
        return self.ctx.responseStream(contentType, consumer)

    def responseStream(self, consumer):
        return self.ctx.responseStream(consumer)
    '''

    def responseSender(self): 
        return self.ctx.responseSender()
    

    def responseWriter(self): 
        return self.ctx.responseWriter()
    

    def responseWriter(self, contentType):
        return self.ctx.responseWriter(contentType)
    
    '''
    def responseWriter(self, contentType, charset):
        return self.ctx.responseWriter(contentType, charset)

    def responseWriter(self, consumer):
        return self.ctx.responseWriter(consumer)
    
    def responseWriter(self, contentType, consumer):
        return self.ctx.responseWriter(contentType, consumer)

    def responseWriter(self, contentType, charset, consumer):
        return self.ctx.responseWriter(contentType, charset, consumer)
    '''

    @dispatch(str)
    def sendRedirect(self, location):
        self.ctx.sendRedirect(location)
        return self
    
    @dispatch(StatusCode, str)
    def sendRedirect(self, redirect, location):
        self.ctx.sendRedirect(redirect, location)
        return self
    
    @dispatch(str)
    def send(self, data):
        self.ctx.send(data)
        return self
    '''
    @dispatch(str, Charset)
    def send(self, data, charset):
        self.ctx.send(data, charset)
        return self
    '''
    
    @dispatch(Exception)
    def sendError(self, cause):
        self.ctx.sendError(cause)
        return self
    
    @dispatch(Exception, StatusCode)
    def sendError(self, cause, code):
        self.ctx.sendError(cause, code)
        return self
    

    def isResponseStarted(self):
        return self.ctx.isResponseStarted()
    
    @dispatch()
    def getResetHeadersOnError(self):
        return self.ctx.getResetHeadersOnError()
    
    @dispatch(bool)
    def setResetHeadersOnError(self, value):
        self.ctx.setResetHeadersOnError(value)
        return self
    

    def onComplete(self, task):
        self.ctx.onComplete(task)
        return self
    
    '''
    def require(self, type): 
        return self.ctx.require(type)
    

    def require(self, type, name):
        return self.ctx.require(type, name)
    

    def require(self, key):
        return self.ctx.require(key)
    '''

    def toString(self): 
        return self.ctx.toString()
    
