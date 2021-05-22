from session import session
from context import context
from value import value
from instant import instant
from sessionStore import sessionStore
from valueNode import valueNode
from multipledispatch import dispatch

class sessionImpl(session):
    @dispatch(context, str, {str: str})
    def __init__(self, ctx: context, idx: str, attributes: {str: str}):
        self.__ctx = ctx
        self.__idx = idx
        self.__attributes = attributes

        self.__isNew = True
        self.__modify = False
        self.__lastAccessedTime = instant.now()
        self.__creationTime = instant.now()
    
    @dispatch(context, str)
    def __init__(self, ctx: context, idx: str):
        self.__init__(ctx, idx, {})

    def isNew(self) -> bool:
        return self.__isNew

    def setNew(self, aNew: bool) -> session:
        self.__isNew = aNew
        return self

    def isModify(self) -> bool:
        return self.__modify

    def setModify(self, modify: bool) -> session:
        self.__modify = modify
        return self
    
    def getId(self) -> str:
        return self.__idx
    
    def setId(self, idx: str) -> session:
        self.__idx = idx
        return self
    
    def get(self, name: str) -> value:
        return value.create(self.__ctx, name, self.__attributes.get(name))
    
    @staticmethod
    def store(ctx: context) -> sessionStore:
        return ctx.getRouter().getSessionStore()

    def updateState(self):
        self.__modify = True
        self.__lastAccessedTime = instant.now()
        sessionImpl.store(self.__ctx).touchSession(self.__ctx, self)

    def put(self, name: str, value: str) -> session:
        self.__attributes[name] = value
        self.updateState()
        return self

    def remove(self, name: str) -> valueNode:
        v = None
        if name in self.__attributes:
            v = self.__attributes[name]
            del self.__attributes[name]
            
        self.updateState()
        if v == None:
            value.missing(name)
        else:
            value.value(self.__ctx, name, v)

    def toMap(self) -> {str: str}:
        return self.__attributes

    def getCreationTime(self) -> instant:
        return self.__creationTime

    def setCreationTime(self, creationTime: instant) -> session:
        self.__creationTime = creationTime
        return self

    def getLastAccessedTime(self) -> instant:
        return self.__lastAccessedTime
    
    def setLastAccessedTime(self, lastAccessedTime: instant) -> session:
        self.__lastAccessedTime = lastAccessedTime
        return self

    def clear(self) -> session:
        self.__attributes.clear()
        self.updateState()
        return self
    
    def destroy(self):
        del self.__ctx.getAttributes[session.NAME]
        self.__attributes.cleart()

    def renewId(self):
        type(self).store(self.__ctx).deleteSession(self.__ctx, self)
        self.updateState()
        return self
