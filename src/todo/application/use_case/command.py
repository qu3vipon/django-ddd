from datetime import datetime

from todo.domain.entity import ToDo
from todo.infra.database.repository.rdb import ToDoRDBRepository


class ToDoCommand:
    def __init__(self, todo_repo: ToDoRDBRepository):
        self.todo_repo = todo_repo

    def create_todo(self, contents: str, due_datetime: datetime) -> ToDo:
        todo: ToDo = ToDo.new(contents=contents, due_datetime=due_datetime)
        return self.todo_repo.save(entity=todo)

    def update_todo(self, todo: ToDo, contents: str | None, due_datetime: datetime | None) -> ToDo:
        if contents:
            todo.update_contents(contents=contents)

        if due_datetime:
            todo.update_due_datetime(due_datetime=due_datetime)

        return self.todo_repo.save(entity=todo)

    def delete_todo_by_id(self, todo_id: int) -> None:
        self.todo_repo.delete_todo_by_id(todo_id=todo_id)
