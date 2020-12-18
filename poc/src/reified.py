class Reified:
    """
    /**
    * Get raw type (class) from given type.
    *
    * @param type Type.
    * @return Raw type.
    */
    """

    @staticmethod
    def raw_type(Type) -> str:
        return str(type(Type))[8: -2] # <class 'int'> => int
