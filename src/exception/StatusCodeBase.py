from final_class import final


"""
Degelagte from Class: StatusCode
requirement: final_class module, `pip install final-class`

"""


@final
class StatusCodeBase:
    def __init__(self, value, reason):
        self.__value = value
        self.__reason = reason
    
    # return the integer value of this status code
    def value(self):
        return self.__value
    
    # return the reason phrase of this status code 
    def reason(self):
        return self.__reason

    # Return a string representation of this status code.
    def toString(self):
        """
        Usage Example: StatusCode.OK.toString() return: '200 Success'

        """
        # fix some bugs 
        temp = self.reason()
        temp = temp.split(" ")
        if not temp[0].isdigit():
            return str(self.value()) + " " + self.reason()
        else:
            return self.reason()

    def equals(self, obj):
        if isinstance(obj, StatusCodeBase):
            return self.value() == obj.value()
        return False

    def hashCode(self):
        return self.value()

    def valueOf(self, statusCode):
        raise NotImplementedError("[Warning] Implemeted in Class: StatusCode !")