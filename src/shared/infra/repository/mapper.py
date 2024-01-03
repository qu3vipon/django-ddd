from typing import List, TypeVar

from django.db.models import Model

from shared.domain.entity import EntityType

DjangoModelType = TypeVar("DjangoModelType", bound=Model)


class ModelMapperInterface:
    def to_entity(self, instance: DjangoModelType) -> EntityType:
        raise NotImplementedError

    def to_instance(self, entity: EntityType) -> DjangoModelType:
        raise NotImplementedError

    def to_entity_list(self, instances: List[DjangoModelType]) -> List[EntityType]:
        return [self.to_entity(instance=i) for i in instances]

    def to_instance_list(self, entities: List[EntityType]) -> List[DjangoModelType]:
        return [self.to_instance(entity=e) for e in entities]
