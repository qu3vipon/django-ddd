from shared.domain.entity import EntityType
from shared.infra.repository.mapper import DjangoModelType, ModelMapperInterface


class RDBRepository:
    model_mapper: ModelMapperInterface

    def save(self, entity: EntityType) -> EntityType:
        instance: DjangoModelType = self.model_mapper.to_instance(entity=entity)
        instance.save()
        return self.model_mapper.to_entity(instance=instance)
