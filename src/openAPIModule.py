from enum import Enum
from extension import extension
from Router import Router

class openAPIModule(extension):
    class Format(Enum):
        JSON = 'JSON'
        YAML = 'YAML'

    def __init__(self, path='/'):
        """
        Creates an OpenAPI module. The path is used to route the open API files. For example:
   
        <pre>{@code
            install(new OpenAPIModule("/docs"));
        }</pre>
    
        Files will be at <code>/docs/openapi.json</code>, <code>/docs/openapi.yaml</code>.
    
        @param path Custom path to use.
        """

        self.__swaggerUIPath = '/swagger'
        self.__redocPath = '/redoc'
        self.__format = {self.Format.JSON, self.Format.YAML}

        # openAPIPath is const!
        self.__openAPIPath = Router.normalizePath(path)

    def swaggerUI(self, path):
        """
        Customize the swagger-ui path. Defaults is <code>/swagger</code>.
   
        @param path Swagger-ui path.
        @return This module.
        """
        self.__swaggerUIPath = Router.normalizePath(path)
        return self

    def redoc(self, path):
        """
        Customize the redoc-ui path. Defaults is <code>/redoc</code>.
   
        @param path Redoc path.
        @return This module.
        """
        self.__redocPath = Router.normalizePath(path)
        return self

    def format(self, format):
        """
        Enable what format are available (json or yaml).
   
        IMPORTANT: UI tools requires the JSON format.
   
        @param format Supported formats.
        @return This module.
        """
        self.__format = set(format)
    
    def fullPath(self, contextPath, path):
        return Router.noTrailingSlash(Router.normalizePath(contextPath + path))
    
    
    def configureUI(self, application):
        ui = {} # String -> Consumer2<Jooby, AssetSource>
        ui['swagger-ui'] = self.swaggerUI
        ui['redoc'] = self.redoc
        classLoader = application.getClassLoader()
        for name, consumer in ui.items():
            if classLoader.getResource(name + '/index.html') != None:
                if self.Format.JSON in self.__format:
                    consumer.accept(application, AssetSource.create(classLoader, name))
                else:
                    application.getLog().debug("{} is disabled when json format is not supported", name)

    def install(self, application):
        directory = application.getBasePackage()
        if directory == None:
            directory = '/'
        else:
            directory = directory.replace('.', '/')
        
        appname = application.getName().replace('joopy', 'openapi')

        for ext in self.__format:
            filename = '/{}.{}'.format(appname, ext.lower())
            openAPIFileLocation = Router.normalizePath(directory) + filename
            application.assets(self.fullPath(self.__openAPIPath, '/openapi.' + ext.lower()), \
                openAPIFileLocation)
        
        """
        Configure UI:
        """
        self.configureUI(application)

    def redocJoopy(self, application, source):
        application.assets(self.__redocPath + '/*', source)
        openAPIJSON = self.fullPath(self.fullPath(application.getContextPath(), self.__openAPIPath), \
            '/openapi.json')
        with open(source + 'index.html') as f:
            template = f.readline()
        template = template.replace('${openAPIPath}', openAPIJSON).replace('${redocPath}', \
            self.fullPath(application.getContextPath(), self.__redocPath))
        application.get(self.__redocPath, lambda ctx : ctx.setResponseType(MediaType.html).send(template))

    def swaggerUIJoopy(self, application, source):
        openAPIJSON = self.fullPath(self.fullPath(application.getContextPath(), self.__openAPIPath), \
            '/openapi.json')
        with open(source + 'index.html') as f:
            template = f.readline()
        template = template.replace('${openAPIPath}', openAPIJSON).replace('${swaggerPath}', \
            self.fullPath(application.getContextPath(), self.__swaggerUIPath))
        application.assets(self.__swaggerUIPath + '/*', source)
        application.get(self.__swaggerUIPath, lambda ctx : ctx.setResponseType(MediaType.html).send(template))
