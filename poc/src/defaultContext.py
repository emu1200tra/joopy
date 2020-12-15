from multipledispatch import dispatch

from poc.src.context import Context


class ServiceKey(object):
    pass


class FlashMap(object):
    pass


class Value(object):
    pass


class Session(object):
    pass


class MissingValue(object):
    pass


class SingleValue(object):
    pass


class UrlParser(object):
    pass


class HashValue(object):
    pass


class MediaType(object):
    pass


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

    def flash(self):
        return Context.get_attributes().computeIfAbsent(FlashMap.NAME, lambda key: FlashMap.create(self,
                                                                                                   Context.get_router().getFlashCookie().clone()))

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

    def sessionOrNull(self):
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

