from abc import abstractmethod, staticmethod
from multipledispatch import dispatch
from context import context
from instant import instant
from value import value
from sessionImpl import sessionImpl

class session():
    NAME = 'session'
    
    @abstractmethod
    def getId(self):
        """
        Session ID or <code>null</code> for stateless (usually signed) sessions.
   
        @return Session ID or <code>null</code> for stateless (usually signed) sessions.
        """
        pass

    @abstractmethod
    def setId(self, id: str):
        """
        Set Session ID.
   
        @param id Session ID or <code>null</code>
        @return Session.
        """
        pass

    @abstractmethod
    def get(self, name: str) -> value:
        """
        Get a session attribute.
   
        @param name Attribute's name.
        @return An attribute value or missing value.
        """
        pass
    
    @abstractmethod
    @dispatch(str, str)
    def put(self, name: str, value: str):
        """
        Put a session attribute.
   
        @param name Attribute's name.
        @param value Attribute's value.
        @return This session.
        """
        pass
    
    @dispatch(str, int)
    def put(self, name: str, value: int) -> session:
        return self.put(name, str(value))
    
    @dispatch(str, float)
    def put(self, name: str, value: float) -> session:
        return self.put(name, str(value))

    @dispatch(str, bool)
    def put(self, name: str, value: bool) -> session:
        return self.put(name, str(value))

    @abstractmethod
    def remove(self, name: str) -> value:
        """
        Remove a session attribute.
   
        @param name Attribute's name.
        @return Session attribute or missing value.
        """
        pass
    
    @abstractmethod
    def toMap(self) -> {str: str}:
        """
        Read-only copy of session attributes.
   
        @return Read-only attributes.
        """
        pass

    @abstractmethod
    def getCreationTime(self) -> instant:
        """
        Session creation time.
   
        @return Session creation time.
        """
        pass
    
    @abstractmethod
    def setCreationTime(self, creationTime: instant) -> session:
        """
        Set session creation time.
   
        @param creationTime Session creation time.
        @return This session.
        """
        pass

    @abstractmethod
    def getLastAccessedTime(self) -> instant:
        """
        Session last accessed time.
   
        @return Session creation time.
        """
        pass

    @abstractmethod
    def setLastAccessedTime(self, setLastAccessedTime: instant) -> session:
        """
        Set session last accessed time.
   
        @param lastAccessedTime Session creation time.
        @return This session.
        """
        pass
    
    @abstractmethod
    def isNew(self) -> bool:
        """
        True for new sessions.
   
        @return True for new sessions.
        """
        pass
    
    @abstractmethod
    def setNew(self, isNew: bool) -> session:
        """
        Set new flag. This method is part of public API but shouldn't be use it.
   
        @param isNew New flag.
        @return This session.
        """
        pass
    
    @abstractmethod
    def isModify(self) -> bool:
        """
        True for modified/dirty sessions.
   
        @return True for modified/dirty sessions.
        """
        pass

    @abstractmethod
    def setModify(self, isModify: bool) -> session:
        """
        Set modify flag. This method is part of public API but shouldn't be use it.
   
        @param modify Modify flag.
        @return This session.
        """
        pass

    @abstractmethod
    def clear(self) -> session:
        """
        Remove all attributes.
   
        @return This session.
        """
        pass

    @abstractmethod
    def destroy(self):
        """
        Destroy/invalidates this session.
        """
        pass

    @abstractmethod
    def renewId(self) -> session:
        """
        Assign a new ID to the existing session.
        @return This session.
        """
        pass

    @staticmethod
    @dispatch(context, str)
    def create(self, ctx: context, idx: str) -> session:
        """
        Creates a new session.
   
        @param ctx Web context.
        @param id Session ID or <code>null</code>.
        @return A new session.
        """
        return sessionImpl(ctx, idx)

    @staticmethod
    @dispatch(context, str, {str: str})
    def create(self, ctx: context, idx: str, data: {str: str}) -> session:
        """
        Creates a new session.
   
        @param ctx Web context.
        @param id Session ID or <code>null</code>.
        @param data Session attributes.
        @return A new session.
        """
        return sessionImpl(ctx, idx, data)