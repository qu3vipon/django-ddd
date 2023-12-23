from shared.infra.repository.rdb import RDBRepository
from .mapper import ToDoMapper


class ToDoRDBRepository(RDBRepository):
    def __int__(self, model_mapper: ToDoMapper):
        self.model_mapper = model_mapper
