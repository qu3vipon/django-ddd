from shared.domain.exception import BaseMsgException, NotFoundException


class ToDoNotFoundException(NotFoundException):
    model_name = "ToDo"
