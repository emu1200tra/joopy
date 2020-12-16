from multipledispatch import dispatch

class MediaType:
    def __init__(self):
        self.__value = None # String
        self.__raw = None # String
        self.__charset = None # Charset
        self.__subtypeStart = None # int
        """
        private MediaType(@Nonnull String value, Charset charset) {
            this.raw = value;
            this.subtypeStart = value.indexOf('/');
            if (subtypeStart < 0) {
                throw new IllegalArgumentException("Invalid media type: " + value);
            }
            int subtypeEnd = value.indexOf(';');
            if (subtypeEnd < 0) {
                this.value = raw;
                this.subtypeEnd = value.length();
            } else {
                this.value = raw.substring(0, subtypeEnd);
                this.subtypeEnd = subtypeEnd;
            }
            this.charset = charset;
        }
        """

    @dispatch(object) # str or MediaType
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
        len = min(len1, len2)

        while i < len:
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
        
        return i == len and len1 == len2
