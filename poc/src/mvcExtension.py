from abc import staticmethod
import mvcFactory
import myController

class mvcExtension(mvcFactory):
    @staticmethod
    def install(self, application, provider):
        # an exception occurs!
        application.get("/mypath", lambda cxt: \
            myController = provider.get()
            myController.controllerMethod()
            return myController).attribute("RequireRole", Controller1527.Role.USER)
        return 

    def supports(self, classType):
        return classType == myController

    def create(self, provider):
        # provider -> controller instance, need to refactor
        return lambda app: self.install(app, provider)