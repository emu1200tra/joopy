from StatusCode import StatusCode
from StatusCodeBase import StatusCodeBase
from StatusCodeException import StatusCodeException
from BadRequestException import BadRequestException


"""
Missing exception. Used when a required attribute/value is missing.

"""


class MissingValueException(BadRequestException):
    def __init__(self, name):
        super(MissingValueException, self).__init__(name)
        """
        Creates a missing exception.
        @param name Parameter/attribute name.
        
        """
        self.__name = name

    def __str__(self):
        return "Missing value: {}".format(self.__name)

    def getName(self):
        """
        Parameter/attribute name
        @return Parameter/attribute name.

        """
        return self.__name

    @staticmethod
    def requireNonNull(name, value):
        """
        Check if the given value is null and throw a {@link MissingValueException} exception
        @param name Attribute's name.
        @param value Value to check.
        @return Input value
    
        """
        if value is None:
            raise MissingValueException(name)
        return value


def main():
    name = "User"
    aa = MissingValueException(name)
    import ipdb; ipdb.set_trace()


if __name__ == "__main__":
    main()
