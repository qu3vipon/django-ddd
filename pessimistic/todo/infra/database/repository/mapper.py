from shared.infra.repository.mapper import ModelMapperInterface
from user.infra.database.repository.mapper import UserMapper

from todo.domain.entity import ToDo as ToDoEntity
from todo.infra.database.models import ToDo as ToDoModel


class ToDoMapper(ModelMapperInterface):
    def __init__(self, user_mapper: UserMapper):
        self.user_mapper = user_mapper

    def to_entity(self, instance: ToDoModel) -> ToDoEntity:
        return ToDoEntity(
            id=instance.id,
            contents=instance.contents,
            due_datetime=instance.due_datetime,
            user=self.user_mapper.to_entity(instance=instance.user),
        )

    def to_instance(self, entity: ToDoEntity) -> ToDoModel:
        return ToDoModel(
            id=entity.id,
            contents=entity.contents,
            due_datetime=entity.due_datetime,
            user=self.user_mapper.to_instance(entity=entity.user),
        )
