from shared.infra.repository.mapper import ModelMapper
from user.domain.entity import User as UserEntity
from user.infra.database.models import User as UserModel

from todo.domain.entity import ToDo as ToDoEntity
from todo.infra.database.models import ToDo as ToDoModel


class ToDoMapper(ModelMapper):
    model_class = ToDoModel
    entity_class = ToDoEntity
    fk_map = {
        "user": {
            "model": UserModel,
            "entity": UserEntity,
        }
    }
