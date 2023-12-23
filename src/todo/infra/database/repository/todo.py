from shared.infra.repository.rdb import RDBRepository
from .mapper import ToDoMapper


class ToDoRDBRepository(RDBRepository):
    def __int__(self, model_mapper: ToDoMapper):
        self.model_mapper = model_mapper

    def get_todo_by_id(self, todo_id: int):
        return super().get_by_pk(pk=todo_id)
