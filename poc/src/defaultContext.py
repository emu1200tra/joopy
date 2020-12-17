from multipledispatch import dispatch

from src import Server
from src.context import Context
import datetime

from PyByteBuffer import ByteBuffer

from src.handler.ErrorHandler import ErrorHandler
from .todo import *


class DefaultContext(Context):
    def __init__(self):
        pass

    @dispatch(object, str)
    def require(self, classType, name):
        raise Exception(Context.get_route().require(classType, name))

    @dispatch(object)
    def require(self, classType):
        raise Exception(Context.get_route().require(classType))

    @dispatch(ServiceKey)
    def require(self, key):
        raise Exception(Context.get_route().require(key))

    def get_user(self):
        return Context.get_attributes().get("user")

    def set_user(self, user):
        return Context.get_attributes().put("user", user)

    def matches(self, pattern):
        return Context.get_router().match(pattern, Context.get_request_path())

    @dispatch(str)
    def attribute(self, key):
        attribute = Context.get_attributes().get(key)
        if attribute is None:
            _globals = Context.get_router().get_attribute()
            attribute = _globals.get(key)
        return attribute

    @dispatch(str, object)
    def attribute(self, key, value):
        Context.get_attributes().put(key, value)
        return self

    @dispatch()
    def flash(self):
        return Context.get_attributes().computeIfAbsent(FlashMap.NAME, lambda key: FlashMap.create(self,Context.get_router().getFlashCookie().clone()))

    @dispatch(str)
    def flash(self, name):
        return Value.create(self, name, Context.flash().get())

    @dispatch(str)
    def session(self, name):
        session = Context.sessionOrNull()
        if session is not None:
            return session.get(name)

        return Value.missing(name)

    @dispatch()
    def session(self):
        session = Context.sessionOrNull()
        if session is None:
            store = Context.get_router().get_session_store()
            session = store.new_session(self)
            if session is not None:
                Context.get_attributes().put(Session.Name, session)

        return session

    def session_or_null(self):
        session = Context.get_attributes().get(Session.Name)
        if session is None:
            router = Context.get_router()
            store = router.get_session_store()
            session = store.find_session(self)
            if session is not None:
                Context.get_attributes().put(Session.Name, session)

        return session

    def forward(self, path):
        Context.set_request_path(path)
        Context.get_router().match(self).execute(self)
        return self

    def cookie(self, name):
        value = Context.cookieMap().get(name)
        return Value.missing(name) if value is None else Value.value(self, name, value)

    @dispatch(str)
    def path(self, name):
        value = Context.path_map().get(name)
        return MissingValue(name) if value is None else SingleValue(self, name, UrlParser.decode_path_segment(value))

    @dispatch(object)
    def path(self, class_type):
        return Context.path().to(class_type)

    @dispatch()
    def path(self):
        path = HashValue(self, None)
        for entry in Context.path_map().entry_set():
            path.put(entry.get_key(), entry.get_value())

    @dispatch(str)
    def query(self, name):
        return self.query().get(name)

    @dispatch(object)
    def query(self, class_type):
        return self.query().to(class_type)

    def query_string(self):
        return self.query().query_string()

    def query_map(self):
        return self.query().to_multimap()

    def header(self, name):
        return self.header().get(name)

    def header_map(self):
        return self.header().to_map()

    def header_multimap(self):
        return self.header().to_multimap()

    def accept(self, content_type):
        accept = Context.header("Accept")
        return accept.is_missing() or content_type.matches(accept.value())

    def accept(self, produce_types):
        accept_types = MediaType.parse(Context.header("Accept").value_or_null())
        result = None
        for accept_type in accept_types:
            for produce_type in produce_types:
                if produce_type.matches(accept_type):
                    if result is None:
                        result = produce_type
                    else:
                        _max = MediaType.MOST_SPECIFIC.apply(result, produce_type)
                        if _max is not result:
                            result = _max

        return result

    @dispatch()
    def get_request_url(self):
        return self.get_request_url("")

    @dispatch(str)
    def get_request_url(self, path):
        scheme = Context.get_scheme()
        host = Context.get_host()
        port = Context.get_port()
        url = ""
        url += scheme
        url += "://"
        url += host

        if port > 0 and port is not 80 and port is not 443:
            url += ":"
            url += port

        if path is None or len(path) == 0:
            url += Context.get_request_path()
        else:
            context_path = Context.get_context_path()
            if context_path != "/" and path.startswith(context_path):
                url += context_path
            url += path
        url += Context.query_string()

        return url

    @dispatch()
    def get_request_type(self) -> MediaType:
        contentType = self.header("Content-Type")
        return None if contentType.is_missing() else MediaType.valueOf(contentType.value())

    @dispatch(object)
    def get_request_type(self, defaults: MediaType) -> MediaType:
        contentType = self.header("Content-Type")
        return defaults if contentType.is_missing() else MediaType.valueOf(contentType.value())

    def get_request_length(self) -> int:
        contentLength = self.header("Content-Length")
        return -1 if contentLength.is_missing() else contentLength.longValue()

    def get_host_and_port(self) -> str:
        header = self.header("X-Forwarded-Host") if self.get_router().isTrustProxy() \
            else None
        value = header if header is not None else lambda x: header("Host").value(self.get_server_host() + ":" + self.getServerPort())
        i = value.find(",")
        host = value[0: i].strip(" ") if i > 0 else value
        if host.startsWith("[") and host.endsWith("]"):
            return host[1, len(host)-1].strip()
        return host

    def get_server_host(self):
        host = self.get_router().get_server_options().get_host()
        return "localhost" if host == "0.0.0.0" else host

    def get_server_port(self) -> int:
        options = self.get_router().get_server_options()
        return options.get_secure_port() if self.is_secure() else options.get_port()

    def get_port(self) -> int:
        hostAndPort = self.get_host_and_port()
        if hostAndPort is not None:
            index = hostAndPort.find(":")
            if index > 0:
                return int(hostAndPort[index+1:])
            return 443 if self.is_secure() else 80

    def get_host(self) -> str:
        hostAndPort = self.get_host_and_port()
        if hostAndPort is not None:
            index = hostAndPort.find(":")
            return hostAndPort[0:index].strip() if index > 0 else hostAndPort
        return self.get_server_host()

    def is_secure(self) -> bool:
        return self.get_scheme() == "https"

    def form_multimap(self) -> object:
        return self.form().to_multimap()

    def form_map(self) -> object:
        return self.form().to_map()

    @dispatch(str)
    def form(self, name: str) -> ValueNode:
        return self.form().get(name)

    @dispatch(object)
    def form(self, type: object) -> object:
        return self.form().to(type)

    @dispatch(str)
    def multipart(self, name: str) -> ValueNode:
        return self.multipart().get(name)

    @dispatch(object)
    def multipart(self, type:object) -> object:
        return self.multipart().to(type)

    def multipart_multimap(self) -> object:
        return self.multipart().to_multimap()

    def multipart_map(self) -> object:
        return self.multipart().to_map()

    @dispatch()
    def files(self) -> object:
        return self.multipart().files()

    @dispatch(str)
    def files(self, name: str) -> object:
        return self.multipart().files(name)

    def file(self, name: str) -> FileUpload:
        return self.multipart().file(name)

    def body(self, type: object) -> object:
        return self.body().to(type)

    def convert(self, value: ValueNode, type: object) -> object:
        result = ValueConverters.convert(value, type, self.get_router())
        if result is None:
            raise Exception
        return result

    def decode(self, type: object, contentType: MediaType):
        try:
            if MediaType.text == contentType:
                result = ValueConverters.convert(self.body(), type, self.get_router())
                return result
            return self.decoder(contentType).decode(self, type)
        except Exception as e:
            # TODO
            raise SneakyThrows.propogate(e)

    def decoder(self, contentType: MediaType) -> MessageDecoder:
        return self.get_route().decoder(contentType)

    def set_response_header(self, name: str, value: datetime) -> Context:
        return self.set_response_header(name, value)

    def set_response_type(self, contentType: MediaType) -> Context:
        return self.set_response_type(contentType, contentType.get_charset())

    def set_response_code(self, statusCode: StatusCode) -> Context:
        return self.set_response_code(statusCode.value())
    
    def render(self, value: object) -> Context:
        try:
            route = self.get_route()
            encoder = route.get_encoder()
            bytes = encoder.encode(self, value)
            if bytes is None:
                if not self.is_response_started():
                    raise Exception
                else:
                    self.send(bytes)
            return self
        except Exception as e:
            raise SneakyThrows.propogate(e)
    
    @dispatch(MediaType)
    def response_stream(self, contentType: MediaType) -> object:
        # TODO: return type: Java OutputStream
        self.set_response_type(contentType)
        return self.response_stream()

    @dispatch(MediaType, object)
    def response_stream(self, contentType: MediaType, consumer: object) -> Context:
        self.set_response_type(contentType)
        return self.response_stream(consumer)

    def response_stream(self, consumer: object) -> Context:
        try:
            out = self.response_stream()
            consumer.accept(out)
        except:
            pass
        return self

    @dispatch()
    def response_writer(self):
        return self.response_writer(MediaType.text)

    @dispatch(MediaType)
    def response_writer(self, contentType: MediaType):
        return self.response_writer(MediaType.text, contentType.get_charset())

    @dispatch(MediaType, object)
    def response_writer(self, contentType: MediaType, consumer: object) -> Context:
        return self.response_writer(MediaType.text, consumer)

    @dispatch(Charset, object)
    def response_writer (self, contentType: MediaType, consumer: object) -> Context:
        return self.response_writer(contentType, contentType.get_charset(), consumer)

    @dispatch(MediaType, object)
    def response_writer (self, contentType: MediaType, charset: object,
        consumer: object) -> Context:
        try:
            writer = self.response_writer(contentType, charset)
            consumer.accept(writer)
        except:
            pass
        return self

    def send_redirect(self, location):
        return self.send_redirect(StatusCode.FOUND, location)

    def send_redirect(self, redirect, location):
        Context.set_response_header("location", location)
        return self.send(redirect)

    @dispatch(list)
    def send(self, data):
        buffer = ByteBuffer.allocate(len(data))
        for i in len(data):
            buffer[i] = ByteBuffer.wrap(data[i])

        return self.send(buffer)

    @dispatch(str)
    def send(self, data):
        return self.send(data, "UTF-8")

    def send(self, file):
        Context.set_response_header("Content-Disposition", file.get_content_disposition)
        content = file.stream()
        length = file.get_file_size()
        if length > 0:
            Context.set_response_length(length)
        Context.set_response_type(file.get_content_type)
        if content is FileInputStream:
            Context.send(content.get_channel())
        else:
            Context.send(content)

        return self

    def send_error(self, cause):
        Context.send_error(cause, Context.get_router().error_code(cause))
        return self

    def send_error(self, cause, code):
        router = Context.get_router()
        log = router.get_log()
        if Context.is_response_started():
            log.error(ErrorHandler.errorMessage(self, code), cause)
        else:
            try:
                if Context.get_reset_headers_on_error():
                    Context.remove_response_header()

                Context.set_response_code(code)
                router.get_error_handler().apply(self, cause, code)
            except Exception as x:
                if not Context.is_response_started():
                    ErrorHandler.create().apply(self, cause, code)

                if Server.connection_lost(x):
                    log.debug("error handler resulted in a exception while processing" + cause + x)
                else:
                    log.error("error handler resulted in a exception while processing " + cause + x)

        if SneakyThrows.isFatal(cause):
            raise SneakyThrows.propagate(cause)

        return self