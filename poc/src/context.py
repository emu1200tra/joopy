from poc.src.Registry import Registry


class ParamLookupImpl(object):
    def __init__(self, context):
        pass


class ReadOnlyContext(object):
    def __init__(self, context):
        pass


class WebSocketSender(object):
    def __init__(self, context, websocket):
        pass


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

    def accept_with_content_type(self, content_type):
        pass

    def accept_with_produce_types(self, produce_types):
        pass

    def get_request_type(self, defaults=None):
        pass

    def get_request_length(self):
        pass

    def locales(self):
        pass

    def locale(self):
        pass

    def get_user(self):
        pass

    def set_user(self, user: object):
        pass

    def get_request_url(self, path: str = None):
        pass

    def get_remote_address(self):
        pass

    def set_remote_address(self, remote_address: str):
        pass

    def get_host(self):
        pass

    def set_host(self, host: str):
        pass

    def get_host_and_port(self):
        pass

    def get_port(self):
        pass

    def set_port(self, port: int):
        pass

    def get_protocol(self):
        pass

    def get_server_port(self):
        pass

    def get_server_host(self):
        pass

    def is_secure(self):
        pass

    def get_scheme(self):
        pass

    def set_scheme(self, scheme: str):
        pass

    def form(self):
        pass

    def form_with_name(self, name: str):
        pass

    def form_with_type(self, form_type):
        pass

    def formMultimap(self):
        pass

    def formMap(self):
        pass

    def multipart(self):
        pass

    def multipart_with_name(self, name: str):
        pass

    def multipart_with_type(self, multipart_type):
        pass

    def multipart_multimap(self):
        pass

    def multipart_map(self):
        pass

    def files(self, name: str = None):
        pass

    def file(self, name: str):
        pass

    def lookup_with_sources(self, name, sources):
        if sources.length == 0:
            raise Exception("No parameter sources were specified")

        # return Arrays.stream(sources)
        # .map(source -> source.provider.apply(this, name))
        # .filter(value -> !value.isMissing())
        # .findFirst()
        # .orElseGet(() -> Value.missing(name));

        pass

    def lookup(self):
        return ParamLookupImpl(self)

    def body(self):
        pass

    def body_with_class_type(self):
        pass

    def body_with_refined_type(self):
        pass

    def decode(self, generic_type, content_type):
        pass

    def is_in_io_thread(self):
        pass

    def dispatch(self, executor, action):
        pass

    def detach(self, next_route_handler):
        raise Exception

    def upgrade_with_initializer(self, handler):
        pass

    def upgrade_with_server_sent_emitter_handler(self, handler):
        pass

    def set_response_header_with_date(self, name, value):
        pass

    def set_response_header_with_instant(self, name, value):
        pass

    def set_response_header_with_object(self, name, value):
        pass

    def set_response_header(self, name):
        pass

    def remove_response_header(self):
        pass

    def set_response_length(self, length):
        pass

    def get_response_header(self, name):
        pass

    def get_response_length(self):
        pass

    def set_response_cookie(self, cookie):
        pass

    def set_response_type_with_str(self, content_type):
        pass

    def set_response_type_with_media_type(self, content_type):
        pass

    def set_response_type_with_media_type_and_charset(self, content_type, charset):
        pass

    def set_default_response_type(self, content_type):
        pass

    def get_response_type(self):
        pass

    def set_response_code(self, status_code):
        pass

    def set_response_code_with_int(self, status_code):
        pass

    def get_response_code(self):
        pass

    def render(self, value):
        pass

    def response_stream(self):
        pass

    def response_stream_with_content_type(self, content_type):
        pass

    def response_stream_with_content_type_and_consumer(self, content_type, consumer):
        pass

    def response_stream_with_consumer(self):
        raise Exception

    def response_sender(self):
        pass

    def response_writer(self):
        pass

    def response_writer_with_content_type(self, content_type):
        pass

    def response_writer_with_content_Type_and_charset(self, content_type, charset):
        pass

    def response_writer_with_content_type_and_consumer(self, content_type, consumer):
        pass

    def response_writer_with_consumer(self, consumer):
        raise Exception

    def response_writer_with_content_type_and_charset_and_consumer(self, content_type, charset, consumer):
        raise Exception

    def send_redirect(self, location):
        pass

    def send_redirect_with_status_code_and_location(self, redirect, location):
        pass

    def send_with_str_data(self, data):
        pass

    def send_with_str_data_and_charset(self, data, charset):
        pass

    def send_with_byte_data(self, data):
        pass

    def send_with_byte_buffer_data(self, data):
        pass

    def send_with_byte_array_data(self, data):
        pass

    def send_with_byte_buffer_array_data(self, data):
        pass

    def send_with_readable_byte_channel(self, channel):
        pass

    def send_with_input_stream(self, input_stream):
        pass

    def send_with_file_download(self, file):
        pass

    def send_with_file_path(self, file):
        pass

    def send_with_file_channel(self, file):
        pass

    def send_with_status_code(self, status_code):
        pass

    def send_error(self, cause):
        pass

    def send_error_with_status_code(self, cause, status_code):
        pass

    def is_response_started(self):
        pass

    def get_reset_headers_on_error(self):
        pass

    def set_reset_headers_on_error(self):
        pass

    def on_complete(self, task):
        pass

    def readonly(self, ctx):
        return ReadOnlyContext(ctx)

    def websocket(self, ctx, ws):
        return WebSocketSender(ctx, ws)













