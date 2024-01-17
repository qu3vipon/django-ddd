from datetime import datetime

from user.domain.entity import User

from todo.domain.entity import ToDo
from todo.infra.database.repository.rdb import ToDoRDBRepository


class ToDoCommand:
    def __init__(self, todo_repo: ToDoRDBRepository):
        self.todo_repo = todo_repo

    def create_todo(self, user: User, contents: str, due_datetime: datetime) -> ToDo:
        todo: ToDo = ToDo.new(user=user, contents=contents, due_datetime=due_datetime)
        return self.todo_repo.save(entity=todo)

    def update_todo(self, todo: ToDo, contents: str | None, due_datetime: datetime | None) -> ToDo:
        if contents:
            todo.update_contents(contents=contents)

        if due_datetime:
            todo.update_due_datetime(due_datetime=due_datetime)

        return self.todo_repo.save(entity=todo)

    def delete_todo_of_user(self, user_id: int, todo_id: int) -> None:
        self.todo_repo.delete_todo_of_user(user_id=user_id, todo_id=todo_id)
