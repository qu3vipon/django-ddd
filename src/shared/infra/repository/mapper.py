from typing import TypeVar

from django.db.models import Model

from shared.domain.entity import EntityType

DjangoModelType = TypeVar("DjangoModelType", bound=Model)


class ModelMapper:
    model_class = None
    entity_class = None

    def model_to_entity(self, model: DjangoModelType) -> EntityType:
        return self.entity_class(
            **{field.name: getattr(model, field.name) for field in model._meta.fields}
        )

    def entity_to_model(self, entity: EntityType) -> DjangoModelType:
        return self.model_class(
            **{field: getattr(entity, field) for field in entity.__dataclass_fields__.keys()}
        )
