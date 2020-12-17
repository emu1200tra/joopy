from multipledispatch import dispatch
from abc import abstractmethod, ABC
class MessageEncoder(ABC):

    @abstractmethod
    def encode(self) -> bytearray:
        pass

    def accept(self, contentType: MediaType) -> MessageEncoder:
        return lambda ctx, value: self.encode(ctx, value) \
            if ctx.accept(contentType) else None
    
    @classmethod
    def to_string(cls, ctx: Context, value: int):
        if ctx.accept(ctx.get_response_type()):
            return str.encode(str(value)) # default encode to bytes in utf-8 format
        raise Exception('NotAcceptableException' + ctx.header('Accept'))
    
    # MessageEncoder
    TO_STRING = lambda ctx, value : MessageEncoder.to_string(ctx, value)

class ToStringMessageEncoder(MessageEncoder):
    # To string renderer

    def encode(self, ctx: Context, value: object) -> bytearray:
        if ctx.accept(ctx.getResponseType()):
            return value.toString().encode('utf-8')
        # TODO: NotAcceptableException(ctx.header("Accept").valueOrNull())
        raise Exception

class HttpMessageEncoder(MessageEncoder):
    pass