from src.todo import ServiceKey
from multipledispatch import dispatch
from abc import abstractmethod, ABCMeta

class Registry(object):
    '''
    * Provides an instance of the given type.
    *
    * @param type Object type.
    * @param <T> Object type.
    * @return Instance of this type.
    * @throws RegistryException If there was a runtime failure while providing an instance.
    '''
    @dispatch(object)
    @abstractmethod
    def require(self, _type):
        pass

    '''
    * Provides an instance of the given type where name matches it.
    *
    * @param type Object type.
    * @param name Object name.
    * @param <T> Object type.
    * @return Instance of this type.
    * @throws RegistryException If there was a runtime failure while providing an instance.
    '''
    @dispatch(object, str)
    @abstractmethod
    def require(self, _type, name):
        pass

    '''
    * Provides an instance of the given type.
    *
    * @param key Object key.
    * @param <T> Object type.
    * @return Instance of this type.
    * @throws RegistryException If there was a runtime failure while providing an instance.
    '''
    @dispatch(ServiceKey)
    @abstractmethod
    def require(self, key):
        pass