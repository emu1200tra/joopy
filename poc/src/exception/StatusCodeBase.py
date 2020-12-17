from final_class import final

@final
class StatusCodeBase:
    def __init__(self, value, reason):
        self.__value = value
        self.__reason = reason
    
    def value(self):
        return self.__value
    
    def reason(self):
        return self.__reason

    # Return a string representation of this status code.
    def toString(self):
        """
        Usage Example: StatusCode.OK.toString() return: 'Success(200)'

        """
        return self.reason()+"("+str(self.value())+")"

    def equals(self, obj):
        if isinstance(obj, StatusCodeBase):
            return self.value() == obj.value()
        return False

    def hashCode(self):
        return self.value()

    def valueOf(self, statusCode):
        pass