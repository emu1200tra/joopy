from .todo import *

class RouteAnalyzer:
    def __init__(self, source: ClassSource, debug: bool):
        self.__source = source
        self.__typeParser = None # TypeParser(source.getLoader())
        self.__debug = debug
    
    def returnType(handler: object):
        pass