class CacheControl:
    """
    Constant for the max-age parameter, when set, the {@code Cache-Control} header is set to {@code no-store, must-revalidate}.
    @see #setMaxAge(long)
    """

    UNDEFINED = -1
    NO_CACHE = -2

    def __init__(self):
        self.__etag = True
        self.__last_modified = True
        self.__max_age = -1

    def is_etag(self) -> bool:
        """
        Returns whether e-tag support is enabled.
        @return {@code true} if enabled.
        """

        return self.__etag

    def is_last_modified(self) -> bool:
        """
        Returns whether the handling of {@code If-Modified-Since} header is enabled.
        @return {@code true} if enabled.
        """
        return self.__last_modified

    def get_max_age(self) -> int:
        """
        Returns the max-age header parameter value.
        @return the max-age header parameter value.
        """
        return self.__max_age

    def set_etag(self, etag: bool):
        """
        Turn on/off e-tag support.
        @param etag True for turning on.
        @return This instance.
        """
        self.__etag = etag
        return self

    def set_last_modified(self, last_modified: bool):
        """
        Turn on/off handling of {@code If-Modified-Since} header.
        @param lastModified True for turning on. Default is: true.
        @return This instance.
        """
        self.__last_modified = last_modified
        return self

    def set_max_age(self, max_age: int):
        """
        Set cache-control header with the given max-age value. If max-age is greater than 0.
        @param maxAge Max-age value in seconds.
        @return This instance.
        @see #UNDEFINED
        @see #NO_CACHE
        """
        self.__max_age = max_age
        return self

    def set_no_cache(self):
        self.__etag = False
        self.__last_modified = False
        self.__max_age = CacheControl.NO_CACHE
        return self

    @staticmethod
    def defaults():
        return CacheControl()

    @staticmethod
    def no_cache():
        return CacheControl.defaults().set_no_cache()
