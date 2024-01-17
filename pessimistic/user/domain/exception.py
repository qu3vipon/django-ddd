from shared.domain.exception import BaseMsgException


class UserNotFoundException(BaseMsgException):
    message = "User Not Found"
