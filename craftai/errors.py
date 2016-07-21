class CraftAIError(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, message):
        super(CraftAIError, self).__init__(message)

    def __str__(self):
        return repr(self.message)


class CraftAIUnknownError(CraftAIError):
    """docstring for CraftAIUnknownError"""
    def __init__(self, message):
        self.message = "".join(("Unknwon error occured. ", message))
        super(CraftAIError, self).__init__(message)


class CraftAINetworkError(CraftAIError):
    """docstring for CraftAINetworkError"""
    def __init__(self, message):
        self.message = "".join(("Network issue: ", message))
        super(CraftAIError, self).__init__(message)


class CraftAICredentialsError(CraftAIError):
    """docstring for CraftAICredentialsError"""
    def __init__(self, message):
        self.message = "".join((
            "Credentials error, make sure the given owner/token are valid.",
            message
        ))
        super(CraftAIError, self).__init__(message)


class CraftAIInternalError(CraftAIError):
    """docstring for CraftAIInternalError"""
    def __init__(self, message):
        self.message = "".join(("Internal error occured", message))
        super(CraftAIError, self).__init__(message)


class CraftAIBadRequestError(CraftAIError):
    """docstring for CraftAIBadRequestError"""
    def __init__(self, message):
        self.message = "".join(("Bad request: ", message))
        super(CraftAIError, self).__init__(message)
