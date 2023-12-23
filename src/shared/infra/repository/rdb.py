from typing import List

from shared.domain.entity import EntityType
from shared.infra.repository.mapper import ModelMapper, DjangoModelType


class RDBRepository:
    def __init__(self, model_mapper: ModelMapper):
        self.model_mapper = model_mapper

    def save(self, entity: EntityType) -> EntityType:
        instance: DjangoModelType = self.model_mapper.entity_to_instance(entity=entity)
        instance.save()
        return self.model_mapper.instance_to_entity(instance=instance)

    def _get_by_pk(self, pk: int) -> EntityType:
        return self.model_mapper.instance_to_entity(
            self.model_mapper.model_class.objects.get(pk=pk)
        )

    def _get_by(self, **kwargs) -> EntityType:
        return self.model_mapper.instance_to_entity(
            self.model_mapper.model_class.objects.get(**kwargs)
        )

    def _filter_by(self, **kwargs) -> List[EntityType]:
        return [
            self.model_mapper.instance_to_entity(instance=i)
            for i in self.model_mapper.model_class.objects.filter(**kwargs)
        ]

    def _delete(self, **kwargs) -> None:
        self.model_mapper.model_class.objects.get(**kwargs).delete()
