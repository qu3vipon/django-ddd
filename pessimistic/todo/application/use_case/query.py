from typing import List

from todo.domain.entity import ToDo
from todo.infra.database.repository.rdb import ToDoRDBRepository


class ToDoQuery:
    def __init__(self, todo_repo: ToDoRDBRepository):
        self.todo_repo = todo_repo

    def get_todo_of_user(self, user_id: int, todo_id: int) -> ToDo:
        return self.todo_repo.get_todo_of_user(user_id=user_id, todo_id=todo_id)

    def get_todos_of_user(self, user_id: int) -> List[ToDo]:
        return self.todo_repo.get_todos_of_user(user_id=user_id)
