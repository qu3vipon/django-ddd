class BaseMsgException(Exception):
    message: str

    def __str__(self):
        return self.message


class NotFoundException(Exception):
    model_name: str

    def __str__(self):
        return f"{self.model_name} Not Found"


class JWTKeyParsingException(BaseMsgException):
    message: str = "Invalid JWT Key Error"


class NotAuthorizedException(BaseMsgException):
    message = "Not Authorized"
