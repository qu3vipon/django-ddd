from todo.infra.database.repository.mapper import ToDoMapper
from todo.infra.database.repository.todo import ToDoRDBRepository

todo_repo: ToDoRDBRepository = ToDoRDBRepository(
    model_mapper=ToDoMapper(),
)
