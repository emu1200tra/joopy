from .defaultContext import Context
from .Route import Route
from .Router import Router
from typing import Dict

class StaticRouterMatch(Router.Match):
    def __init__(self, route: Route):
        self.__route = route;

    def matches(self) -> bool:
        return True

    def route(self) -> Route:
        return self.__route

    def execute(self, context: Context):
        context.setRoute(self.__route)
        try:
            self.__route.getPipeline().apply(context)
        except Exception as e:
            context.sendError(e)

    def pathMap(self) -> Dict[str, str]:
        return {}