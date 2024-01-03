from user.infra.di_containers import user_mapper

from todo.application.use_case.command import ToDoCommand
from todo.application.use_case.query import ToDoQuery
from todo.infra.database.repository.mapper import ToDoMapper
from todo.infra.database.repository.rdb import ToDoRDBRepository

todo_mapper = ToDoMapper(user_mapper=user_mapper)
todo_repo: ToDoRDBRepository = ToDoRDBRepository(model_mapper=todo_mapper)

todo_query: ToDoQuery = ToDoQuery(todo_repo=todo_repo)
todo_command: ToDoCommand = ToDoCommand(todo_repo=todo_repo)
