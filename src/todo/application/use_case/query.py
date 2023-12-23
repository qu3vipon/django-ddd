from todo.domain.entity import ToDo
from todo.infra.database.repository.rdb import ToDoRDBRepository


class ToDoQuery:
    def __init__(self, todo_repo: ToDoRDBRepository):
        self.todo_repo = todo_repo

    def get_todo_by_id(self, todo_id: int) -> ToDo:
        return self.todo_repo.get_todo_by_id(todo_id=todo_id)
