from todo.application.use_case.command import ToDoCommand
from todo.application.use_case.query import ToDoQuery
from todo.infra.database.repository.rdb import ToDoRDBRepository

todo_repo: ToDoRDBRepository = ToDoRDBRepository()

todo_query: ToDoQuery = ToDoQuery(todo_repo=todo_repo)
todo_command: ToDoCommand = ToDoCommand(todo_repo=todo_repo)
