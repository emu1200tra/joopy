from abc import abstractmethod
from context import context
from cookie import cookie
from flashMapImpl import flashMapImpl

class flashMap(object):
    """
    Flash map attribute.
    """
    NAME = 'flash'

    def __init__(self):
        self.__map__ = {}

    @staticmethod
    def create(ctx: context, template: cookie) -> flashMap:
        """
        Creates a new flash-scope using the given cookie.
   
        @param ctx Web context.
        @param template Cookie template.
        @return A new flash map.
        """
        return flashMapImpl(context, template)

    @abstractmethod
    def keep(self) -> flashMap:
        """
        Keep flash cookie for next request.
   
        @return This flash map.
        """
        pass