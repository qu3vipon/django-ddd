from typing import List

from shared.infra.repository.rdb import RDBRepository

from todo.domain.entity import ToDo as ToDoEntity
from todo.domain.exception import ToDoNotFoundException
from todo.infra.database.models import ToDo as ToDoModel
from todo.infra.database.repository.mapper import ToDoMapper


class ToDoRDBRepository(RDBRepository):
    def __init__(self, model_mapper: ToDoMapper = ToDoMapper()):
        self.model_mapper = model_mapper

    def get_todo_of_user(self, user_id: int, todo_id: int) -> ToDoEntity:
        try:
            return self.model_mapper.to_entity(instance=ToDoModel.objects.get(id=todo_id, user_id=user_id))
        except ToDoModel.DoesNotExist:
            raise ToDoNotFoundException

    def get_todos_of_user(self, user_id: int) -> List[ToDoEntity]:
        return self.model_mapper.to_entity_list(instances=ToDoModel.objects.filter(user_id=user_id))

    @staticmethod
    def delete_todo_of_user(user_id: int, todo_id: int) -> None:
        try:
            ToDoModel.objects.get(id=todo_id, user_id=user_id).delete()
        except ToDoModel.DoesNotExist:
            raise ToDoNotFoundException
