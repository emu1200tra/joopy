from Route import Route


class AssetHandler(Route.Handler):
    
    __ONE_SEC = 1000

    # private final AssetSource[] sources;
    __source = None

    # private final CacheControl defaults = CacheControl.defaults();
    
