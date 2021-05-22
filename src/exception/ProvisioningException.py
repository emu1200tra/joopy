from StatusCode import StatusCode
from StatusCodeBase import StatusCodeBase
from StatusCodeException import StatusCodeException
from BadRequestException import BadRequestException


"""
Provisioning exception, throws by MVC routes when parameter binding fails.

"""


class ProvisioningException(BadRequestException):
    def __init__(self, parameter, cause):
        super(ProvisioningException, self).__init__(parameter)
        """
        Creates a provisioning exception.
        @param parameter Failing parameter.
        @param cause Cause.

        """

def main():
    parameter = 'p'
    cause = 'c'
    aa = ProvisioningException(parameter, cause)
    import ipdb; ipdb.set_trace()


if __name__ == "__main__":
    main()