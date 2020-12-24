from multipledispatch import dispatch

class MediaTypeBase:
    def __init__(self, value, charset):
        self.raw = value # String
        self.subtypeStart = value.index('/') # int
        self.subtypeEnd = None # int
        self.value = None # String

        if self.subtypeStart < 0:
            raise Exception('Invalid media type' + value)
        if ';' not in value:
            self.value = self.raw
            self.subtypeEnd = len(value)
        else:
            subtypeEnd = value.index(';')
            self.value = self.raw[0: subtypeEnd]
            self.subtypeEnd = subtypeEnd
        self.charset = charset

class MediaType:
    JSON = 'application/json' # static string
    json = MediaTypeBase(JSON, 'UTF_8'); # static MediaType; UTF_8 is charset in java

    def __init__(self):
        self.__raw = MediaType.json.value
        self.__subtypeStart = MediaType.json.subtypeStart
        self.__subtypeEnd = MediaType.json.subtypeEnd
        self.__value = MediaType.json.value
        self.__charset = MediaType.json.charset

    @dispatch(object)  # str or MediaType
    def matches(self, str_or_mediaType) -> bool:
        if isinstance(str_or_mediaType, str):
            return MediaType.matches(self.__value, str_or_mediaType)
        elif isinstance(str_or_mediaType, MediaType):
            return MediaType.matches(self.__value, str_or_mediaType.__value)
        else:
            raise ValueError('input type must be String or MediaType')

    @staticmethod
    @dispatch(str, str)
    def matches(expected: str, contentType: str) -> bool:
        start, len1, end = 0, len(expected), contentType.index(',')

        while end != -1:
            if MediaType.matchOne(expected, len1, contentType[start: end].strip()):
                return True

            start, end = end + 1, contentType.index(',', start)

        clen = len(contentType)
        if start < clen:
            return MediaType.matchOne(expected, len1, contentType[start: clen].strip())

        return False

    @staticmethod
    def matchOne(expected: str, len1: int, contentType: str) -> bool:
        if contentType.startswith('*/*') or contentType == '*':
            return True

        i, len2 = 0, len(contentType)
        len_ = min(len1, len2)

        while i < len_:
            ch1 = expected[i]
            ch2 = contentType[i]

            if ch1 != ch2:
                if i > 0:
                    prev = expected[i-1]
                    if prev == '/':
                        if ch1 == '*':
                            if i == len1 - 1:
                                return True

                            # tail/suffix matches
                            j, k = len1 - 1, len2 - 1
                            while j > i:
                                if expected[j] != contentType[k]:
                                    return False

                                j, k = j - 1, k - 1

                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            i += 1

        return i == len_ and len1 == len2
