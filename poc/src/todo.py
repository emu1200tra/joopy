from multipledispatch import dispatch

class ValueConverters:
    pass

class Runnable:
    pass

class RouteSet:
    pass

class RouterOption:
    pass

class Context:
    pass

class ClassSource:
    pass

class RouteAnalyzer:
    pass

class Pipeline:
    pass

class MediaType:
    def __init__(self):
        self.__value = None # String

    @dispatch(Object) # str or MediaType
    def matches(self, str_or_mediaType) -> bool:
        if isinstance(str_or_mediaType, str):
            return self.matches(self.__value, str_or_mediaType)
        elif isinstance(str_or_mediaType, MediaType):
            return self.matches(self.__value, str_or_mediaType.__value)
        else:
            raise ValueError('input type must be String or MediaType')

    @staticmethod
    @dispatch(str, str)
    def matches(self, expected: str, contentType: str) -> bool:
        start, len1, end = 0, len(expected), contentType.index(',')
    
        while end != -1:
            if self.matchOne(expected, len1, contentType[start: end].strip()):
                return True
            
            start, end = end + 1, contentType.index(',', start)
        
        clen = len(contentType)
        if start < clen:
            return self.matchOne(expected, len1, contentType[start: clen].strip())
        
        return False


    def matchOne(self, expected: str, len1: int, contentType: str) -> bool:
        if contentType.startswith('*/*') or contentType == '*':
            return True

        i, len2, len = 0, len(contentType), min(len1, len2)

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

class Executor:
    pass

class ForwardingExecutor:
    # implement Executor
    pass

class MessageEncoder:
    pass

class HttpMessageEncoder:
    # implement MessageEncoder
    pass