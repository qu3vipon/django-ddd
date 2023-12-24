from typing import Any, Dict, TypeVar

from django.db.models import ForeignKey, Model

from shared.domain.entity import EntityType

DjangoModelType = TypeVar("DjangoModelType", bound=Model)


class ModelMapper:
    model_class = None
    entity_class = None
    fk_map: Dict[str, DjangoModelType] = {}

    def instance_to_entity(self, instance: DjangoModelType, entity_class: EntityType | None = None) -> EntityType:
        if entity_class is None:
            entity_class = self.entity_class

        entity_values: Dict[str, Any] = {}
        for field in instance._meta.fields:
            if issubclass(type(field), ForeignKey):
                entity_values[field.name] = self.instance_to_entity(
                    instance=getattr(instance, field.name),
                    entity_class=self.fk_map[field.name]["entity"],
                )
            else:
                entity_values[field.name] = getattr(instance, field.name)

        return entity_class(**entity_values)

    def entity_to_instance(self, entity: EntityType, model_class: DjangoModelType | None = None) -> DjangoModelType:
        if model_class is None:
            model_class = self.model_class

        instance_values: Dict[str, Any] = {}
        for field_name in entity.__dataclass_fields__.keys():
            field: Any = getattr(entity, field_name)
            if hasattr(field, "__dataclass_fields__"):
                instance_values[field_name] = self.entity_to_instance(
                    entity=field,
                    model_class=self.fk_map[field_name]["model"],
                )
            else:
                instance_values[field_name] = field

        return model_class(**instance_values)
