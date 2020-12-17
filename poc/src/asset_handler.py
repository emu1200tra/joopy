from multipledispatch import dispatch
from cache_control import CacheControl
# from Route import Route
from asset_source import AssetSource
from collections import Iterable
import datetime


class StatusCode:
    NOT_FOUND = "404"
    NOT_MODIFIED = "lalala"


class AssetHandler:

    __ONE_SEC = 1000

    @dispatch(str, Iterable)
    def __init__(self, fallback: str, sources: Iterable):
        """Creates a new asset handler that fallback to the given fallback asset when the asset
        is not found. Instead of produces a <code>404</code> its fallback to the given asset.

        <pre>{@code{
            assets(
                    "/?", new AssetHandler("index.html", AssetSource.create(Paths.get("...")));
                }
            }</pre>

         The fallback option makes the asset handler to work like a SPA (Single-Application-Page).

        @param fallback Fallback asset.
        @param sources Asset sources.
        """

        # private final AssetSource[] sources;
        self.__sources = sources
        self.__defaults = CacheControl.defaults()
        self.__file_key = None
        self.__fallback = fallback

        # private Function<String, CacheControl> cacheControl = path -> defaults;
        self.__cache_control = lambda path: self.__defaults

    @dispatch(Iterable)
    def __init__(self, sources: Iterable):
        self.__sources = sources

    def apply(self, ctx):
        resolved_path = None
        file_path = ctx.path_map().get_or_default(self.__file_key, "index.html")
        asset = self.__resolve(file_path)

        if asset is None:
            if self.__fallback is not None:
                asset = self.__resolve(self.__fallback)

            # still None ?
            if asset is None:
                ctx.send(StatusCode.NOT_FOUND)
                return ctx
            else:
                resolved_path = self.__fallback

        else:
            resolved_path = file_path

        cache_parms = self.__cache_control.apply(resolved_path)

        # handle If-None-Match
        if cache_parms.is_etag():
            # ifnm = if not match
            ifnm = ctx.header(name="If-None-Match").value(None)
            if (ifnm is not None) and (ifnm == asset.get_etag()):
                ctx.send(StatusCode.NOT_MODIFIED)
                asset.close()
                return ctx

            else:
                ctx.set_response_header("Etag", asset.get_etag())

        # Handle If-Modified-Since
        if cache_parms.is_last_modified():
            last_modified = asset.get_last_modified()
            if last_modified > 0:
                ifms = ctx.header("If-Modified-Since").long_value(-1)
                ONE_SEC = AssetHandler.__ONE_SEC
                if last_modified // ONE_SEC <= ifms // ONE_SEC:
                    ctx.send(StatusCode.NOT_MODIFIED)
                    asset.close()
                    return ctx
                ctx.set_response_header(
                    "Last-Modified", datetime.datetime.strptime(last_modified, "%Y-%m-%dT%H:%M:%S.%fZ"))

    def __resolve(self, file_path):
        for s in self.__sources:
            asset = s.resolve(file_path)
            if asset is not None:
                return asset
