from shared.infra.repository.mapper import ModelMapper

from todo.domain.entity import ToDo as ToDoEntity
from todo.infra.database.models import ToDo as ToDoModel


class ToDoMapper(ModelMapper):
    model_class = ToDoModel
    entity_class = ToDoEntity
