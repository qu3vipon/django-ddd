from typing import List

from shared.infra.repository.rdb import RDBRepository

from todo.domain.entity import ToDo
from todo.domain.exception import ToDoNotFoundException

from .mapper import ToDoMapper


class ToDoRDBRepository(RDBRepository):
    def __int__(self, model_mapper: ToDoMapper):
        self.model_mapper = model_mapper

    def get_todo_of_user(self, user_id: int, todo_id: int) -> ToDo:
        try:
            return self._get_by(id=todo_id, user_id=user_id)
        except self.model_mapper.model_class.DoesNotExist:
            raise ToDoNotFoundException()

    def get_todos_of_user(self, user_id: int) -> List[ToDo]:
        return self._filter_by(user_id=user_id)

    def delete_todo_of_user(self, user_id: int, todo_id: int) -> None:
        try:
            self._delete(id=todo_id, user_id=user_id)
        except self.model_mapper.model_class.DoesNotExist:
            raise ToDoNotFoundException()
