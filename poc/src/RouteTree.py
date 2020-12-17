from .Route import Route
from .Router import Router
from abc import abstractmethod, ABC

class RouteTree(ABC):
    @abstractmethod
    def insert(self, method: str, pattern: str, route: Route):
        pass

    @abstractmethod
    def exists(self, method: str, path: str) -> bool:
        pass

    @abstractmethod
    def find(self, method: str, path: str) -> Router.Match:
        pass
    
    @abstractmethod
    def destroy(self):
        pass