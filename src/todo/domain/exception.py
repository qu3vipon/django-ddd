from shared.domain.exception import BaseMsgException


class ToDoNotFoundException(BaseMsgException):
    message = "ToDo Not Found"
