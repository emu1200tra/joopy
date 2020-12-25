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
        context.set_route(self.__route)
        try:
            self.__route.get_pipeline().apply(context)
        except Exception as e:
            context.send_error(e)

    def pathMap(self) -> Dict[str, str]:
        return {}