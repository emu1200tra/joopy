from .mvcFactory import mvcFactory
from .myControllerHandler import myControllerHandler
from .Route import Route

class mvcExtension(mvcFactory):
    @staticmethod
    def install(application, provider):
        # an exception occurs!
        def f(ctx, provider):
            myController = provider()
            #myController.controllerMethod()
            return ctx

        handler = Route.Handler(lambda ctx: f(ctx, provider))
        application.get("/mypath", handler)#.attribute("RequireRole", Controller1527.Role.USER)

    def supports(self, classType):
        return classType == myController

    def create(self, provider):
        # provider -> controller instance, need to refactor
        return lambda app: self.install(app, provider)