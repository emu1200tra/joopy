from flashMap import flashMap
from context import context
from cookie import cookie
from multipledispatch import dispatch

class flashMapImpl(flashMap):
    def __init__(self, ctx: context, template: cookie):
        super().__init__()
        cookieInstance = ctx.cookie(template.getName())
        if cookieInstance.isMissing():
            self.seed = {}
        else:
            self.seed = decode(cookieInstance.value())
        self.__map__ = dict(self.seed)
        self.__ctx = ctx
        self.__template = template
        self.__initialScope = dict(self.seed)
        if len(self.seed) > 0:
            self.syncCookie()

    def keep(self) -> flashMap:
        if (self.__map__) > 0:
            cookieTemp = self.__template.copy().setValue(cookie.encode(self))
            self.__ctx.setResponseCookie(cookieTemp)
        return self

    def toCookie(self) -> cookie:
        # 1. no change detect
        if self.__map__ == self.__initialScope:
            # 1.a. existing data available, discard
            if len(self.__map__) > 0:
                return self.__template.copy().setMaxAge(0)
        # 2. change detected
        else:
            # 2.a everything was removed from app logic
            if len(self.__map__) == 0:
                return self.__template.copy().setMaxAge(0)
            # 2.b there is something to see in the next request
            else:
                return self.__template.copy().setValue(cookie.encode(self))
        return None

    def syncCookie(self):
        cookieTemp = self.toCookie()
        if cookieTemp != None:
            self.__ctx.setResponseCookie(cookieTemp)
    
    # unknown remappingFunction type
    def compute(self, key: str, remappingFunction) -> str:
        pass
    def computeIfAbsent(self, key: str, remappingFunction) -> str:
        pass
    def computeIfPresent(self, key: str, remappingFunction) -> str:
        pass
    def merge(self, key: str, value: str, remappingFunction) -> str:
        pass

    def put(self, key: str, value: str) -> str:
        if key in self.__map__:
            result = self.__map__[key]
        else:
            result = None
        self.__map__[key] = value
        return result
    
    def putIfAbsent(self, key: str, value: str) -> str:
        if key in self.__map__:
            return self.__map__[key]
        self.__map__[key] = value
        return None
    
    def putAll(self, m: {str: str}):
        self.__map__ = dict(m)
        self.syncCookie()
    
    @dispatch(object, object)
    def remove(self, key: object, value: object) -> bool:
        if key in self.__map__ and self.__map__[key] == value:
            del self.__map__[key]
            self.syncCookie()
            return True
        return False
    
    @dispatch(object)
    def remove(self, key: object) -> str:
        if key in self.__map__:
            result = self.__map__[key]
            del self.__map__[key]
        else:
            result = None
        self.syncCookie()
        return result

    @dispatch(str, str, str)
    def replace(self, key: str, oldValue: str, newValue: str) -> bool:
        if key in self.__map__ and self.__map__[key] == oldValue:
            self.__map__[key] = newValue
            self.syncCookie()
            return True
        return False
    
    @dispatch(str, str)
    def replace(self, key: str, value: str) -> str:
        if key in self.__map__:
            result = self.__map__[key]
            self.__map__[key] = value
        else:
            result = None
        self.syncCookie()
        return result
    
    # unknown function type
    def replaceAll(self, function):
        pass