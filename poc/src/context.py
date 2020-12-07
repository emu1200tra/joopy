from poc.src.Registry import Registry


class Context(Registry):
    def __init__(self):
        self.port = 80
        self.secure_port = 443
        self.accept = "Accept"

        # RFC1123 DatetimeFormatter not implemented

    def get_attributes(self) -> dict:
        pass

    def attribute(self, key: str, value: object = None) -> object:
        pass

    def get_router(self):
        pass

    def forward(self, path: str):
        pass

    def convert(self, value, class_type):
        pass

    def flash(self, name):
        pass

    def session(self, name: str = None):
        pass

    def cookie(self, name):
        pass

    def cookie_map(self):
        pass

    def get_method(self):
        pass

    def set_method(self, method: str):
        pass

    def get_route(self):
        pass

    def matches(self, pattern: str):
        pass

    def set_route(self, route):
        pass

    def get_context_path(self):
        return self.get_router().get_context_path()

    def get_request_path(self):
        pass

    def set_request_path(self, path: str):
        pass

    def path(self, name: str = None):
        pass

    def path(self, class_type):
        pass

    def path_map(self):
        pass

    def set_path_map(self, path_map: dict):
        pass

    def query(self, name: str = None):
        pass

    def query(self, class_type):
        pass

    def query_string(self):
        pass

    def query_map(self):
        pass

    def query_multimap(self):
        pass

    def header(self, name: str = None):
        pass

    def header_map(self):
        pass

    def header_multimap(self):
        pass

    def accept(self, content_type):
        pass

    def accept(self, produce_types):
        pass

    def get_request_type(self, defaults=None):
        pass

    def get_request_length(self):
        pass



