from abc import staticmethod
import mvcFactory
import myController

class mvcExtension(mvcFactory):
    @staticmethod
    def install(application, provider):
        # an exception occurs!
        def f(ctx, provider):
            myController = provider.get()
            myController.controllerMethod()
            return ctx

        application.get("/mypath", lambda cxt: f(ctx, provider)).attribute("RequireRole", Controller1527.Role.USER)

    def supports(self, classType):
        return classType == myController

    def create(self, provider):
        # provider -> controller instance, need to refactor
        return lambda app: self.install(app, provider)