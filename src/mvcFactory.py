from abc import abstractmethod 

class mvcFactory:
    @abstractmethod
    def supports(self, classType):
        """
        Check if the factory applies for the given MVC route.
   
        @param type MVC route.
        @return True for matching factory.
        """
        pass
    
    @abstractmethod
    def create(self, provider):
        """
        Creates an extension module. The extension module are created at compilation time by Jooby
        APT.
   
        @param provider MVC route instance provider.
        @return All mvc route as extension module.
        """
        pass