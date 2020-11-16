from wsgiref.util import setup_testing_defaults, guess_scheme, request_uri
from wsgiref.simple_server import make_server

routes = ()


def setup_wsgi(environ, start_response):
    response_status = '200 OK'
    # content-type 應該由 route 決定, 暫時先 hard code
    headers = [('Content-type', 'text/plain')]

    start_response(response_status, headers)

    uri = environ['PATH_INFO']
    # method = environ['REQUEST_METHOD']

    return [routes[uri][1]()]


def start(rs):
    # 不應該用 global, 但不知道怎麼 pass 給 setup_wsgi 使用
    global routes
    routes = rs
    httpd = make_server('', 8000, setup_wsgi)
    print("serving http on port 8000...")
    httpd.serve_forever()

    # setup_testing_defaults(environ)

#
# # A relatively simple WSGI application. It's going to print out the
# # environment dictionary after being updated by setup_testing_defaults
# def simple_app(environ, start_response):
#     setup_testing_defaults(environ)
#
#     status = '200 OK'
#     headers = [('Content-type', 'text/plain; charset=utf-8')]
#
#     start_response(status, headers)
#
#     print(guess_scheme(environ))
#     print(request_uri(environ))
#
#     geturl = environ['PATH_INFO']
#     print(geturl)
#     # for item in url:
#     #     if item[0] == geturl:
#     #         return [item[1]().encode("utf-8")]
#     # else:
#     #     return '404'
#
#     ret = [("%s: %s\n" % (key, value)).encode("utf-8")
#            for key, value in environ.items()]
#
#     ret = b'hello world'
#     return [ret, ]
#
#     # return ret
#
#
# with make_server('', 8000, simple_app) as httpd:
#     print("Serving on port 8000...")
#     httpd.serve_forever()
