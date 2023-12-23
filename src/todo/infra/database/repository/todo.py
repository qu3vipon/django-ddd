from shared.infra.repository.rdb import RDBRepository
from todo.domain.entity import ToDo
from todo.domain.exception import ToDoNotFoundException
from .mapper import ToDoMapper


class ToDoRDBRepository(RDBRepository):
    def __int__(self, model_mapper: ToDoMapper):
        self.model_mapper = model_mapper

    def get_todo_by_id(self, todo_id: int) -> ToDo:
        try:
            return super()._get_by_pk(pk=todo_id)
        except self.model_mapper.model_class.DoesNotExist:
            raise ToDoNotFoundException()

    def delete_todo_by_id(self, todo_id: int) -> None:
        try:
            super()._delete_by_pk(pk=todo_id)
        except self.model_mapper.model_class.DoesNotExist:
            raise ToDoNotFoundException()
