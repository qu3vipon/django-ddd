class BaseMsgException(Exception):
    message: str

    def __str__(self):
        return self.message


class JWTKeyParsingException(BaseMsgException):
    message: str = "Invalid JWT Key Error"


class NotAuthorizedException(BaseMsgException):
    message = "Not Authorized"
