from shared.domain.entity import EntityType
from shared.infra.repository.mapper import ModelMapper, DjangoModelType


class RDBRepository:
    def __init__(self, model_mapper: ModelMapper):
        self.model_mapper = model_mapper

    def get_by_pk(self, pk: int) -> EntityType:
        return self.model_mapper.model_to_entity(
            self.model_mapper.model_class.objects.get(pk=pk)
        )

    def save(self, entity: EntityType) -> EntityType:
        model: DjangoModelType = self.model_mapper.entity_to_model(entity=entity)
        model.save()
        return self.model_mapper.model_to_entity(model=model)
