from StatusCode import StatusCode
from StatusCodeBase import StatusCodeBase
from StatusCodeException import StatusCodeException
from BadRequestException import BadRequestException

"""
Type mismatch exception. Used when a value can't be converted to the required type.

"""


class TypeMismatchException(BadRequestException):
    def __init__(self, name, Type):
        super(TypeMismatchException, self).__init__(name)
        """
        Creates a type mismatch error.
        @param name Parameter/attribute name.
        @param type Parameter/attribute type.
        @param cause Cause.
        
        """
        self.__name = name
        self.__type = Type
    
    def __str__(self):
        return "Connot convert value: {} to {}".format(self.__name, self.__type)

    def getName(self):
        return self.__name


def main():
    name = "body"
    Type = "Type"
    aa = TypeMismatchException(name, Type)
    import ipdb; ipdb.set_trace()


if __name__ == "__main__":
    main()