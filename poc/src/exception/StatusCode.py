from StatusCodeBase import StatusCodeBase
from final_class import final


"""
We want class level access to different statuscode
We also want the code to be static, final, not being able to edit
so we created a class code, pass in its .code to prevent modification

"""

@final
class StatusCode:
    """
    1xx Informational

    """
    CONTINUE_CODE = 100
    CONTINUE = StatusCodeBase(
        CONTINUE_CODE,
        "Continue"
    )

    SWITCHING_PROTOCOLS_CODE = 101
    SWITCHING_PROTOCOLS = StatusCodeBase(
        SWITCHING_PROTOCOLS_CODE,
        "Switching Protocols"
    )

    PROCESSING_CODE = 102
    PROCESSING = StatusCodeBase(
        PROCESSING_CODE,
        "Processing"
    )

    CHECKPOINT_CODE = 103
    CHECKPOINT = StatusCodeBase(
        CHECKPOINT_CODE,
        "Checkpoint"
    )

    """
    2xx Success

    """

    OK_CODE = 200
    OK = StatusCodeBase(
        OK_CODE,
        "Success"
    )

    CREATED_CODE = 201
    CREATED = StatusCodeBase(
        CREATED_CODE,
        "Created"
    )

    ACCEPTED_CODE = 202
    ACCEPTED = StatusCodeBase(
        ACCEPTED_CODE,
        "Accepted"
    )

    NON_AUTHORITATIVE_INFORMATION_CODE = 203
    NON_AUTHORITATIVE_INFORMATION = StatusCodeBase(
        NON_AUTHORITATIVE_INFORMATION_CODE,
        "Non-Authoritative Information"
    )

    NO_CONTENT_CODE = 204
    NO_CONTENT = StatusCodeBase(
        NO_CONTENT_CODE,
        "No Content"
    )

    RESET_CONTENT_CODE = 205
    RESET_CONTENT = StatusCodeBase(
        RESET_CONTENT_CODE,
        "Reset Content"
    )

    PARTIAL_CONTENT_CODE = 206
    PARTIAL_CONTENT = StatusCodeBase(
        PARTIAL_CONTENT_CODE,
        "Partial Content"
    )

    MULTI_STATUS_CODE = 207
    MULTI_STATUS = StatusCodeBase(
        MULTI_STATUS_CODE,
        "Multi-StatusCode"
    )

    ALREADY_REPORTED_CODE = 208
    ALREADY_REPORTED = StatusCodeBase(
        ALREADY_REPORTED_CODE,
        "Already Reported"
    )

    IM_USED_CODE = 226
    IM_USED = StatusCodeBase(
        IM_USED_CODE,
        "IM Used"
    )

    """
    3xx Rediction

    """

    MULTIPLE_CHOICES_CODE = 300
    MULTIPLE_CHOICES = StatusCodeBase(
        MULTIPLE_CHOICES_CODE,
        "Multiple Choices"
    )

    MOVED_PERMANENTLY_CODE = 301
    MOVED_PERMANENTLY = StatusCodeBase(
        MOVED_PERMANENTLY_CODE,
        "Moved Permanently"
    )

    FOUND_CODE = 302
    FOUND = StatusCodeBase(
        FOUND_CODE,
        "Found"
    )

    SEE_OTHER_CODE = 303
    SEE_OTHER = StatusCodeBase(
        SEE_OTHER_CODE,
        "See Other"
    )

    NOT_MODIFIED_CODE = 304
    NOT_MODIFIED = StatusCodeBase(
        NOT_MODIFIED_CODE,
        "Not Modified"
    )

    USE_PROXY_CODE = 305
    USE_PROXY = StatusCodeBase(
        USE_PROXY_CODE,
        "Use Proxy"
    )

    TEMPORARY_REDIRECT_CODE = 307
    TEMPORARY_REDIRECT = StatusCodeBase(
        TEMPORARY_REDIRECT_CODE,
        "Temporary Redirect"
    )

    RESUME_INCOMPLETE_CODE = 308
    RESUME_INCOMPLETE = StatusCodeBase(
        RESUME_INCOMPLETE_CODE,
        "Resume Incomplete"
    )

    """
    4xx Client Error

    """

    BAD_REQUEST_CODE = 400
    BAD_REQUEST = StatusCodeBase(
        BAD_REQUEST_CODE,
        "Bad Request"
    )

    UNAUTHORIZED_CODE = 401
    UNAUTHORIZED = StatusCodeBase(
        UNAUTHORIZED_CODE,
        "Unauthorized"
    )

    PAYMENT_REQUIRED_CODE = 402
    PAYMENT_REQUIRED = StatusCodeBase(
        PAYMENT_REQUIRED_CODE,
        "Payment Required"
    )

    FORBIDDEN_CODE = 403
    FORBIDDEN = StatusCodeBase(
        FORBIDDEN_CODE,
        "Forbidden"
    )

    NOT_FOUND_CODE = 404
    NOT_FOUND = StatusCodeBase(
        NOT_FOUND_CODE,
        "Not Found"
    )

    METHOD_NOT_ALLOWED_CODE = 405
    METHOD_NOT_ALLOWED = StatusCodeBase(
        METHOD_NOT_ALLOWED_CODE,
        "Method Not Allowed"
    )

    NOT_ACCEPTABLE_CODE = 406
    NOT_ACCEPTABLE = StatusCodeBase(
        NOT_ACCEPTABLE_CODE,
        "Not Acceptable"
    )

    PROXY_AUTHENTICATION_REQUIRED_CODE = 407
    PROXY_AUTHENTICATION_REQUIRED = StatusCodeBase(
        PROXY_AUTHENTICATION_REQUIRED_CODE,
        "Proxy Authentication Required"
    )

    REQUEST_TIMEOUT_CODE = 408
    REQUEST_TIMEOUT = StatusCodeBase(
        REQUEST_TIMEOUT_CODE,
        "Request Timeout"
    )

    CONFLICT_CODE = 409
    CONFLICT = StatusCodeBase(
        CONFLICT_CODE,
        "Conflict"
    )

    GONE_CODE = 410
    GONE = StatusCodeBase(
        GONE_CODE,
        "Gone"
    )

    LENGTH_REQUIRED_CODE = 411
    LENGTH_REQUIRED = StatusCodeBase(
        LENGTH_REQUIRED_CODE,
        "Length Required"
    )

    PRECONDITION_FAILED_CODE = 412
    PRECONDITION_FAILED = StatusCodeBase(
        PRECONDITION_FAILED_CODE,
        "Precondition Failed"
    )

    REQUEST_ENTITY_TOO_LARGE_CODE = 413
    REQUEST_ENTITY_TOO_LARGE = StatusCodeBase(
        REQUEST_ENTITY_TOO_LARGE_CODE,
        "Request Entity Too Large"
    )

    REQUEST_URI_TOO_LONG_CODE = 414
    REQUEST_URI_TOO_LONG = StatusCodeBase(
        REQUEST_URI_TOO_LONG_CODE,
        "Request-URI Too Long"
    )

    UNSUPPORTED_MEDIA_TYPE_CODE = 415
    UNSUPPORTED_MEDIA_TYPE = StatusCodeBase(
        UNSUPPORTED_MEDIA_TYPE_CODE,
        "Unsupported Media Type"
    )

    REQUESTED_RANGE_NOT_SATISFIABLE_CODE = 416
    REQUESTED_RANGE_NOT_SATISFIABLE = StatusCodeBase(
        REQUESTED_RANGE_NOT_SATISFIABLE_CODE,
        "Requested range not satisfiable"
    )

    EXPECTATION_FAILED_CODE = 417
    EXPECTATION_FAILED = StatusCodeBase(
        EXPECTATION_FAILED_CODE,
        "Expectation Failed"
    )

    I_AM_A_TEAPOT_CODE = 418
    I_AM_A_TEAPOT = StatusCodeBase(
        I_AM_A_TEAPOT_CODE,
        "I'm a teapot"
    )

    UNPROCESSABLE_ENTITY_CODE = 422
    UNPROCESSABLE_ENTITY = StatusCodeBase(
        UNPROCESSABLE_ENTITY_CODE,
        "Unprocessable Entity"
    )

    LOCKED_CODE = 423
    LOCKED = StatusCodeBase(
        LOCKED_CODE,
        "Locked"
    )

    FAILED_DEPENDENCY_CODE = 424
    FAILED_DEPENDENCY = StatusCodeBase(
        FAILED_DEPENDENCY_CODE,
        "Failed Dependency"
    )

    UPGRADE_REQUIRED_CODE = 426
    UPGRADE_REQUIRED = StatusCodeBase(
        UPGRADE_REQUIRED_CODE,
        "Upgrade Required"
    )

    PRECONDITION_REQUIRED_CODE = 428
    PRECONDITION_REQUIRED = StatusCodeBase(
        PRECONDITION_REQUIRED_CODE,
        "Precondition Required"
    )

    TOO_MANY_REQUESTS_CODE = 429
    TOO_MANY_REQUESTS = StatusCodeBase(
        TOO_MANY_REQUESTS_CODE,
        "Too Many Requests"
    )

    REQUEST_HEADER_FIELDS_TOO_LARGE_CODE = 431
    REQUEST_HEADER_FIELDS_TOO_LARGE = StatusCodeBase(
        REQUEST_HEADER_FIELDS_TOO_LARGE_CODE,
        "Request Header Fields Too Large"
    )

    """
    5xx Server Error

    """

    SERVER_ERROR_CODE = 500
    SERVER_ERROR = StatusCodeBase(
        SERVER_ERROR_CODE,
        "Server Error"
    )

    NOT_IMPLEMENTED_CODE = 501
    NOT_IMPLEMENTED = StatusCodeBase(
        NOT_IMPLEMENTED_CODE,
        "Not Implemented"
    )

    BAD_GATEWAY_CODE = 502
    BAD_GATEWAY = StatusCodeBase(
        BAD_GATEWAY_CODE,
        "Bad Gateway"
    )

    SERVICE_UNAVAILABLE_CODE = 503
    SERVICE_UNAVAILABLE = StatusCodeBase(
        SERVICE_UNAVAILABLE_CODE,
        "Service Unavailable"
    )

    GATEWAY_TIMEOUT_CODE = 504
    GATEWAY_TIMEOUT = StatusCodeBase(
        GATEWAY_TIMEOUT_CODE,
        "Gateway Timeout"
    )

    HTTP_VERSION_NOT_SUPPORTED_CODE = 505
    HTTP_VERSION_NOT_SUPPORTED = StatusCodeBase(
        HTTP_VERSION_NOT_SUPPORTED_CODE,
        "HTTP Version not supported"
    )

    VARIANT_ALSO_NEGOTIATES_CODE = 506
    VARIANT_ALSO_NEGOTIATES = StatusCodeBase(
        VARIANT_ALSO_NEGOTIATES_CODE,
        "Variant Also Negotiates"
    )

    INSUFFICIENT_STORAGE_CODE = 507
    INSUFFICIENT_STORAGE = StatusCodeBase(
        INSUFFICIENT_STORAGE_CODE,
        "Insufficient Storage"
    )

    LOOP_DETECTED_CODE = 508
    LOOP_DETECTED = StatusCodeBase(
        LOOP_DETECTED_CODE,
        "Loop Detected"
    )

    BANDWIDTH_LIMIT_EXCEEDED_CODE = 509
    BANDWIDTH_LIMIT_EXCEEDED = StatusCodeBase(
        BANDWIDTH_LIMIT_EXCEEDED_CODE,
        "Bandwidth Limit Exceeded"
    )

    NOT_EXTENDED_CODE = 510
    NOT_EXTENDED = StatusCodeBase(
        NOT_EXTENDED_CODE,
        "Not Extended"
    )

    NETWORK_AUTHENTICATION_REQUIRED_CODE = 511
    NETWORK_AUTHENTICATION_REQUIRED = StatusCodeBase(
        NETWORK_AUTHENTICATION_REQUIRED_CODE,
        "Network Authentication Required"
    )

    def __init__(self, value, reason):
        self.__value = value
        self.__reason = reason

    def value(self):
        return self.__value

    def reason(self):
        return self.__reason
    
    def valueOf(self, statusCode):
        if statusCode == CONTINUE_CODE:
            return CONTINUE
        elif statusCode == SWITCHING_PROTOCOLS_CODE:
            return SWITCHING_PROTOCOLS


def main():
    print(StatusCode.NETWORK_AUTHENTICATION_REQUIRED_CODE)
    print(StatusCode.NETWORK_AUTHENTICATION_REQUIRED)
    print(StatusCode.NETWORK_AUTHENTICATION_REQUIRED.reason())
    print(StatusCode.I_AM_A_TEAPOT_CODE)
    import ipdb; ipdb.set_trace()


if __name__ == "__main__":
    main()

    