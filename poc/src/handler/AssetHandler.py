from ..Route import Handler
class AssetHandler(Handler):
    '''
    * Handler for static resources represented by the {@link Asset} contract.
    *
    * It has built-in support for static-static as well as SPAs (single page applications).
    *
    * @author edgar
    * @since 2.0.0
    '''
    def __init__(self, fallback, sources):
        self.ONE_SEC = 1000
        self.sources = sources
        #self.defaults = CacheControl.defaults()
        self.filekey = ''
        self.fallback = fallback
        #self.cacheControl = lambda path : self.defaults
