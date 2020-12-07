from ..Route import Decorator
class CorsHandler(Decorator):
    ORIGIN = "Origin"
    ANY_ORIGIN = "*"
    AC_REQUEST_METHOD = "Access-Control-Request-Method"
    AC_REQUEST_HEADERS = "Access-Control-Request-Headers"
    AC_MAX_AGE = "Access-Control-Max-Age"
    AC_EXPOSE_HEADERS = "Access-Control-Expose-Headers"
    AC_ALLOW_ORIGIN = "Access-Control-Allow-Origin"
    AC_ALLOW_HEADERS = "Access-Control-Allow-Headers"
    AC_ALLOW_CREDENTIALS = "Access-Control-Allow-Credentials"
    AC_ALLOW_METHODS = "Access-Control-Allow-Methods"
    def __init__(self, options):
        this.options = options
