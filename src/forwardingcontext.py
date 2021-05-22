from .context import Context
from multipledispatch import dispatch

class ForwardingContext(Context):
    def __init__(self, context):
        self.ctx = context

    def get_user(self):
        return self.ctx.get_user()

    def set_user(self, user):
        self.ctx.set_user(user)
        return self

    def forward(self, path):
        self.ctx.forward()
        return self

    def matches(self, pattern):
        return self.ctx.matches(pattern)

    def is_secure(self):
        return self.is_secure()

    def get_attribute(self):
        return self.ctx.get_attributes()

    @dispatch(str)
    def attribute(self, key):
        return self.ctx.attribute(key)

    @dispatch(str, object)
    def attribute(self, key, value):
        self.ctx.attribute(key, value)
        return self

    def get_router(self):
        return self.ctx.get_router()

    def flash(self):
        return self.ctx.flash()

    @dispatch(str)
    def session(self, name):
        return self.ctx.session(name)

    @dispatch()
    def session(self):
        return self.session()

    def session_or_null(self):
        return self.ctx.session_or_null()

    def cookie(self, name):
        return self.ctx.cookie(name)

    def cookie_map(self):
        return self.ctx.cookie_map()

    def get_method(self, method):
        self.ctx.get_method(method)
        return self

    def set_method(self, method):
        self.ctx.set_method(method)
        return self
    
    def get_route(self, route):
        return self.ctx.get_route()

    def set_route(self, route):
        return self.ctx.set_route(route)

    def get_request_path(self):
        return ctx.get_request_path()
  
    def set_request_path(self, path):
        self.ctx.set_request_path(path)
        return self

    @dispatch(str)
    def path(self, name):
        return self.ctx.path(name)
    
    @dispatch(object)
    def path(self, type):
        return self.ctx.path(type)

    @dispatch()
    def path(self):
        return self.ctx.path()   

    def path_map(self):
        return self.ctx.path_map()
    
    def set_path_map(self, pathMap):
        self.ctx.set_path_map(pathMap)
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

    def query_string(self): 
        return self.ctx.query_string()
    
    def query_map(self): 
        return self.ctx.query_map()

    def query_multimap(self): 
        return self.ctx.query_multimap()

    @dispatch()
    def header(self): 
        return self.ctx.header()
    
    @dispatch(str)
    def header(self, name):
        return self.ctx.header(name)
    
    def header_map(self): 
        return self.ctx.header_map()
    

    def header_multimap(self): 
        return self.ctx.header_multimap()
    
    @dispatch(MediaType)
    def accept(self, contentType):
        return self.ctx.accept(contentType)
    
    @dispatch(List[MediaType])
    def accept(self, produceTypes):
        return self.ctx.accept(produceTypes)
    
    @dispatch()
    def get_request_type(self):
        return self.ctx.get_request_type()

    @dispatch(MediaType)
    def get_request_type(self, defaults):
        return self.ctx.get_request_type(defaults)
    

    def get_request_length(self):
        return self.ctx.get_request_length()
    
    def get_remote_address(self):
        return self.ctx.get_remote_address()
    
    def set_remote_address(self, remote_address):
        self.ctx.set_remote_address(remote_address)
        return self

    def get_host(self): 
        return self.ctx.get_host()
    
    def set_host(self, host):
        self.ctx.set_host(host)
        return self
    
    def get_server_port(self): 
        return self.ctx.get_server_port()
    

    def get_server_host(self): 
        return self.ctx.get_server_host()
    

    def get_port(self):
        return self.ctx.get_port()
    

    def set_port(self, port):
        self.self.ctx.set_port(port)
        return self
    
    def get_host_and_port(self): 
        return self.ctx.get_host_and_port()

    @dispatch()
    def get_request_url(self):
        return self.ctx.get_request_url()

    @dispatch(str)
    def get_request_url(self, path): 
        return self.ctx.get_request_url(path)
    

    def get_protocol(self):
        return self.ctx.get_protocol()
    
    def get_scheme(self): 
        return self.ctx.get_scheme()
    
    def set_scheme(self, scheme):
        self.self.ctx.set_scheme(scheme)
        return self
    
    def form_multimap(self): 
        return self.ctx.form_multimap()
    
    def form_map(self): 
        return self.ctx.form_map()
    
    @dispatch()
    def form(self): 
        return self.ctx.form()

    @dispatch(str)
    def form(self, name):
        return self.ctx.form(name)
    
    @dispatch(object)
    def form(self, type):
        return self.ctx.form(type)
    
    @dispatch()
    def multipart(self): 
        return self.ctx.multipart()
    
    @dispatch(str)
    def multipart(self, name):
        return self.ctx.multipart(name)
    
    @dispatch(object)
    def multipart(self, type):
        return self.ctx.multipart(type)
    

    def multipart_multimap(self): 
        return self.ctx.multipart_multimap()
    
    def multipart_map(self):
        return self.ctx.multipart_map()
    
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
    
    @dispatch(object)
    def body(self, type):
        return self.ctx.body(type)
    

    def convert(self, value, type):
        return self.ctx.convert(value, type)

    def decode(self, type, contentType):
        return self.ctx.decode(type, contentType)
    
    def decoder(self, contentType):
        return self.ctx.decoder(contentType)
    
    def is_in_io_thread(self):
        return self.ctx.is_in_io_thread()
    
    @dispatch(Runnable)
    def _dispatch(self, action):
        self.ctx.dispatch(action)
        return self
    
    @dispatch(Executor, Runnable)
    def _dispatch(self, executor, action):
        self.ctx.dispatch(executor, action)
        return self

    def detach(self, next):
        self.ctx.detach(next)
        return self
    

    def upgrade(self, handler):
        self.ctx.upgrade(handler)
        return self

    @dispatch(str, str)
    def set_response_header(self, name, value):
        self.ctx.set_response_header(name, value)
        return self

    @dispatch(str)
    def set_response_header(self, name):
        self.ctx.set_response_header(name)
        return self
    
    def remove_response_header(self, name):
        self.ctx.remove_response_header(name)
        return self    

    def remove_response_headers(self):
        self.ctx.remove_response_headers()
        return self
    

    def get_response_header(self, name):
        return self.ctx.get_response_header(name)
    

    def get_response_length(self):
        return self.ctx.get_response_length()
    
    def set_response_length(self, length):
        self.ctx.set_response_length(length)
        return self
    

    def set_response_cookie(self, cookie):
        self.ctx.set_response_cookie(cookie)
        return self
    
    @dispatch(MediaType)
    def set_response_type(self, contentType):
        self.ctx.set_response_type(contentType)
        return self
    
    @dispatch(MediaType, Charset)
    def set_response_type(self, contentType, charset):
        self.ctx.set_response_type(contentType, charset)
        return self


    def set_default_responseType(self, contentType):
        self.ctx.set_responseType(contentType)
        return self
    

    def get_responseType(self):
        return self.ctx.get_responseType()
    
    def set_response_code(self, statusCode):
        self.ctx.set_response_code(statusCode)
        return self
    
    def get_response_code(self): 
        return self.ctx.get_response_code()
    

    def render(self, value):
        self.ctx.render(value)
        return self
    

    def response_stream(self): 
        return self.ctx.r_sponse_stream()
    

    def response_stream(self, contentType):
        return self.ctx.response_stream(contentType)
    '''
    def responseStream(self, contentType, consumer):
        return self.ctx.responseStream(contentType, consumer)

    def responseStream(self, consumer):
        return self.ctx.responseStream(consumer)
    '''

    def response_sender(self): 
        return self.ctx.response_sender()
    

    def response_writer(self): 
        return self.ctx.response_writer()
    
    @dispatch(MediaType)
    def response_writer(self, contentType):
        return self.ctx.response_writer(contentType)
    
    @dispatch(MediaType, Charset)
    def response_writer(self, contentType, charset):
        return self.ctx.response_writer(contentType, charset)
    '''
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

    @dispatch(str, Charset)
    def send(self, data, charset):
        self.ctx.send(data, charset)
        return self

    
    @dispatch(Exception)
    def sendError(self, cause):
        self.ctx.sendError(cause)
        return self
    
    @dispatch(Exception, StatusCode)
    def sendError(self, cause, code):
        self.ctx.sendError(cause, code)
        return self
    

    def is_response_started(self):
        return self.ctx.is_response_started()
    
    @dispatch()
    def get_reset_headers_on_error(self):
        return self.ctx.get_reset_headers_on_error()
    
    @dispatch(bool)
    def set_reset_headers_on_error(self, value):
        self.ctx.set_reset_headers_on_error(value)
        return self
    

    def on_complete(self, task):
        self.ctx.on_complete(task)
        return self
    
    @dispatch(object)
    def require(self, type): 
        return self.ctx.require(type)
    
    @dispatch(object, str)
    def require(self, type, name):
        return self.ctx.require(type, name)
    
    '''
    def require(self, key):
        return self.ctx.require(key)
    '''

    def toString(self): 
        return self.ctx.toString()
    
