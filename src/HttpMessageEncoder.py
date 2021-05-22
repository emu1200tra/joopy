from numbers import Number

from .todo import *
from .exception.StatusCode import StatusCode
from .MessageEncoder import MessageEncoder
from .context import Context

class HttpMessageEncoder(MessageEncoder):
    def __init__(self):
        self.__encoderList = [] # List<MessageEncoder> # new ArrayList<>(2)
        self.__templateEngineList = [] # List<TemplateEngine> # new ArrayList<>(2)

    def add(self, encoder: MessageEncoder):
        if isinstance(encoder, TemplateEngine):
            self.__templateEngineList.append(encoder)
        else:
            self.__encoderList.append(encoder)
        return self

    def encode(self, ctx: Context, value: object) -> bytearray:
        if isinstance(value, ModelAndView):
            modelAndView = value # ModelAndView
            for engine in self.__templateEngineList:
                if engine.supports(modelAndView):
                    return engine.encode(ctx, modelAndView)
            raise Exception("No template engine for: " + modelAndView.getView())

        """ InputStream: """
        if isinstance(value, InputStream):
            ctx.send(value)
            return None
        """ StatusCode: """
        if isinstance(value, StatusCode):
            ctx.send(value)
            return None
        """ FileChannel: """
        if isinstance(value, FileChannel):
            ctx.send(value)
            return None
        if isinstance(value, File):
            ctx.send(value.toPath())
            return None
        if isinstance(value, Path):
            ctx.send(value)
            return None
        """ FileDownload: """
        if isinstance(value, FileDownload):
            ctx.send(value)
            return None
        """ Strings: """
        if isinstance(value, str):
            return value.toString().encode('utf-8')
        if isinstance(value, Number):
            return value.toString().encode('utf-8')
        """ RawByte: """
        if isinstance(value, bytearray):
            return value
        """
        if (value instanceof ByteBuffer) {
        ctx.send((ByteBuffer) value);
        return null;
        }
        """

        it = iter(self.__encoderList)
        """ NOTE: looks like an infinite loop but there is a default renderer at the end of iterator. """
        result = None
        while result is None:
            result = next(it).encode(ctx, value)

        return result
