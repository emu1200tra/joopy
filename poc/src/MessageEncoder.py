from .MediaType import MediaType
from .context import Context

class MessageEncoder():
    class ToStringMessageEncoder():
        # To string renderer
        def encode(self, ctx: Context, value: object) -> bytearray:
            if ctx.accept(ctx.get_response_type()):
                return value.toString().encode('utf-8')
            raise Exception('NotAcceptableException' + ctx.header("Accept"))

        def accept(self, contentType: MediaType):
            return MessageEncoder.accept(self, contentType)

    TO_STRING = ToStringMessageEncoder() # MessageEncoder

    def __init__(self, func):
        self.__func = func

    def encode(self, ctx: Context, value: object) -> bytearray:
        self.__func(ctx, value)

    def accept(self, contentType: MediaType):
        func = lambda ctx, value: self.encode(ctx, value) if ctx.accept(contentType) else None
        return MessageEncoder(func)
