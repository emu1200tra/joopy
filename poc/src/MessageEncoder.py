from abc import abstractmethod, ABC

class MessageEncoder(ABC):

    @abstractmethod
    def encode(self) -> bytearray:
        pass

    def accept(self, contentType: MediaType) -> MessageEncoder:
        return lambda ctx, value: self.encode(ctx, value) \
            if ctx.accept(contentType) else None

class ToStringMessageEncoder(MessageEncoder):
    # To string renderer

    def encode(self, ctx: Context, value: object) -> bytearray:
        if ctx.accept(ctx.getResponseType()):
            return value.toString().encode('utf-8')
        # TODO: NotAcceptableException(ctx.header("Accept").valueOrNull())
        raise Exception