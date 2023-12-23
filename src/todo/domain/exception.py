from shared.domain.exception import NotFoundException


class ToDoNotFoundException(NotFoundException):
    model_name = "ToDo"
